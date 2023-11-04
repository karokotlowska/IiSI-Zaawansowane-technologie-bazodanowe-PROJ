import sqlalchemy
from dotenv import load_dotenv
from sqlalchemy import MetaData
from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from graphviz import Digraph
import time
import sys
import threading

from chatGPT import ChatGPT

load_dotenv()

# db_type = input("Enter the database type (e.g., postgresql, mysql): ")
# db_host = input("Enter the database host: ")
# db_port = input("Enter the database port: ")
# db_name = input("Enter the database name: ")
# db_user = input("Enter the database username: ")
# db_password = input("Enter the database password: ")

db_url = f"postgresql://postgres:admin@localhost:5432/shopping_db"
engine = create_engine(db_url)
metadata = MetaData()
metadata.reflect(bind=engine)

print("Number of Tables:", len(metadata.tables))

for table_name in metadata.tables:
    table = metadata.tables[table_name]
    print(f"Table: {table_name}")
    for column in table.columns:
        print(f"Column: {column.name}, Type: {column.type}")

dot = Digraph(comment='Database Schema')
dot.graph_attr['rankdir'] = 'LR'

for table_name in metadata.tables:
    table = metadata.tables[table_name]
    dot.node(table_name, label=table_name, shape='plaintext')

for table_name in metadata.tables:
    table = metadata.tables[table_name]
    for column in table.columns:
        column_name_sanitized = str(column.name).replace(" ", "_")
        label = f"{column.name} (PK)" if column.primary_key else column.name
        dot.node(f'{table_name}_{column_name_sanitized}', label=label)
        dot.edge(table_name, f'{table_name}_{column_name_sanitized}')

for table_name in metadata.tables:
    table = metadata.tables[table_name]
    for fk in table.foreign_key_constraints:
        referred_table = list(fk.elements)[0].column.table.name
        dot.edge(table_name, referred_table, label=f"FK: {', '.join(col.name for col in fk.columns)}")

dot.render('database_schema', format='png', view=True)

#database description to send to chatbot 
def describe_table(table):
    description = f"Table: {table.name}\n"
    foreign_keys = set()

    # Retrieve all foreign keys' columns across the tables
    for t in metadata.tables.values():
        for fk in t.foreign_key_constraints:
            foreign_keys.update(fk.columns)

    for column in table.columns:
        pk_marker = '*' if column.primary_key else ''
        fk_marker = '+' if column in foreign_keys and not column.primary_key else ''
        description += f" - {column.name}: {column.type} {pk_marker}{fk_marker}"

        if column.comment:
            description += f" ({column.comment})"

        description += "\n"
    return description

text_description = ''
comments = ''

for table_name in metadata.tables:
    table = metadata.tables[table_name]
    text_description += describe_table(table) + "\n"
    for column in table.columns:
        if column.comment:
            comments += f"Table: {table.name}, Column: {column.name}, Comment: {column.comment}\n"

with open('database_description.txt', 'w') as file:
    file.write(text_description)
    file.write("\n\nComments:\n")
    file.write(comments)

#KROKI------------------------------database_description_pattern.txt
def describe_table(table):
    description = f"[{table.name}]\n"
    foreign_keys = set()

    for t in metadata.tables.values():
        for fk in t.foreign_key_constraints:
            foreign_keys.update(fk.columns)

    for column in table.columns:
        pk_marker = '*' if column.primary_key else ''
        fk_marker = '+' if column in foreign_keys and not column.primary_key else ''
        description += f"{pk_marker}{fk_marker}{column.name}\n"

    return description

def has_duplicate_values(table_name, column_name):
    with engine.connect() as connection:
        query = f"SELECT {column_name}, COUNT(*) FROM {table_name} GROUP BY {column_name} HAVING COUNT(*) > 1"
        result = connection.execute(query)
        return result.first() is not None

def has_intermediate_table(table_name):
    table = metadata.tables[table_name]
    foreign_key_count = 0

    for constraint in table.constraints:
        if isinstance(constraint, sqlalchemy.ForeignKeyConstraint):
            referred_tables = [list(element.column.table.name for element in constraint.elements)]
            foreign_key_count += len(referred_tables)

    return foreign_key_count > 2

def describe_relationships():
    relationship_description = "\n\n# Relationships (Cardinality Syntax)"
    encountered_relationships = set()

    for table_name in metadata.tables:
        table = metadata.tables[table_name]

        symbol = ""
        has_primary_key = any(column.primary_key for column in table.columns)
        has_foreign_key = any(isinstance(constraint, sqlalchemy.ForeignKeyConstraint) for constraint in table.constraints)
        has_unique_constraint = any(isinstance(constraint, sqlalchemy.UniqueConstraint) for constraint in table.constraints)

        for column in table.columns:
            if column.primary_key:
                column_name = column.name
                has_foreign_key = any(isinstance(constraint, sqlalchemy.ForeignKeyConstraint) for constraint in table.constraints)
                has_duplicate_values1 = has_duplicate_values(table_name, column_name)

                if column.primary_key and has_foreign_key and not has_duplicate_values1:
                    symbol = "1--*"

                if has_foreign_key and not has_duplicate_values1:
                    symbol = "*--1"

        if has_intermediate_table(table_name) and has_foreign_key:
            symbol = "*--*"

        if has_primary_key and has_foreign_key and has_unique_constraint:
            symbol = "1--1"

        for constraint in table.constraints:
            if isinstance(constraint, sqlalchemy.ForeignKeyConstraint):
                referred_table = list(constraint.elements)[0].column.table.name

                combined_relationship = (table_name, symbol, referred_table)

                if combined_relationship not in encountered_relationships and combined_relationship[::-1] not in encountered_relationships:
                    encountered_relationships.add(combined_relationship)
                    relationship_description += f"\n{referred_table} {symbol} {table_name}"

    return relationship_description

text_description = ''
comments = ''
relationship_description = describe_relationships()



for table_name in metadata.tables:
    table = metadata.tables[table_name]
    text_description += describe_table(table) + "\n\n"
    for column in table.columns:
        if column.comment:
            comments += f"Table: {table.name}, Column: {column.name}, Comment: {column.comment}\n"

with open('database_description_pattern.txt', 'w') as file:
    file.write(text_description)
    file.write(relationship_description)

def loading_animation():
    while not event.is_set():
        sys.stdout.write('\r|')
        time.sleep(0.1)
        sys.stdout.write('\r/')
        time.sleep(0.1)
        sys.stdout.write('\r-')
        time.sleep(0.1)
        sys.stdout.write('\r\\')
        time.sleep(0.1)

event = threading.Event()

question = "Wygeneruj opis dla tabeli o takiej strukturze. Opis powinien próbować odgadnąć semantyke oraz relacje pomiędzy tabelami"

chatGPT = ChatGPT()
loading_thread = threading.Thread(target=loading_animation)
loading_thread.start()

response = chatGPT.ask_gpt(f"{question}\n\n{text_description}")

event.set()
loading_thread.join()

print(f"GPT Response: {response}")