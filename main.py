import sqlalchemy
from dotenv import load_dotenv
from sqlalchemy import MetaData, PrimaryKeyConstraint, UniqueConstraint, ForeignKeyConstraint
from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from graphviz import Digraph
import time
import sys
import threading
from sqlalchemy import inspect

from Kroki.kroki import get_diagram_svg, convert_svg_to_png, save_svg_diagram
from Database import Database


from chatGPT import ChatGPT

load_dotenv()

# db_type = input("Enter the database type (e.g., postgresql, mysql): ")
# db_host = input("Enter the database host: ")
# db_port = input("Enter the database port: ")
# db_name = input("Enter the database name: ")
# db_user = input("Enter the database username: ")
# db_password = input("Enter the database password: ")

db_url = f"postgresql://postgres:admin@localhost:5432/shopping_db"
db = Database()
db.connect(db_url)
db.create_description_for_chat('description_for_chat.txt')
db.create_description_for_kroki('description_for_kroki.txt')


svg_diagram = get_diagram_svg('description_for_kroki.txt', 'kroki.io')
save_svg_diagram('diagram.svg', svg_diagram)
convert_svg_to_png('diagram.svg')



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