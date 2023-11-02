# from enum import StrEnum


class Prompt:

    def __init__(self, engine, temperature, max_tokens, type, prompt):
        self._engine = engine
        self._max_temperature = temperature
        self._max_tokens = max_tokens
        self._prompt = prompt
        self._type = type

    @property
    def type(self):
        return self._type

    @property
    def prompt(self):
        return self._prompt

    @property
    def max_tokens(self):
        return self._max_tokens

    @property
    def max_temperature(self):
        return self._max_temperature

    @property
    def engine(self):
        return self._engine


# class PromptEnum(StrEnum):
#     COMPLETION = 'completion'
#     CHAT = 'chat'
