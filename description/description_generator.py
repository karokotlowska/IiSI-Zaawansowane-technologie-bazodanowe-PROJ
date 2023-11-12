import json
import sys
import time
import threading

from chatGPT import ChatGPT
from .questions import Query
import logging


class DescriptionGenerator:
    gptClient: ChatGPT = ChatGPT()

    tablesQueryVersions = {
        Query.Lang.PL: Query.TABLES_PL,
        Query.Lang.EN: Query.TABLES_EN
    }

    viewsQueryVersions = {
        Query.Lang.PL: Query.VIEWS_PL,
        Query.Lang.EN: Query.VIEWS_EN
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
    def runner(cls, tables: dict, views: list, lang: Query.Lang) -> dict:

        event = threading.Event()
        loading_thread = threading.Thread(target=cls._loading_animation, args=(event,))
        loading_thread.start()

        try:
            tables_response = cls._generate_tables_description(tables, lang)
            # views_response = cls._generate_views_description(views, lang)
            event.set()
            loading_thread.join()
            return {"tables": tables_response}
        except Exception as e:
            event.set()
            loading_thread.join()
            raise e

    @classmethod
    def _generate_views_description(cls, views: list, lang: Query.Lang) -> dict:
        # TODO use json.dumps instead of str
        query = cls.viewsQueryVersions[lang].builder(str(views))
        logging.info(f"Starting generating views description with GPT query: {query}")
        response = cls.gptClient.ask_gpt(query)
        logging.info(f"Finished generating views description. Successfully got response: {response}")
        return response

    @classmethod
    def _generate_tables_description(cls, tables: list, lang: Query.Lang) -> dict:
        # TODO use json.dumps instead of str
        query = cls.tablesQueryVersions[lang].builder(str(tables))
        logging.info(f"Starting generating tables description with GPT query: {query}")
        response = cls.gptClient.ask_gpt(query)
        logging.info(f"Finished generating tables description. Successfully got response: {response}")
        return response

    @classmethod
    def _save_to_file(cls, content: str):
        with open('database_description_gpt.txt', 'w') as file:
            file.write(content)
