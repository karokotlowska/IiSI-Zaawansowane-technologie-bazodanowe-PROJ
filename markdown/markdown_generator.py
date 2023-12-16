import json

from config import output_dir


class MarkdownGenerator:

    @classmethod
    def generate(cls, db_metadata: dict, gpt_descriptions: dict, db_description: str, diagrams: dict):
        markdown = cls._generate_markdown(db_metadata, gpt_descriptions, db_description, diagrams)
        cls._save_markdown(markdown)

    @classmethod
    def _generate_markdown(cls, db_metadata: dict, gpt_descriptions: dict, db_description: str, diagrams: dict) -> str:
        markdown = ""
        markdown += cls._generate_database_description(db_metadata, db_description, gpt_descriptions, diagrams)
        markdown += cls._generate_tables_description(db_metadata, gpt_descriptions)
        markdown += cls._generate_views_description(db_metadata, gpt_descriptions)
        markdown += cls._generate_functions_description(db_metadata, gpt_descriptions)
        markdown += cls._generate_triggers_description(db_metadata, gpt_descriptions)
        return markdown

    @classmethod
    def _insert_svg_files(cls, diagram: str) -> str:
        markdown = ""
        svg_tag = f'<img src="{diagram}" alt="Kroki diagram">\n\n'
        markdown += svg_tag
        return markdown

    @classmethod
    def _generate_database_description(cls, db_metadata: dict, db_description: str, gtp_descriptions: dict,
                                       diagrams: dict) -> str:
        markdown = "# Database description\n\n"
        markdown += db_description + "\n\n"
        markdown += cls._generate_database_description_content(db_metadata, gtp_descriptions, diagrams)
        return markdown

    @classmethod
    def _generate_database_description_content(cls, db_metadata: dict, gpt_descriptions, diagrams: dict) -> str:
        markdown = ""
        for schema in db_metadata:
            schema_descriptions = gpt_descriptions[schema]
            markdown += cls._generate_schema_description(schema, db_metadata[schema], schema_descriptions)
            markdown += cls._insert_svg_files(diagrams[schema])
        return markdown

    @classmethod
    def _generate_schema_description(cls, schema: str, schema_metadata: dict, schema_descriptions: dict) -> str:
        markdown = ""
        markdown += cls._generate_schema_name(schema)
        markdown += cls._generate_schema_tables(schema_metadata, schema_descriptions['tables'])
        markdown += cls._generate_schema_views(schema_metadata, schema_descriptions['views'])
        markdown += cls._generate_schema_functions(schema_metadata, schema_descriptions['functions'])
        return markdown

    @classmethod
    def _generate_schema_name(cls, schema: str) -> str:
        markdown = f"## {schema}\n\n"
        return markdown

    @classmethod
    def _generate_schema_tables(cls, schema_metadata: dict, table_descriptions: dict) -> str:
        markdown = ""
        markdown += cls._generate_schema_tables_header()
        markdown += cls._generate_schema_tables_content(schema_metadata['tables'], table_descriptions)
        markdown += "\n"
        return markdown

    @classmethod
    def _generate_schema_tables_header(cls) -> str:
        markdown = "| Table name | Description |\n"
        markdown += "| --- | --- |\n"
        return markdown

    @classmethod
    def _generate_schema_tables_content(cls, tables_metadata: list, table_descriptions: dict) -> str:
        markdown = ""
        for table_metadata in tables_metadata:
            markdown += cls._generate_table_description(table_metadata, table_descriptions[table_metadata['name']])
        return markdown

    @classmethod
    def _generate_table_description(cls, table_metadata: dict, table_description: str) -> str:
        markdown = ""
        markdown += f"| {table_metadata['name']} | {table_description} |\n"
        return markdown

    @classmethod
    def _generate_schema_views(cls, schema_metadata: dict, views_descriptions: dict) -> str:
        markdown = ""
        markdown += cls._generate_schema_views_header()
        markdown += cls._generate_schema_views_content(schema_metadata['views'], views_descriptions)
        markdown += "\n"
        return markdown

    @classmethod
    def _generate_schema_views_header(cls) -> str:
        markdown = "| View name | Description |\n"
        markdown += "| --- | --- |\n"
        return markdown

    @classmethod
    def _generate_schema_views_content(cls, views_metadata: list, views_descriptions: dict) -> str:
        markdown = ""
        for view_metadata in views_metadata:
            markdown += cls._generate_view_description(view_metadata, views_descriptions[view_metadata['name']])
        return markdown

    @classmethod
    def _generate_view_description(cls, view_metadata: dict, view_description: str) -> str:
        markdown = ""
        markdown += f"| {view_metadata['name']} | {view_description} |\n"
        return markdown

    @classmethod
    def _generate_schema_functions(cls, schema_metadata: dict, functions_descriptions: dict) -> str:
        markdown = ""
        markdown += cls._generate_schema_functions_header()
        markdown += cls._generate_schema_functions_content(schema_metadata['functions'], functions_descriptions)
        markdown += "\n"
        return markdown

    @classmethod
    def _generate_schema_functions_header(cls) -> str:
        markdown = "| Function name | Description |\n"
        markdown += "| --- | --- |\n"
        return markdown

    @classmethod
    def _generate_schema_functions_content(cls, functions_metadata: list, functions_descritpions: dict) -> str:
        markdown = ""
        for function_metadata in functions_metadata:
            markdown += cls._generate_function_description(function_metadata,
                                                           functions_descritpions[function_metadata['name']])
        return markdown

    @classmethod
    def _generate_function_description(cls, function_metadata: dict, function_description: str) -> str:
        markdown = ""
        markdown += f"| {function_metadata['name']} | {function_description}|\n"
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
        return markdown

    @classmethod
    def _generate_table_description_content_content(cls, table_metadata: dict) -> str:
        markdown = ""
        for column_metadata in table_metadata['columns_details']:
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
        markdown += f"| {column_metadata['name']} | {column_metadata['type']} | {column_metadata['primary_key']} | {len(column_metadata['foreign_key']) > 0} | {column_metadata['unique']} | {not column_metadata['nullable']} |{column_metadata['default']} | {json.dumps(column_metadata['identity'])} | {column_metadata['autoincrement']} | {column_metadata['comment']} |\n"
        return (markdown.replace("True", "&check;")
                .replace("False", "&cross;")
                .replace("None", "-")
                .replace("null", "-"))

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
        markdown += f"| {index_metadata['table_name']} | {', '.join(index_metadata['constraints'])} |\n"
        return markdown

    @classmethod
    def _generate_table_checks_description_content_header(cls, table_metadata: dict) -> str:
        print("-----------------\n\n\n")
        print(table_metadata)
        print("n\\nn----------")
        markdown = "Checks: \n\n"
        markdown += "| Check name | Expression |\n"
        markdown += "|------------|------------|\n"

        for check in table_metadata.get('checks', []):
            check_name = check.get('name', 'N/A')
            sqltext = check.get('sqltext', 'N/A')
        
            markdown += f"| {check_name} | {sqltext} |\n"
    
        return markdown

    @classmethod
    def _generate_table_checks_description_content_content(cls, table_metadata: dict) -> str:
        markdown = ""
        # for check_metadata in table_metadata['checks']:
        markdown += cls._generate_check_description(table_metadata['checks'])
        markdown += "\n"
        return markdown

    @classmethod
    def _generate_check_description(cls, check_metadata: dict) -> str:
        markdown = ""
        # markdown += f"| {check_metadata['name']} | {check_metadata['sqltext']} |\n"
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
        with open(output_dir('description.md'), 'w') as f:
            f.write(markdown)
