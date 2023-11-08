import openai
from dotenv import load_dotenv

from chatGPT import Prompt
import os

load_dotenv()


class ChatGPT:
    COMPLETION = 'COMPLETION'
    CHAT = 'CHAT'

    def __init__(self):
        self.key = os.getenv("OPENAI_API_KEY")

    def ask_gpt(self, question: str):
        openai.api_key = self.key
        prompt = Prompt("gpt-3.5-turbo", 0.6, 2048, ChatGPT.CHAT, question)
        return self._create_response(prompt)

    def _create_response(self, prompt: Prompt):
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
