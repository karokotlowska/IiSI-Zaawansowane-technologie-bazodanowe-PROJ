import sys
import time
import threading

from chatGPT import ChatGPT
from .questions import Query


class DescriptionGenerator:
    gptClient: ChatGPT = ChatGPT()

    queryVersions = {
        Query.Lang.PL: Query.PL,
        Query.Lang.EN: Query.EN
    }

    @classmethod
    def _loading_animation(cls, event: threading.Event):
        while not event.is_set():
            sys.stdout.write('\r|')
            time.sleep(0.1)
            sys.stdout.write('\r/')
            time.sleep(0.1)
            sys.stdout.write('\r-')
            time.sleep(0.1)
            sys.stdout.write('\r\\')
            time.sleep(0.1)

    @classmethod
    def runner(cls, db_details: str, lang: str):
        event = threading.Event()

        loading_thread = threading.Thread(target=cls._loading_animation, args=(event,))
        loading_thread.start()

        try:
            query = cls.queryVersions[lang].builder(db_details)
            response = cls.gptClient.ask_gpt(query)
            event.set()
            loading_thread.join()
            print(f"GPT Response: {response}")
            cls._save_to_file(response)
        except Exception as e:
            event.set()
            loading_thread.join()
            raise e

    @classmethod
    def _save_to_file(cls, content: str):
        with open('database_description_gpt.txt', 'w') as file:
            file.write(content)
