import copy

from kroki.kroki import process_kroki_files
from database import Database
from markdown import MarkdownGenerator
from description import DescriptionGenerator, Query
from multiprocessing.pool import ThreadPool


class Context:

    @staticmethod
    def run(db_url: str, lang: Query.Lang):
        db = Database()
        db.connect(db_url)
        db.generate_data_for_kroki()
        db.visualize()
        process_kroki_files()
        db_metadata = db.get_database_metadata()

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
            # We don't want to send the whole metadata to GPT
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
        db_description = async_db_description.get()
        MarkdownGenerator.generate(db_metadata, gpt_responses, db_description, diagrams, lang)
