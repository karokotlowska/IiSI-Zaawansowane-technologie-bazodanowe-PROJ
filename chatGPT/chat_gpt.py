import logging
import threading

import openai
from openai.error import RateLimitError, InvalidRequestError, OpenAIError
from dotenv import load_dotenv
from urllib3.exceptions import ReadTimeoutError

from chatGPT import Prompt
import os
import time

load_dotenv()


class ChatGPT:
    COMPLETION = 'COMPLETION'
    CHAT = 'CHAT'
    KEY = os.getenv("OPENAI_API_KEY")
    GTP_VERSION = 'gpt-3.5-turbo'
    MAX_TOKENS = 2048

    class GPTException(Exception):
        def __init__(self, message):
            self.message = message

    @classmethod
    def ask_gpt(cls, question: str, attempt: int = 0):
        try:
            if cls.KEY is None:
                raise ChatGPT.GPTException("OpenAI API key not found")

            openai.api_key = cls.KEY
            prompt = Prompt(cls.GTP_VERSION, 0.68, cls.MAX_TOKENS, ChatGPT.CHAT, question)
            return cls._create_response(prompt)
        except RateLimitError as e:
            logging.warning(
                f"Thread [{threading.current_thread().name}] Rate limit exceeded, waiting 20 seconds for question {question} and trying again in 3 attempts left {3 - attempt}")
            time.sleep(20)
            if attempt > 3:
                logging.error(
                    f"Thread [{threading.current_thread().name}] Rate limit exceeded for question {question}, tried 3 times, giving up")
                raise ChatGPT.GPTException(e.user_message)
            return cls.ask_gpt(question, attempt + 1)
        except ReadTimeoutError:
            logging.warning(
                f"Thread [{threading.current_thread().name}] Read timeout exceeded, waiting 20 seconds for question {question} and trying again in 3 attempts left {3 - attempt}")
            time.sleep(20)
            if attempt > 3:
                logging.error(
                    f"Thread [{threading.current_thread().name}] Read timeout exceeded for question {question}, tried 3 times, giving up")
                raise ChatGPT.GPTException("Read timeout exceeded")
            return cls.ask_gpt(question, attempt + 1)
        except InvalidRequestError as e:
            logging.error(
                f"Thread [{threading.current_thread().name}] Invalid request for question {question}")
            raise ChatGPT.GPTException(e.user_message)
        except OpenAIError as e:
            logging.error(
                f"Thread [{threading.current_thread().name}] Unexpected error for question {question}")
            raise ChatGPT.GPTException(e.user_message)

    @classmethod
    def _create_response(cls, prompt: Prompt):
        if prompt.type == ChatGPT.COMPLETION:
            return openai.Completion.create(
                engine=prompt.engine,
                prompt=prompt.prompt,
                temperature=prompt.max_temperature,
                max_tokens=prompt.max_tokens,
            )['choices'][0]
        elif prompt.type == ChatGPT.CHAT:
            message = {'role': 'user', 'content': prompt.prompt}
            return openai.ChatCompletion.create(
                model=prompt.engine,
                temperature=prompt.max_temperature,
                max_tokens=prompt.max_tokens,
                messages=[message]
            )['choices'][0]['message']['content']
