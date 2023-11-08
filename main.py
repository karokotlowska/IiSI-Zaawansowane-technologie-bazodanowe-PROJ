
import sqlalchemy
from dotenv import load_dotenv
from sqlalchemy import MetaData, PrimaryKeyConstraint, UniqueConstraint, ForeignKeyConstraint
from sqlalchemy.engine import create_engine
from graphviz import Digraph
import time
import sys
import threading
from sqlalchemy import inspect

from Kroki.kroki import get_diagram_svg, convert_svg_to_png, save_svg_diagram
from Database import Database
from menu import Menu
from description import DescriptionGenerator, Query

load_dotenv()


# db_type = input("Enter the database type (e.g., postgresql, mysql): ")
# db_host = input("Enter the database host: ")
# db_port = input("Enter the database port: ")
# db_name = input("Enter the database name: ")
# db_user = input("Enter the database username: ")
# db_password = input("Enter the database password: ")

def run(db_url: str, lang: Query.Lang):
    db = Database()
    db.connect(db_url)
    db.create_description_for_chat('description_for_chat.txt')
    db.create_description_for_kroki('description_for_kroki.txt')


    svg_diagram = get_diagram_svg('description_for_kroki.txt', 'kroki.io')
    save_svg_diagram('diagram.svg', svg_diagram)
    convert_svg_to_png('diagram.svg')



    DescriptionGenerator.runner('description_for_chat.txt', lang)


if __name__ == '__main__':
    menu = Menu()
    menu.run(run)
