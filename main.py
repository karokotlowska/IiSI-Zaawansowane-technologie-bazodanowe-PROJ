import json

from dotenv import load_dotenv

import pprint
from Kroki.kroki import get_diagram_svg, convert_svg_to_png, save_svg_diagram, process_kroki_files
from Database import Database
from markdown import MarkdownGenerator
from menu import Menu
from description import DescriptionGenerator, Query
import logging
from multiprocessing.pool import ThreadPool


def run(db_url: str, lang: Query.Lang):
    db = Database()
    db.connect(db_url)
    db.generate_data_for_kroki()

    process_kroki_files()
    # db.create_description_for_kroki('description_for_kroki.txt')
    db_metadata = db.get_database_metadata()
    # pprint.pprint(db_metadata)
    print(db_metadata.values())

    schemas_structure = {}
    for schema_name, schema_data in db_metadata.items():
        schema_structure = {
            'tables': [table['name'] for table in schema_data.get('tables', [])],
            'views': [view['name'] for view in schema_data.get('views', [])],
            'functions': [func['name'] for func in schema_data.get('functions', [])],
            'indexes': [],  # Include indexes if available
            'triggers': [trigger['name'] for trigger in schema_data.get('triggers', [])]
        }
        schemas_structure[schema_name] = schema_structure

    pool = ThreadPool(processes=1)

    async_db_description = pool.apply_async(DescriptionGenerator.generate_database_description,
                                            (schemas_structure, lang))

    gpt_responses = {}
    for schema in db_metadata:
        tables = db_metadata[schema]['tables']
        views = db_metadata[schema]['views']
        functions = db_metadata[schema]['functions']
        gpt_responses[schema] = DescriptionGenerator.runner(tables, views, functions, lang)

    print(gpt_responses)
    db_description = async_db_description.get()
    MarkdownGenerator.generate(db_metadata, gpt_responses, db_description)


if __name__ == '__main__':
    load_dotenv()
    logging.basicConfig()
    logging.root.setLevel(logging.NOTSET)
    logging.basicConfig(level=logging.NOTSET)

    menu = Menu()
    menu.run(run)
