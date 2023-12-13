import copy

from dotenv import load_dotenv

from kroki.kroki import process_kroki_files
from database import Database
from config import delete_tmp_dir, delete_output_dir
from markdown import MarkdownGenerator
from menu import Menu
from description import DescriptionGenerator, Query
import logging
from multiprocessing.pool import ThreadPool


def run(db_url: str, lang: Query.Lang, dump_command):
    db = Database(dump_command)
    db.connect(db_url)
    db.generate_data_for_kroki()
    # db.generate_data_for_digraph()

    db.visualize()

    process_kroki_files()
    # db.create_description_for_kroki('description_for_kroki.txt')
    db_metadata = db.get_database_metadata()
    # pprint.pprint(db_metadata)
    # print(db_metadata.values())

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
    diagrams = {}
    counter = 1
    for schema in db_metadata:
        # We don't want to send the whole metadata to GPT-3
        tables = db_metadata[schema]['tables']
        modified_tables = []
        for table in tables:
            modified_table = copy.deepcopy(table)
            del modified_table['columns_details']
            del modified_table['checks']
            del modified_table['indexes']
            modified_tables.append(modified_table)

        views = db_metadata[schema]['views']
        functions = db_metadata[schema]['functions']
        gpt_responses[schema] = DescriptionGenerator.runner(modified_tables, views, functions, lang)
        diagrams[schema] = f"description_for_kroki{counter}_diagram.svg"
        counter += 1
    print(gpt_responses)
    db_description = async_db_description.get()
    MarkdownGenerator.generate(db_metadata, gpt_responses, db_description, diagrams)


if __name__ == '__main__':
    load_dotenv()
    logging.basicConfig()
    logging.root.setLevel(logging.NOTSET)
    logging.basicConfig(level=logging.NOTSET)

    try:
        delete_output_dir()
        menu = Menu()
        menu.run(run)
    except Exception as e:
        raise e
    finally:
        delete_tmp_dir()
