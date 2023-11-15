import json

from dotenv import load_dotenv

import pprint
from Kroki.kroki import get_diagram_svg, convert_svg_to_png, save_svg_diagram, process_kroki_files
from Database import Database
from markdown import MarkdownGenerator
from menu import Menu
from description import DescriptionGenerator, Query
import logging


def run(db_url: str, lang: Query.Lang):
    db = Database()
    db.connect(db_url)
    db.generate_data_for_kroki()
    # db.create_description_for_kroki('description_for_kroki.txt')
    db_metadata = db.get_database_metadata()
    # pprint.pprint(db_metadata)

    process_kroki_files()



    # gpt_responses = {}
    # for schema in db_metadata:
    #     tables = db_metadata[schema]['tables']
    #     views = db_metadata[schema]['views']
    #     gpt_responses[schema] = DescriptionGenerator.runner(db_metadata[schema], views, lang)

    # print(gpt_responses)
    MarkdownGenerator.generate(db_metadata, {})


if __name__ == '__main__':

    load_dotenv()
    logging.basicConfig()
    logging.root.setLevel(logging.NOTSET)
    logging.basicConfig(level=logging.NOTSET)

    menu = Menu()
    menu.run(run)
