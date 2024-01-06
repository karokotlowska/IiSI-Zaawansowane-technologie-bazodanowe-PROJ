import json

from config import output_dir
from description import Query

class MarkdownGenerator:

    @classmethod
    def generate(cls, db_metadata: dict, gpt_descriptions: dict, db_description: str, diagrams: dict, language: Query.Lang):
        markdown = cls._generate_markdown(db_metadata, gpt_descriptions, db_description, diagrams, language)
        cls._save_markdown(markdown)

    @classmethod
    def _generate_markdown(cls, db_metadata: dict, gpt_descriptions: dict, db_description: str, diagrams: dict, language: Query.Lang) -> str:
        markdown = ""
        markdown += cls._generate_database_description(db_metadata, db_description, gpt_descriptions, diagrams, language)
        markdown += cls._generate_tables_description(db_metadata, gpt_descriptions, language)
        markdown += cls._generate_views_description(db_metadata, gpt_descriptions, language)
        markdown += cls._generate_functions_description(db_metadata, gpt_descriptions, language)
        markdown += cls._generate_triggers_description(db_metadata, gpt_descriptions, language)
        return markdown

    @classmethod
    def _insert_svg_files(cls, diagram: str) -> str:
        markdown = ""
        svg_tag = f'<img src="{diagram}" alt="Kroki diagram">\n\n'
        markdown += svg_tag
        return markdown

    @classmethod
    def _generate_database_description(cls, db_metadata: dict, db_description: str, gtp_descriptions: dict,
                                       diagrams: dict, language: Query.Lang) -> str:
        if language == Query.Lang.EN:
            markdown = "# Database description\n\n"
        elif language == Query.Lang.PL:
            markdown = "# Opis bazy danych\n\n"

        markdown += db_description + "\n\n"
        markdown += cls._generate_database_description_content(db_metadata, gtp_descriptions, diagrams, language)
        return markdown

    @classmethod
    def _generate_database_description_content(cls, db_metadata: dict, gpt_descriptions, diagrams: dict, language: Query.Lang) -> str:
        markdown = ""
        for schema in db_metadata:
            schema_descriptions = gpt_descriptions[schema]
            markdown += cls._generate_schema_description(schema, db_metadata[schema], schema_descriptions, language)
            markdown += cls._insert_svg_files(diagrams[schema])
        return markdown

    @classmethod
    def _generate_schema_description(cls, schema: str, schema_metadata: dict, schema_descriptions: dict, language: Query.Lang) -> str:
        markdown = ""
        markdown += cls._generate_schema_name(schema)
        markdown += cls._generate_schema_tables(schema_metadata, schema_descriptions['tables'], language)
        markdown += cls._generate_schema_views(schema_metadata, schema_descriptions['views'], language)
        markdown += cls._generate_schema_functions(schema_metadata, schema_descriptions['functions'], language)
        return markdown

    @classmethod
    def _generate_schema_name(cls, schema: str) -> str:
        markdown = f"## {schema}\n\n"
        return markdown

    @classmethod
    def _generate_schema_tables(cls, schema_metadata: dict, table_descriptions: dict, language: Query.Lang) -> str:
        markdown = ""
        markdown += cls._generate_schema_tables_header(language)
        markdown += cls._generate_schema_tables_content(schema_metadata['tables'], table_descriptions)
        markdown += "\n"
        return markdown

    @classmethod
    def _generate_schema_tables_header(cls, language: Query.Lang) -> str:
        if language == Query.Lang.EN:
            markdown = "| Table name | Description |\n"
        elif language == Query.Lang.PL:
            markdown = "| Nazwa tabeli | Opis |\n"
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
    def _generate_schema_views(cls, schema_metadata: dict, views_descriptions: dict, language: Query.Lang) -> str:
        markdown = ""
        markdown += cls._generate_schema_views_header(language)
        markdown += cls._generate_schema_views_content(schema_metadata['views'], views_descriptions)
        markdown += "\n"
        return markdown

    @classmethod
    def _generate_schema_views_header(cls, language: Query.Lang) -> str:
        if language == Query.Lang.EN:
            markdown = "| View name | Description |\n"
        elif language == Query.Lang.PL:
            markdown = "| Nazwa widoku | Opis |\n"
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
    def _generate_schema_functions(cls, schema_metadata: dict, functions_descriptions: dict, language: Query.Lang) -> str:
        markdown = ""
        markdown += cls._generate_schema_functions_header(language)
        markdown += cls._generate_schema_functions_content(schema_metadata['functions'], functions_descriptions)
        markdown += "\n"
        return markdown

    @classmethod
    def _generate_schema_functions_header(cls, language: Query.Lang) -> str:
        if language == Query.Lang.EN:
            markdown = "| Function name | Description |\n"
        elif language == Query.Lang.PL:
            markdown = "| Nazwa funkcji | Opis |\n"        
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
    def _generate_tables_description(cls, db_metadata: dict, gpt_descriptions: dict, language: Query.Lang) -> str:
        if language == Query.Lang.EN:
            markdown = "# Tables description\n\n"
        elif language == Query.Lang.PL:
            markdown = "# Opis tabel\n\n"
        markdown += cls._generate_tables_description_content(db_metadata, gpt_descriptions, language)
        return markdown
    
    @classmethod
    def _generate_tables_description_content(cls, db_metadata: dict, gpt_descriptions: dict, language: Query.Lang) -> str:
        markdown = ""
        for schema in db_metadata:
            markdown += cls._generate_schema_tables_description(schema, db_metadata[schema], {}, language)
        return markdown

    @classmethod
    def _generate_schema_tables_description(cls, schema: str, schema_metadata: dict, gpt_descriptions: dict, language: Query.Lang) -> str:
        markdown = ""
        markdown += cls._generate_schema_name(schema)
        markdown += cls._generate_schema_tables_description_content(schema_metadata['tables'], language)
        return markdown

    @classmethod
    def _generate_schema_tables_description_content(cls, tables_metadata: list, language: Query.Lang) -> str:
        markdown = ""
        for table_metadata in tables_metadata:
            if language == Query.Lang.EN:
                markdown += f"### Table: *{table_metadata['name']}*\n\n"
            elif language == Query.Lang.PL:
                markdown += f"### Tabela: *{table_metadata['name']}*\n\n"
            
            markdown += cls._generate_table_description_content(table_metadata, language)
        return markdown

    @classmethod
    def _generate_table_description_content(cls, table_metadata: dict, language: Query.Lang) -> str:
        markdown = ""
        markdown += cls._generate_table_description_content_header(language)
        markdown += cls._generate_table_description_content_content(table_metadata)
        markdown += cls._generate_table_indexes_description_content_header(language)
        markdown += cls._generate_table_indexes_description_content_content(table_metadata)
        markdown += cls._generate_table_checks_description_content_header(language)
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
    def _generate_table_description_content_header(cls, language: Query.Lang) -> str:
        if language == Query.Lang.EN:
            markdown = "Structure: \n\n"
            header = "| Column name | Type | Primary key | Foreign key | Unique | Not null | Default | Identity | Autoincrement | Comment |\n"
        elif language == Query.Lang.PL:
            markdown = "Struktura: \n\n"
            header = "| Nazwa kolumny | Typ | Klucz główny | Klucz obcy | Unikalny | Nie null | Domyślna wartość | Tożsamość | Autoinkrementacja | Komentarz |\n"
        
        markdown += header
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
    def _generate_table_indexes_description_content_header(cls, language: Query.Lang) -> str:
        if language == Query.Lang.EN:
            header = "Indexes: \n\n"
            column_headers = "| Index name | Columns |\n"
        elif language == Query.Lang.PL:
            header = "Indeksy: \n\n"
            column_headers = "| Nazwa indeksu | Kolumny |\n"
        markdown = header
        markdown += column_headers
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
    def _generate_table_checks_description_content_header(cls, language: Query.Lang) -> str:
        if language == Query.Lang.EN:
            markdown = "Checks: \n\n"
            header = "| Check name | Expression |\n"
        elif language == Query.Lang.PL:
            markdown = "Sprawdzenia: \n\n"
            header = "| Nazwa sprawdzenia | Wyrażenie |\n"
        
        markdown += header
        markdown += "|------------|------------|\n"
        return markdown

    @classmethod
    def _generate_table_checks_description_content_content(cls, table_metadata: dict) -> str:
        markdown = ""
        for check_metadata in table_metadata.get('checks', []):
            markdown += cls._generate_check_description(check_metadata)
        return markdown

    @classmethod
    def _generate_check_description(cls, check_metadata: dict) -> str:
        check_name = check_metadata.get('name', 'N/A')
        sqltext = check_metadata.get('sqltext', 'N/A')
        markdown = ""
        markdown += f"| {check_name} | {sqltext} |\n"
        return markdown

    @classmethod
    def _generate_views_description(cls, db_metadata: dict, gpt_descriptions: dict, language: Query.Lang) -> str:
        if language == Query.Lang.EN:
            markdown = "# Views description\n\n"
        elif language == Query.Lang.PL:
            markdown = "# Opis widoków\n\n"
        
        markdown += cls._generate_views_description_content(db_metadata, gpt_descriptions, language)
        return markdown

    @classmethod
    def _generate_views_description_content(cls, db_metadata: dict, gpt_descriptions: dict, language: Query.Lang) -> str:
        markdown = ""
        for schema in db_metadata:
            markdown += cls._generate_schema_views_description(schema, db_metadata[schema], {}, language)
        return markdown

    @classmethod
    def _generate_schema_views_description(cls, schema: str, schema_metadata: dict, gpt_descriptions: dict, language: Query.Lang) -> str:
        markdown = ""
        markdown += cls._generate_schema_name(schema)
        content = cls._generate_schema_views_description_content(schema_metadata['views'], gpt_descriptions, language)
        
        if content.strip() == "":
            if language == Query.Lang.EN:
                markdown += "*No views in this schema*\n\n"
            elif language == Query.Lang.PL:
                markdown += "*Brak widoków w tym schemacie*\n\n"
        else:
            markdown += content

        return markdown

    @classmethod
    def _generate_schema_views_description_content(cls, views_metadata: list, gpt_descriptions: dict, language: Query.Lang) -> str:
        markdown = ""
        for view_metadata in views_metadata:
            if language == Query.Lang.EN:
                markdown += f"### View: *{view_metadata['name']}*\n\n"
            elif language == Query.Lang.PL:
                markdown += f"### Widok: *{view_metadata['name']}*\n\n"
            markdown += cls._generate_view_description_content(view_metadata, gpt_descriptions, language)
        return markdown

    @classmethod
    def _generate_view_description_content(cls, view_metadata: dict, gpt_descriptions: dict) -> str:
        markdown = ""
        markdown += cls._generate_view_definition_content(view_metadata)
        markdown += cls._generate_view_columns_content_header()
        markdown += cls._generate_view_columns_content_content(view_metadata)
        return markdown

    @classmethod
    def _generate_view_definition_content(cls, view_metadata: dict, language: Query.Lang) -> str:
        if language == Query.Lang.EN:
            markdown = f"View definition: \n```sql\n\n {view_metadata['definition']} \n\n```\n\n"
        elif language == Query.Lang.PL:
            markdown = f"Definicja widoku: \n```sql\n\n {view_metadata['definition']} \n\n```\n\n"
        return markdown

    @classmethod
    def _generate_view_columns_content_header(cls, language: Query.Lang) -> str:
        if language == Query.Lang.EN:
            markdown = "Structure: \n\n"
            header = "| Column name | Type |\n"
        elif language == Query.Lang.PL:
            markdown = "Struktura: \n\n"
            header = "| Nazwa kolumny | Typ |\n"
        
        markdown += header
        markdown += "| --- | --- |\n"
        return markdown

    @classmethod
    def _generate_view_columns_content_content(cls, view_metadata: dict, language: Query.Lang) -> str:
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
    def _generate_functions_description(cls, db_metadata: dict, gpt_descriptions: dict, language: Query.Lang) -> str:
        if language == Query.Lang.EN:
            markdown = "# Functions description\n\n"
        elif language == Query.Lang.PL:
            markdown = "# Opis funkcji\n\n"
        
        markdown += cls._generate_functions_description_content(db_metadata, gpt_descriptions, language)
        return markdown

    @classmethod
    def _generate_functions_description_content(cls, db_metadata: dict, gpt_descriptions: dict, language: Query.Lang) -> str:
        markdown = ""
        for schema in db_metadata:
            markdown += cls._generate_schema_functions_description(schema, db_metadata[schema], language)
        return markdown

    @classmethod
    def _generate_schema_functions_description(cls, schema: str, schema_metadata: dict, language: Query.Lang) -> str:
        markdown = ""
        markdown += cls._generate_schema_name(schema)
        if len(schema_metadata['functions']) == 0:
            if language == Query.Lang.EN:
                markdown += "*No functions in this schema*\n\n"
            elif language == Query.Lang.PL:
                markdown += "*Brak funkcji w tym schemacie*\n\n"
        else:
            markdown += cls._generate_schema_functions_description_content(schema_metadata['functions'], language)

        return markdown

    @classmethod
    def _generate_schema_functions_description_content(cls, functions_metadata: list, language: Query.Lang) -> str:
        markdown = ""
        for function_metadata in functions_metadata:
            markdown += cls._generate_function_description_content_content(function_metadata, language)
        return markdown

    @classmethod
    def _generate_function_description_content_content(cls, function_metadata: dict, language: Query.Lang) -> str:
        if language == Query.Lang.EN:
            markdown = f"### Function: *{function_metadata['name']}*\n"
        elif language == Query.Lang.PL:
            markdown = f"### Funkcja: *{function_metadata['name']}*\n"
        
        markdown += f"```sql\n{function_metadata['definition']}\n``` \n\n"
        return markdown

    @classmethod
    def _generate_triggers_description(cls, db_metadata: dict, gpt_descriptions: dict, language: Query.Lang) -> str:
        if language == Query.Lang.EN:
            markdown = "# Triggers description\n\n"
        elif language == Query.Lang.PL:
            markdown = "# Opis wyzwalaczy\n\n"
        
        markdown += cls._generate_triggers_description_content(db_metadata, gpt_descriptions, language)
        return markdown

    @classmethod
    def _generate_triggers_description_content(cls, db_metadata: dict, gpt_descriptions: dict, language: Query.Lang) -> str:
        markdown = ""
        for schema in db_metadata:
            markdown += cls._generate_schema_triggers_description(schema, db_metadata[schema], language)
        return markdown

    @classmethod
    def _generate_schema_triggers_description(cls, schema: str, schema_metadata: dict, language: Query.Lang) -> str:
        markdown = ""
        markdown += cls._generate_schema_name(schema)
        if len(schema_metadata['triggers']) == 0:
            if language == Query.Lang.EN:
                markdown += "*No triggers in this schema*\n\n"
            elif language == Query.Lang.PL:
                markdown += "*Brak wyzwalaczy w tym schemacie*\n\n"
        else:
            markdown += cls._generate_schema_triggers_description_content(schema_metadata['triggers'], language)

        return markdown

    @classmethod
    def _generate_schema_triggers_description_content(cls, triggers_metadata: list, language: Query.Lang) -> str:
        markdown = ""
        markdown += cls._generate_schema_triggers_description_content_header(language)
        for trigger_metadata in triggers_metadata:
            markdown += cls._generate_trigger_description_content_content(trigger_metadata)
        return markdown

    @classmethod
    def _generate_schema_triggers_description_content_header(cls, language: Query.Lang) -> str:
        if language == Query.Lang.EN:
            markdown = "| Trigger name | Event | Table | Action | Definition |\n"
        elif language == Query.Lang.PL:
            markdown = "| Nazwa wyzwalacza | Zdarzenie | Tablica | Akcja | Definicja |\n"
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
