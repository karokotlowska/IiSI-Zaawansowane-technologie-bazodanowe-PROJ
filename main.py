import sqlalchemy
from sqlalchemy import MetaData
from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from graphviz import Digraph

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


def describe_table(table):
    description = f"Table: {table.name}\n"
    for column in table.columns:
        description += f" - {column.name}: {column.type}"
        if column.comment:
            description += f" ({column.comment})"
        description += "\n"
    return description

text_description = ''
for table_name in metadata.tables:
    table = metadata.tables[table_name]
    text_description += describe_table(table) + "\n"

with open('database_description.txt', 'w') as file:
    file.write(text_description)
