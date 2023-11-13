from sqlalchemy import MetaData, PrimaryKeyConstraint, UniqueConstraint, ForeignKeyConstraint, text
from sqlalchemy.engine import create_engine, Engine
from sqlalchemy import inspect
from sqlalchemy.dialects.postgresql.base import PGInspector
import logging


class Database:
    metadata: MetaData
    inspector: PGInspector
    engine: Engine
    tables: list
    view_names: list
    db_url: str

    SCHEMAS_TO_IGNORE = ['information_schema', 'pg_catalog', 'pg_toast', 'pg_temp_1', 'pg_toast_temp_1', 'pg_catalog']

    def __init__(self):
        self.tables = []
        self.view_names = []
        self.db_url = ''

    def connect(self, db_url):
        self.db_url = db_url
        engine = create_engine(self.db_url)
        self.engine = engine
        metadata = MetaData()
        metadata.reflect(bind=engine)
        self.metadata = metadata
        self.inspector = inspect(engine)
        self.tables = metadata.tables

    def get_database_metadata(self) -> dict:

        schemas = [schema for schema in self.inspector.get_schema_names() if schema not in self.SCHEMAS_TO_IGNORE]
        db = {}
        for schema in schemas:
            self.metadata.reflect(bind=self.engine, schema=schema)
            tables = self.get_tables(schema)
            views = self.get_views(schema)
            functions = self.get_functions(schema)
            triggers = self.get_triggers(schema)
            db[schema] = {"tables": tables, "views": views, "functions": functions, "triggers": triggers}
        return db

    def get_views(self, schema: str) -> list:
        views = []
        view_names = self.inspector.get_view_names(schema=schema)
        for view_name in view_names:
            views.append({
                "name": view_name,
                "definition": self.inspector.get_view_definition(view_name),
                "columns": self.inspector.get_columns(view_name)
            })
        return views

    def get_tables(self, schema: str) -> list:
        tables = []
        table_names = self.inspector.get_table_names(schema=schema)
        for table_name in table_names:
            table = self.metadata.tables[schema + "." + table_name]
            parsed_table = self.describe_table(table)
            parsed_table["checks"] = self.inspector.get_check_constraints(table_name, schema=schema)
            tables.append(parsed_table)
        return tables

    def get_functions(self, schema: str) -> list:
        with self.engine.connect() as connection:
            result = connection.execute(text(
                f"SELECT * FROM information_schema.routines WHERE routine_type='FUNCTION' AND specific_schema = '{schema}';"))
            functions = result.fetchall()

        return [{
            "name": function['routine_name'],
            "definition": function['routine_definition']
        } for function in functions]

    def get_triggers(self, schema: str) -> list:
        with self.engine.connect() as connection:
            result = connection.execute(text(
                f"SELECT * FROM information_schema.triggers WHERE  trigger_schema = '{schema}';"))
            triggers = result.fetchall()

        return [{
            "name": trigger['trigger_name'],
            "event": trigger['event_manipulation'],
            "table": trigger['event_object_table'],
            "action": f"{trigger['action_timing']} {trigger['action_orientation']}",
            "definition": trigger['action_statement']
        } for trigger in triggers]

    def describe_table(self, table) -> dict:
        logging.info(f"Fetching metadata for table: {table.name}")

        foreign_keys = []
        unique_constraints = []
        primary_keys = []
        indexes = []

        for c in table.constraints:
            if isinstance(c, ForeignKeyConstraint):
                foreign_keys = list(map(lambda col: col.name, c.columns))
            elif isinstance(c, UniqueConstraint):
                unique_constraints = list(map(lambda col: col.name, c.columns))
            elif isinstance(c, PrimaryKeyConstraint):
                primary_keys = list(map(lambda col: col.name, c.columns))

        for index in table.indexes:
            indexes.append({"name": index.name, "columns": list(map(lambda col: col.name, index.columns))})

        columns = [{"name": column.name,
                    "type": column.type,
                    "primary_key": column.primary_key,
                    "foreign_key": column in foreign_keys and not column.primary_key,
                    "comment": column.comment,
                    "default": column.default,
                    "nullable": column.nullable,
                    "unique": column.unique,
                    "autoincrement": column.autoincrement,
                    "identity": {
                        "start": column.identity.start,
                        "increment": column.identity.increment,
                        "minvalue": column.identity.minvalue,
                        "maxvalue": column.identity.maxvalue,
                    } if column.identity is not None else None
                    } for column in table.columns]

        return {
            "name": table.name,
            "comment": table.comment,
            "columns": columns,
            "primary_keys": primary_keys,
            "foreign_keys": foreign_keys,
            "unique_constraints": unique_constraints,
            "indexes": indexes,
            "checks": []
        }

        # #KROKI
    def describe_kroki_table(self, table):
        description = f"[{table.name}]\n"
        foreign_keys = set()

        for t in self.metadata.tables.values():
            for fk in t.foreign_key_constraints:
                foreign_keys.update(fk.columns)

        for column in table.columns:
            pk_marker = '*' if column.primary_key else ''
            fk_marker = '+' if column in foreign_keys and not column.primary_key else ''
            description += f"{pk_marker}{fk_marker}{column.name}\n"

        return description

    def has_second_table_primary_key_of_first_table_primary_key(self, table_name, other_table_name):
        if (table_name != other_table_name):
            inspector = inspect(self.engine)
            pk_columns = inspector.get_pk_constraint(table_name)['constrained_columns']

            other_pk_columns = inspector.get_pk_constraint(other_table_name)['constrained_columns']
            for pk_column in pk_columns:
                if pk_column in other_pk_columns:
                    return True

        return False

    def create_description_for_kroki(self, file_name):
        text_description = ''
        relationship_description = self.describe_relations_between_tables()

        for table_name in self.metadata.tables:
            table = self.metadata.tables[table_name]
            text_description += self.describe_kroki_table(table) + "\n\n"

        with open(file_name, 'w') as file:
            file.write(text_description)
            file.write(relationship_description)
            file.close()

    def describe_relations_between_tables(self):
        relationship_description = "\n\n# Relationships"
        encountered_relationships = set()

        all_foreign_keys = self.get_all_foreign_keys()
        all_primery_keys = self.get_all_primary_keys()
        for table_name in self.metadata.tables:
            table = self.metadata.tables[table_name]
            symbol = ""

            has_primary_key = any(column.primary_key for column in table.columns)
            primary_keys = [constraint for constraint in table.constraints if
                            isinstance(constraint, PrimaryKeyConstraint)]
            unique_constraints = [constraint for constraint in table.constraints if
                                  isinstance(constraint, UniqueConstraint)]

            relationship_description += self.check_relation_many_to_many(table, table_name, all_primery_keys, encountered_relationships)
            relationship_description += self.check_relation_one_to_one(table_name, primary_keys, all_foreign_keys,
                                                                       unique_constraints, encountered_relationships)
            relationship_description += self.check_relation_one_to_many(table_name, primary_keys, all_foreign_keys, encountered_relationships)

        return relationship_description

    def check_relation_many_to_many(self, table, table_name, all_primery_keys, encountered_relationships):
        symbol = ""
        relationship_description = ""
        for constraint in all_primery_keys:
            referred_table = constraint.table.name
            symbol = "*--*"
            combined_relationship = (referred_table, symbol, table_name)
            print(combined_relationship)
            if self.has_second_table_primary_key_of_first_table_primary_key(table_name,
                                                                            constraint.table.name) and referred_table != table_name and combined_relationship not in encountered_relationships and combined_relationship[::-1] not in encountered_relationships:
                #relationship_description += f"\n{referred_table} {symbol} {table_name}"
                encountered_relationships.add(combined_relationship)
                print(f"\n{referred_table} {symbol} {table_name}")
        return relationship_description

    def check_relation_one_to_one(self, table_name, primary_keys, foreign_keys, unique_constraints, encountered_relationships):
        symbol = ""
        relationship_description = ""
        for constraint in foreign_keys:
            referred_table = constraint.column.table.name
            for pk in primary_keys:
                for columns in pk:
                    for unique in unique_constraints:
                        for uni in unique:
                            symbol = "1--1"
                            if referred_table != table_name and constraint.column.name == uni.name:  # różne nazwy tabel oraz nazwa FK jest równa Unique
                                relationship_description += f"\n{referred_table} {symbol} {table_name}"
        return relationship_description

    def check_relation_one_to_many(self, table_name, primary_keys, foreign_keys, encountered_relationships):
        symbol = ""
        relationship_description = ""
        for constraint in foreign_keys:
            if (constraint.column.table.name != table_name):
                referred_table = constraint.column.table.name
                for pk in primary_keys:
                    for columns in pk:
                        symbol = "*--1"
                        combined_relationship = (referred_table, symbol, table_name)
                        if self.has_second_table_foreign_key_of_first_table_primary_key(columns.name,
                                                                                        constraint.column.table.name) and referred_table != table_name and combined_relationship not in encountered_relationships and combined_relationship[::-1] not in encountered_relationships:  # usunelam to sprawdzanie
                            relationship_description += f"\n{referred_table} {symbol} {table_name}"
                            print(relationship_description)
                            encountered_relationships.add(combined_relationship)
        return relationship_description

    def has_second_table_foreign_key_of_first_table_primary_key(self, primary_key, second_table):
        inspector = inspect(self.engine)
        foreign_keys = inspector.get_foreign_keys(second_table)
        for foreign_key in foreign_keys:
            referred_columns = foreign_key['referred_columns']
            if primary_key in referred_columns:
                return True

        return False

    def has_intermediate_table(self, table_name):
        foreign_keys = self.inspector.get_foreign_keys(table_name)

        referred_tables = set()
        for foreign_key in foreign_keys:
            referred_tables.add(foreign_key['referred_table'])

        return len(referred_tables) > 1

    def get_all_foreign_keys(self):
        all_foreign_keys = []
        for table in self.metadata.tables.values():
            foreign_keys = table.foreign_keys
            all_foreign_keys.extend(foreign_keys)
        return all_foreign_keys

    def get_all_primary_keys(self):
        all_primary_keys = []
        for table in self.metadata.tables.values():
            primary_key = [constraint for constraint in table.constraints if
                           isinstance(constraint, PrimaryKeyConstraint)]
            all_primary_keys.extend(primary_key)
        return all_primary_keys


'''
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

    dot.render('database_schema', format='png', view=True)'''
