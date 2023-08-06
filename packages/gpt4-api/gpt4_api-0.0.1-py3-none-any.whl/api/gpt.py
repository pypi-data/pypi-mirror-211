import threading
import logging
import time
import openai
import asyncio
from pathlib import Path
from multiprocessing import JoinableQueue
from queue import Empty

logging.basicConfig(filename='gpt.log', level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')


class GPTTaskManager:
    def __init__(self, num_threads):
        self.num_threads = num_threads
        self.task_queue = JoinableQueue()

    def __worker(self, run_func):
        logging.disable(logging.NOTSET)
        while True:
            try:
                task = self.task_queue.get(timeout=1)
                content = task.get("ask")
                messages = task.get("messages")
                run_func(task, content, messages)
                self.task_queue.task_done()
            except Empty:
                break

    def _run_tasks(self, tasks, run_func):
        threads = []
        logging.info("Total threads: %s" % self.num_threads)
        for _ in range(self.num_threads):
            thread = threading.Thread(target=self.__worker, args=(run_func,))
            thread.start()
            threads.append(thread)
        logging.info("Total tasks: %s" % len(tasks))
        for task in tasks:
            self.task_queue.put(task)
        self.task_queue.join()
        for thread in threads:
            thread.join()


class GPT4(GPTTaskManager):
    def __init__(self, keys=None, model='gpt-4', temperature=0.8, top_p=1, presence_penalty=0, frequency_penalty=0, n=1,
                 stream=False, system_content=None, num_threads=50, result_call_black=None, key_limit=2048, max_retries=3):
        # 模型
        self.model = model
        # 用于控制生成文本的随机性和创造性的参数。值越高，生成文本越随机和创造性；值越低，生成文本越可预测和保守
        self.temperature = temperature
        # 用于对生成文本进行选择的参数，它表示只选择所有可能的令牌中累计概率高于给定阈值的那些令牌。默认值为1，表示选择所有可能的令牌
        self.top_p = top_p
        # 用于惩罚生成文本中未出现过的片段的参数。默认值为0，表示不进行惩罚
        self.presence_penalty = presence_penalty
        # 用于惩罚生成文本中频繁出现的重复片段的参数。默认值为0，表示不进行惩罚
        self.frequency_penalty = frequency_penalty
        # 要生成的文本的数量。默认为1，表示生成一段文本
        self.n = n
        # 是否将生成的文本作为流返回，而不是一次性返回所有文本。默认为False，表示一次性返回所有文本
        self.stream = stream
        # 系统默认内容
        self.system_content = system_content
        self.messages = []
        self.call_black = result_call_black
        self.key_lock = threading.Lock()
        self.key_limit = key_limit
        self.max_retries = max_retries
        self.usable_openai_keys = self.process_token(keys=keys) or []
        super(GPT4, self).__init__(num_threads=num_threads)

    @staticmethod
    def process_token(keys):
        usable_openai_keys = []
        for key in keys:
            usable_openai_keys.append({"api_key": key, "token_limit": 0})
        if len(usable_openai_keys) == 0:
            raise Exception("Unable to execute gpt task without token")
        logging.info("Total tokens: %s" % len(usable_openai_keys))
        return usable_openai_keys

    @staticmethod
    def read_prompt(path):
        return Path(path).read_text()

    def retry_on_error(self, task, ask_content, messages, retries):
        retries += 1
        if retries <= self.max_retries:
            self.process_task(task, ask_content, messages, retries=retries, retry=True)
        else:
            self.task_queue.put(task)

    def __get_key(self):
        with self.key_lock:
            sorted_data = sorted(self.usable_openai_keys, key=lambda x: x['token_limit'], reverse=True)
            if len(sorted_data) <= 0:
                return False
            open_ai_key = sorted_data[0].get("api_key")
            token_limit = sorted_data[0].get("token_limit")
            if open_ai_key and token_limit >= self.key_limit:
                logging.info("Token re election")
                return self.__get_key()
            return open_ai_key

    def __release_token(self, open_ai_key):
        for openaiKey in self.usable_openai_keys:
            if openaiKey.get("api_key", None) == open_ai_key:
                openaiKey["token_limit"] = 0

    @staticmethod
    def __get_active_thread_count():
        return threading.active_count() - 1

    def process_task(self, task, ask_content, messages, retries=1, retry=False):
        open_ai_key = self.__get_key()
        if open_ai_key:
            if len(messages) == 0 and self.system_content:
                messages.append({"role": "system", "content": self.system_content})
            if not retry:
                messages.append({"role": "user", "content": ask_content})
            try:
                start_time = time.time()
                response = openai.ChatCompletion.create(
                    model=self.model,
                    messages=messages,
                    temperature=self.temperature,
                    api_key=open_ai_key
                )
                elapsed_time = time.time() - start_time
                response_str = response['choices'][0]['message']['content']
                messages.append({"role": response['choices'][0]['message']['role'], "content": response_str})
                completion_tokens = response['usage']['completion_tokens']
                prompt_tokens = response['usage']['prompt_tokens']
                total_tokens = response['usage']['total_tokens']
                logging.info("request cost time: %s second" % int(elapsed_time))
                logging.info("prompt tokens: %s" % prompt_tokens)
                logging.info("completion tokens: %s" % completion_tokens)
                logging.info("total tokens: %s" % total_tokens)
                for openaiKey in self.usable_openai_keys:
                    if openaiKey.get("api_key", None) == open_ai_key:
                        openaiKey["token_limit"] += total_tokens
                logging.info("active threads: %s" % self.__get_active_thread_count())
                self.call_black(response_str, messages, elapsed_time, completion_tokens, prompt_tokens, total_tokens)
            except openai.error.RateLimitError as e:
                logging.error(f"Retrying: {retries}, OpenAI API request exceeded rate limit: {e} api_key: {open_ai_key}")
                self.__release_token(open_ai_key)
                self.retry_on_error(task, ask_content, messages, retries=retries)
            except openai.error.Timeout as e:
                logging.error(f"Retrying: {retries}, OpenAI API request timed out: {e} ")
                self.retry_on_error(task, ask_content, messages, retries=retries)
            except openai.error.APIConnectionError as e:
                logging.error(f"Retrying: {retries}, OpenAI API request timed out, OpenAI API request failed to connect: {e}")
                self.retry_on_error(task, ask_content, messages, retries=retries)
            except openai.error.APIError as e:
                logging.error(f"Retrying: {retries}, OpenAI API returned an API Error: {e}")
                self.retry_on_error(task, ask_content, messages, retries=retries)
        else:
            self.task_queue.put(task)

    def run_tasks(self, tasks):
        self._run_tasks(tasks=tasks, run_func=self.process_task)

    def asyncio_run_gpt_ask(self, prompt, realTime_output=False):
        if len(self.messages) == 0:
            self.messages.append({"role": "system", "content": self.system_content})
        self.messages.append({"role": "user", "content": prompt})
        if self.stream:
            return asyncio.run(self.__ask(realTime_output))[0]
        else:
            start_time = time.time()
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=self.messages,
                temperature=self.temperature
            )
            elapsed_time = time.time() - start_time
            return response['choices'][0]['message']['content'], int(round(elapsed_time, 0))

    async def __ask(self, realTime_output=False):
        return await asyncio.gather(*[self.__generate_text_async(realTime_output)])

    async def __generate_text_async(self, realTime_output) -> tuple:
        response_text_array = []
        response_text = ""
        start_time = time.time()
        async for chunk in await openai.ChatCompletion.acreate(
                model=self.model,
                messages=self.messages,
                temperature=self.temperature,
                top_p=self.top_p,
                presence_penalty=self.presence_penalty,
                frequency_penalty=self.frequency_penalty,
                n=self.n,
                stream=self.stream
        ):
            chunk = chunk['choices'][0]
            if "content" in chunk["delta"]:
                text = chunk["delta"]['content']
                response_text += text
                if text in ["\n"]:
                    response_text_array.append(response_text)
                    if realTime_output:
                        print(response_text)
                    response_text = ""
        elapsed_time = time.time() - start_time
        logging.info(f"{elapsed_time:.2f} seconds to execute")
        return "\n".join(response_text_array), int(round(elapsed_time, 0))
