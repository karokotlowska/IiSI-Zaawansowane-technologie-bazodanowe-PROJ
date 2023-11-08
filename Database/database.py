from sqlalchemy import MetaData, PrimaryKeyConstraint, UniqueConstraint, ForeignKeyConstraint
from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import inspect

class Database:
    def __init__(self):
        self.metadata = []
        self.tables = []
        self.engine = ''
        self.db_url = ''
    
    def connect(self, db_url):
        self.db_url = db_url
        engine = create_engine(self.db_url)
        self.engine = engine
        metadata = MetaData()
        metadata.reflect(bind=engine)
        self.metadata = metadata
        self.tables = metadata.tables

    def create_description_for_chat(self, file_name):
        text_description = ''
        comments = ''

        for table_name in self.tables:
            table = self.metadata.tables[table_name]
            print(table)
            text_description += self.describe_table(table) + "\n"
            for column in table.columns:
                if column.comment:
                    comments += f"Table: {table.name}, Column: {column.name}, Comment: {column.comment}\n"

        with open(file_name, 'w') as file:
            file.write(text_description)
            file.write("\n\nComments:\n")
            file.write(comments)

    def describe_table(self, table):
        description = f"Table: {table.name}\n"
        foreign_keys = set()

        for t in self.tables.values():
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
        if(table_name != other_table_name):
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
            primary_keys = [constraint for constraint in table.constraints if isinstance(constraint, PrimaryKeyConstraint)]
            unique_constraints = [constraint for constraint in table.constraints if isinstance(constraint, UniqueConstraint)]

            relationship_description += self.check_relation_many_to_many(table, table_name, all_primery_keys)
            relationship_description += self.check_relation_one_to_one(table_name, primary_keys, all_foreign_keys, unique_constraints)
            relationship_description += self.check_relation_one_to_many(table_name, primary_keys, all_foreign_keys)

        return relationship_description
        
    def check_relation_many_to_many(self, table, table_name, all_primery_keys):
        symbol = ""
        relationship_description = ""
        for constraint in all_primery_keys:
            referred_table = constraint.table.name
            symbol = "*--*"
            if self.has_second_table_primary_key_of_first_table_primary_key(table_name, constraint.table.name) and referred_table!= table_name:
                relationship_description += f"\n{referred_table} {symbol} {table_name}"
        return relationship_description
    
    def check_relation_one_to_one(self, table_name, primary_keys, foreign_keys, unique_constraints):
        symbol = ""
        relationship_description = ""
        for constraint in foreign_keys:
            referred_table = constraint.column.table.name
            for pk in primary_keys:
                for columns in pk:
                    for unique in unique_constraints:
                        for uni in unique:
                            symbol = "1--1"
                            if referred_table!= table_name and constraint.column.name == uni.name:    #różne nazwy tabel oraz nazwa FK jest równa Unique     
                                    relationship_description += f"\n{referred_table} {symbol} {table_name}"
        return relationship_description

    def check_relation_one_to_many(self, table_name, primary_keys, foreign_keys):
        symbol = ""
        relationship_description = ""
        for constraint in foreign_keys:
            if(constraint.column.table.name != table_name):
                referred_table = constraint.column.table.name
                for pk in primary_keys:
                    for columns in pk:
                        symbol = "*--1"
                        if self.has_second_table_foreign_key_of_first_table_primary_key(columns.name, constraint.column.table.name) and referred_table!= table_name : #usunelam to sprawdzanie
                            relationship_description += f"\n{referred_table} {symbol} {table_name}"
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
        inspector = inspect(self.engine)
        foreign_keys = inspector.get_foreign_keys(table_name)

        referred_tables = set()
        for foreign_key in foreign_keys:
            referred_tables.add(foreign_key['referred_table'])

        return len(referred_tables) > 1

    def get_all_foreign_keys(self):
        all_foreign_keys = []
        for table in self.metadata.tables.values():
            foreign_keys =  table.foreign_keys
            all_foreign_keys.extend(foreign_keys)
        return all_foreign_keys

    def get_all_primary_keys(self):
        all_primary_keys = []
        for table in self.metadata.tables.values():
            primary_key = [constraint for constraint in table.constraints if isinstance(constraint, PrimaryKeyConstraint)]
            all_primary_keys.extend(primary_key)
        return all_primary_keys