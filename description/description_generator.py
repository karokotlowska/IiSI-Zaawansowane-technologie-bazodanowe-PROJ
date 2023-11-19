import json
import sys
import time
import threading
from typing import List

from chatGPT import ChatGPT
from .error import Error
from .questions import Query
import logging


class DescriptionGenerator:
    gptClient: ChatGPT = ChatGPT()
    errors: List[Error] = []

    tablesQueryVersions = {
        Query.Lang.PL: Query.TABLES_PL,
        Query.Lang.EN: Query.TABLES_EN
    }

    viewsQueryVersions = {
        Query.Lang.PL: Query.VIEWS_PL,
        Query.Lang.EN: Query.VIEWS_EN
    }

    databaseQueryVersions = {
        Query.Lang.PL: Query.DATABASE_PL,
        Query.Lang.EN: Query.DATABASE_PL
    }

    functionsQueryVersions = {
        Query.Lang.PL: Query.FUNCTIONS_PL,
        Query.Lang.EN: Query.FUNCTIONS_PL
    }

    tables_response = {}
    views_response = {}
    functions_response = {}

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
    def runner(cls, tables: list, views: list, functions: list, lang: Query.Lang) -> dict:

        # event = threading.Event()
        # loading_thread = threading.Thread(target=cls._loading_animation, args=(event,))
        # loading_thread.start()

        try:
            #
            tables_thread = threading.Thread(target=cls._generate_tables_description, args=(tables, lang))
            views_thread = threading.Thread(target=cls._generate_views_description, args=(views, lang))
            functions_thread = threading.Thread(target=cls._generate_functions_description, args=(functions, lang))

            tables_thread.start()
            views_thread.start()
            functions_thread.start()

            tables_thread.join()
            views_thread.join()
            functions_thread.join()

            if len(cls.errors) > 0:
                logging.error(f"Aborting system...Error while generating description {cls.errors}")
                raise Exception("Error while generating description")

            # event.set()
            # loading_thread.join()
            return {"tables": cls.tables_response, "views": cls.views_response, "functions": cls.functions_response}
        except Exception as e:
            # event.set()
            # loading_thread.join()
            raise e

    @classmethod
    def _generate_views_description(cls, views: list, lang: Query.Lang) -> dict:
        # TODO use json.dumps instead of str

        if len(views) == 0:
            cls.views_response = {}
            return

        query = cls.viewsQueryVersions[lang].builder(str(views))
        logging.info(
            f"Thread: [{threading.current_thread().name}] Starting generating views description with GPT query: {query}")
        response = cls.gptClient.ask_gpt(query)
        logging.info(
            f"Thread: [{threading.current_thread().name}] Finished generating views description. Successfully got "
            f"response: {response}")
        try:
            cls.views_response = json.loads(response)
        except Exception as e:
            logging.error(f"Thread: [{threading.current_thread().name}] Error occurred while generating views "
                          f"description {e}")
            cls.errors.append(Error(str(e), "generate_views_description", threading.current_thread().name))
            raise Exception(e)

    @classmethod
    def _generate_tables_description(cls, tables: list, lang: Query.Lang) -> dict:
        # TODO use json.dumps instead of str

        if len(tables) == 0:
            cls.tables_response = {}

        query = cls.tablesQueryVersions[lang].builder(str(tables))
        logging.info(
            f"Thread: [{threading.current_thread().name}] Starting generating tables description with GPT query: {query}")
        response = cls.gptClient.ask_gpt(query)
        logging.info(
            f"Thread: [{threading.current_thread().name}] Finished generating tables description. Successfully got "
            f"response: {response}")

        try:
            cls.tables_response = json.loads(response)
        except Exception as e:
            logging.error(f"Thread: [{threading.current_thread().name}] Error occurred while generating tables "
                          f"description {e}")
            cls.errors.append(Error(str(e), "generate_tables_description", threading.current_thread().name))
            raise Exception(e)

    @classmethod
    def _generate_functions_description(cls, functions: list, lang: Query.Lang) -> dict:
        # TODO use json.dumps instead of str

        if len(functions) == 0:
            cls.functions_response = {}
            return

        query = cls.functionsQueryVersions[lang].builder(str(functions))
        logging.info(
            f"Thread: [{threading.current_thread().name}] Starting generating functions description with GPT query: {query}")
        response = cls.gptClient.ask_gpt(query)
        logging.info(
            f"Thread: [{threading.current_thread().name}] Finished generating functions description. Successfully got "
            f"response: {response}")

        try:
            cls.functions_response = json.loads(response)
        except Exception as e:
            logging.error(f"Thread: [{threading.current_thread().name}] Error occurred while generating functions "
                          f"description {e}")
            cls.errors.append(Error(str(e), "generate_functions_description", threading.current_thread().name))
            raise Exception(e)

    @classmethod
    def generate_database_description(cls, db: dict, lang: Query.Lang) -> str:
        # TODO use json.dumps instead of str
        query = cls.databaseQueryVersions[lang].builder(str(db))
        logging.info(
            f"Thread: [{threading.current_thread().name}] Starting generating database description with GPT query: {query}")
        response = cls.gptClient.ask_gpt(query)
        dict_response = json.loads(response)
        logging.info(f"Thread: [{threading.current_thread().name}] Finished generating database description. "
                     f"Successfully got response: {response}")
        if 'database' not in dict_response:
            logging.error(
                f"Thread: [{threading.current_thread().name}] GPT response for database description returned in "
                f"invalid format {dict_response}")
            raise Exception("Invalid GPT response")
        return dict_response['database']

    @classmethod
    def _save_to_file(cls, content: str):
        with open('database_description_gpt.txt', 'w') as file:
            file.write(content)
