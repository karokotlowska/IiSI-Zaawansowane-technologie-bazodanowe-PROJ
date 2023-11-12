import json


class MarkdownGenerator:

    @classmethod
    def generate(cls, db_metadata: dict, gpt_descriptions: dict):
        markdown = cls._generate_markdown(db_metadata, gpt_descriptions)
        cls._save_markdown(markdown)

    @classmethod
    def _generate_markdown(cls, db_metadata: dict, gpt_descriptions: dict) -> str:
        markdown = ""
        markdown += cls._generate_database_description(db_metadata)
        markdown += cls._generate_tables_description(db_metadata, gpt_descriptions)
        markdown += cls._generate_views_description(db_metadata, gpt_descriptions)
        markdown += cls._generate_functions_description(db_metadata, gpt_descriptions)
        markdown += cls._generate_triggers_description(db_metadata, gpt_descriptions)
        return markdown

    @classmethod
    def _generate_database_description(cls, db_metadata: dict) -> str:
        markdown = "# Database description\n\n"
        markdown += "Miejsce na opis od bota dla całej bazy danych\n\n"
        markdown += cls._generate_database_description_content(db_metadata)
        return markdown

    @classmethod
    def _generate_database_description_content(cls, db_metadata: dict) -> str:
        markdown = ""
        for schema in db_metadata:
            markdown += cls._generate_schema_description(schema, db_metadata[schema])
        return markdown

    @classmethod
    def _generate_schema_description(cls, schema: str, schema_metadata: dict) -> str:
        markdown = ""
        markdown += cls._generate_schema_name(schema)
        markdown += cls._generate_schema_tables(schema_metadata)
        markdown += cls._generate_schema_views(schema_metadata)
        markdown += cls._generate_schema_functions(schema_metadata)
        return markdown

    @classmethod
    def _generate_schema_name(cls, schema: str) -> str:
        markdown = f"## {schema}\n\n"
        return markdown

    @classmethod
    def _generate_schema_tables(cls, schema_metadata: dict) -> str:
        markdown = ""
        markdown += cls._generate_schema_tables_header()
        markdown += cls._generate_schema_tables_content(schema_metadata['tables'])
        markdown += "\n"
        return markdown

    @classmethod
    def _generate_schema_tables_header(cls) -> str:
        markdown = "| Table name | Description |\n"
        markdown += "| --- | --- |\n"
        return markdown

    @classmethod
    def _generate_schema_tables_content(cls, tables_metadata: list) -> str:
        markdown = ""
        for table_metadata in tables_metadata:
            markdown += cls._generate_table_description(table_metadata)
        return markdown

    @classmethod
    def _generate_table_description(cls, table_metadata: dict) -> str:
        markdown = ""
        markdown += f"| {table_metadata['name']} | Miejsce na opis bota |\n"
        return markdown

    @classmethod
    def _generate_schema_views(cls, schema_metadata: dict) -> str:
        markdown = ""
        markdown += cls._generate_schema_views_header()
        markdown += cls._generate_schema_views_content(schema_metadata['views'])
        markdown += "\n"
        return markdown

    @classmethod
    def _generate_schema_views_header(cls) -> str:
        markdown = "| View name | Description |\n"
        markdown += "| --- | --- |\n"
        return markdown

    @classmethod
    def _generate_schema_views_content(cls, views_metadata: list) -> str:
        markdown = ""
        for view_metadata in views_metadata:
            markdown += cls._generate_view_description(view_metadata)
        return markdown

    @classmethod
    def _generate_view_description(cls, view_metadata: dict) -> str:
        markdown = ""
        markdown += f"| {view_metadata['name']} | Miejsce na opis bota |\n"
        return markdown

    @classmethod
    def _generate_schema_functions(cls, schema_metadata: dict) -> str:
        markdown = ""
        markdown += cls._generate_schema_functions_header()
        markdown += cls._generate_schema_functions_content(schema_metadata['functions'])
        markdown += "\n"
        return markdown

    @classmethod
    def _generate_schema_functions_header(cls) -> str:
        markdown = "| Function name | Description |\n"
        markdown += "| --- | --- |\n"
        return markdown

    @classmethod
    def _generate_schema_functions_content(cls, functions_metadata: list) -> str:
        markdown = ""
        for function_metadata in functions_metadata:
            markdown += cls._generate_function_description(function_metadata)
        return markdown

    @classmethod
    def _generate_function_description(cls, function_metadata: dict) -> str:
        markdown = ""
        markdown += f"| {function_metadata['name']} | Miejsce na opis bota |\n"
        return markdown

    @classmethod
    def _generate_tables_description(cls, db_metadata: dict, gpt_descriptions: dict) -> str:
        markdown = "# Tables description\n\n"
        markdown += cls._generate_tables_description_content(db_metadata, gpt_descriptions)
        return markdown

    @classmethod
    def _generate_tables_description_content(cls, db_metadata: dict, gpt_descriptions: dict) -> str:
        markdown = ""
        for schema in db_metadata:
            markdown += cls._generate_schema_tables_description(schema, db_metadata[schema], {})
        return markdown

    @classmethod
    def _generate_schema_tables_description(cls, schema: str, schema_metadata: dict, gpt_descriptions: dict) -> str:
        markdown = ""
        markdown += cls._generate_schema_name(schema)
        markdown += cls._generate_schema_tables_description_content(schema_metadata['tables'])
        return markdown

    @classmethod
    def _generate_schema_tables_description_content(cls, tables_metadata: list) -> str:
        markdown = ""
        for table_metadata in tables_metadata:
            markdown += "### Table: *" + table_metadata['name'] + "*\n\n"
            markdown += cls._generate_table_description_content(table_metadata)
        return markdown

    @classmethod
    def _generate_table_description_content(cls, table_metadata: dict) -> str:
        markdown = ""
        markdown += cls._generate_table_description_content_header()
        markdown += cls._generate_table_description_content_content(table_metadata)
        markdown += cls._generate_table_indexes_description_content_header()
        markdown += cls._generate_table_indexes_description_content_content(table_metadata)
        markdown += cls._generate_table_checks_description_content_header(table_metadata)
        markdown += cls._generate_table_checks_description_content_content(table_metadata)
        # markdown += cls._generate_table_unique_constraints_description_content_header()
        # markdown += cls._generate_table_unique_constraints_description_content_content(table_metadata)
        return markdown

    @classmethod
    def _generate_table_description_content_content(cls, table_metadata: dict) -> str:
        markdown = ""
        for column_metadata in table_metadata['columns']:
            markdown += cls._generate_column_description(column_metadata)
        markdown += "\n"
        return markdown

    @classmethod
    def _generate_table_description_content_header(cls) -> str:
        markdown = "Structure: \n\n"
        markdown += "| Column name | Type | Primary key | Foreign key | Unique | Not null | Default | Identity | Autoincrement | Comment |\n"
        markdown += "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | \n"
        return markdown

    @classmethod
    def _generate_column_description(cls, column_metadata: dict) -> str:
        markdown = ""
        markdown += f"| {column_metadata['name']} | {column_metadata['type']} | {column_metadata['primary_key']} | {column_metadata['foreign_key']} | {column_metadata['unique']} | {not column_metadata['nullable']} |{column_metadata['default']} | {json.dumps(column_metadata['identity'])} | {column_metadata['autoincrement']} | {column_metadata['comment']}\n"
        return markdown

    @classmethod
    def _generate_table_indexes_description_content_header(cls) -> str:
        markdown = "Indexes: \n\n"
        markdown += "| Index name | Columns |\n"
        markdown += "| --- | --- |\n"
        return markdown

    @classmethod
    def _generate_table_indexes_description_content_content(cls, table_metadata: dict) -> str:
        markdown = ""
        for index_metadata in table_metadata['indexes']:
            markdown += cls._generate_index_description(index_metadata)
        markdown += "\n"
        return markdown

    @classmethod
    def _generate_index_description(cls, index_metadata: dict) -> str:
        markdown = ""
        markdown += f"| {index_metadata['name']} | {', '.join(index_metadata['columns'])} |\n"
        return markdown

    @classmethod
    def _generate_table_checks_description_content_header(cls, table_metadata: dict) -> str:
        markdown = "Checks: \n\n"
        markdown += "| Check name | Expression |\n"
        markdown += "| --- | --- |\n"
        return markdown

    @classmethod
    def _generate_table_checks_description_content_content(cls, table_metadata: dict) -> str:
        markdown = ""
        for check_metadata in table_metadata['checks']:
            markdown += cls._generate_check_description(check_metadata)
        markdown += "\n"
        return markdown

    @classmethod
    def _generate_check_description(cls, check_metadata: dict) -> str:
        markdown = ""
        markdown += f"| {check_metadata['name']} | {check_metadata['sqltext']} |\n"
        return markdown

    @classmethod
    def _generate_table_unique_constraints_description_content_header(cls) -> str:
        markdown = "| Unique constraint name | Columns |\n"
        markdown += "| --- | --- |\n"
        return markdown

    @classmethod
    def _generate_table_unique_constraints_description_content_content(cls, table_metadata: dict) -> str:
        markdown = ""
        for unique_constraint_metadata in table_metadata['unique_constraints']:
            markdown += cls._generate_unique_constraint_description(unique_constraint_metadata)
        return markdown

    @classmethod
    def _generate_unique_constraint_description(cls, unique_constraint_metadata: dict) -> str:
        markdown = ""
        print(unique_constraint_metadata)
        markdown += f"| {unique_constraint_metadata['name']} | {', '.join(unique_constraint_metadata['columns'])} |\n"
        return markdown

    @classmethod
    def _generate_views_description(cls, db_metadata: dict, gpt_descriptions: dict) -> str:
        markdown = "# Views description\n\n"
        markdown += cls._generate_views_description_content(db_metadata, gpt_descriptions)
        return markdown

    @classmethod
    def _generate_views_description_content(cls, db_metadata: dict, gpt_descriptions: dict) -> str:
        markdown = ""
        for schema in db_metadata:
            markdown += cls._generate_schema_views_description(schema, db_metadata[schema], {})
        return markdown

    @classmethod
    def _generate_schema_views_description(cls, schema: str, schema_metadata: dict, gpt_descriptions: dict) -> str:
        markdown = ""
        markdown += cls._generate_schema_name(schema)
        content = cls._generate_schema_views_description_content(schema_metadata['views'], gpt_descriptions)
        markdown += content if content.strip() != "" else "*No views in this schema*\n\n"
        return markdown

    @classmethod
    def _generate_schema_views_description_content(cls, views_metadata: list, gpt_descriptions: dict) -> str:
        markdown = ""
        for view_metadata in views_metadata:
            markdown += "### View: *" + view_metadata['name'] + "*\n\n"
            markdown += cls._generate_view_description_content(view_metadata, gpt_descriptions)
        return markdown

    @classmethod
    def _generate_view_description_content(cls, view_metadata: dict, gpt_descriptions: dict) -> str:
        markdown = ""
        markdown += cls._generate_view_definition_content(view_metadata)
        markdown += cls._generate_view_columns_content_header()
        markdown += cls._generate_view_columns_content_content(view_metadata)
        return markdown

    @classmethod
    def _generate_view_definition_content(cls, view_metadata: dict) -> str:
        markdown = ""
        markdown += f"View definition: \n```sql\n\n {view_metadata['definition']} \n\n```\n\n"
        return markdown

    @classmethod
    def _generate_view_columns_content_header(cls) -> str:
        markdown = "Structure: \n\n"
        markdown += "| Column name | Type |\n"
        markdown += "| --- | --- |\n"
        return markdown

    @classmethod
    def _generate_view_columns_content_content(cls, view_metadata: dict) -> str:
        markdown = ""
        for column_metadata in view_metadata['columns']:
            markdown += cls._generate_view_column_description(column_metadata)
        return markdown

    @classmethod
    def _generate_view_column_description(cls, column_metadata: dict) -> str:
        markdown = ""
        markdown += f"| {column_metadata['name']} | {column_metadata['type']} |\n"
        return markdown

    @classmethod
    def _generate_functions_description(cls, db_metadata: dict, gpt_descriptions: dict) -> str:
        markdown = "# Functions description\n\n"
        markdown += cls._generate_functions_description_content(db_metadata, gpt_descriptions)
        return markdown

    @classmethod
    def _generate_functions_description_content(cls, db_metadata: dict, gpt_descriptions: dict) -> str:
        markdown = ""
        for schema in db_metadata:
            markdown += cls._generate_schema_functions_description(schema, db_metadata[schema])
        return markdown

    @classmethod
    def _generate_schema_functions_description(cls, schema: str, schema_metadata: dict) -> str:
        markdown = ""
        markdown += cls._generate_schema_name(schema)
        if len(schema_metadata['functions']) == 0:
            markdown += "*No functions in this schema*\n\n"
        else:
            markdown += cls._generate_schema_functions_description_content(schema_metadata['functions'])

        return markdown

    @classmethod
    def _generate_schema_functions_description_content(cls, functions_metadata: list) -> str:
        markdown = ""
        for function_metadata in functions_metadata:
            markdown += cls._generate_function_description_content_content(function_metadata)
        return markdown

    @classmethod
    def _generate_function_description_content_content(cls, function_metadata: dict) -> str:
        markdown = f"### Function: *{function_metadata['name']}*\n"
        markdown += f"```sql\n{function_metadata['definition']}\n``` \n\n"
        return markdown

    @classmethod
    def _generate_triggers_description(cls, db_metadata: dict, gpt_descriptions: dict) -> str:
        markdown = "# Triggers description\n\n"
        markdown += cls._generate_triggers_description_content(db_metadata, gpt_descriptions)
        return markdown

    @classmethod
    def _generate_triggers_description_content(cls, db_metadata: dict, gpt_descriptions: dict) -> str:
        markdown = ""
        for schema in db_metadata:
            markdown += cls._generate_schema_triggers_description(schema, db_metadata[schema])
        return markdown

    @classmethod
    def _generate_schema_triggers_description(cls, schema: str, schema_metadata: dict) -> str:
        markdown = ""
        markdown += cls._generate_schema_name(schema)
        if len(schema_metadata['triggers']) == 0:
            markdown += "*No triggers in this schema*\n\n"
        else:
            markdown += cls._generate_schema_triggers_description_content(schema_metadata['triggers'])
        return markdown

    @classmethod
    def _generate_schema_triggers_description_content(cls, triggers_metadata: list) -> str:
        markdown = ""
        markdown += cls._generate_schema_triggers_description_content_header()
        for trigger_metadata in triggers_metadata:
            markdown += cls._generate_trigger_description_content_content(trigger_metadata)
        return markdown

    @classmethod
    def _generate_schema_triggers_description_content_header(cls) -> str:
        markdown = "| Trigger name | Event | Table | Action | Definition |\n"
        markdown += "| --- | --- | --- | --- | --- |\n"
        return markdown

    @classmethod
    def _generate_trigger_description_content_content(cls, trigger_metadata: dict) -> str:
        markdown = ""
        markdown += f"| {trigger_metadata['name']} | {trigger_metadata['event']} | {trigger_metadata['table']} | {trigger_metadata['action']} | ` {trigger_metadata['definition']}` |\n"
        return markdown

    @classmethod
    def _save_markdown(cls, markdown: str):
        with open('description.md', 'w') as f:
            f.write(markdown)
