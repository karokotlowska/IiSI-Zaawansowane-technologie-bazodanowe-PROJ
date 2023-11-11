from dotenv import load_dotenv


from Kroki.kroki import get_diagram_svg, convert_svg_to_png, save_svg_diagram
from Database import Database
from menu import Menu
from description import DescriptionGenerator, Query
import logging


def run(db_url: str, lang: Query.Lang):
    db = Database()
    db.connect(db_url)
    # db.create_description_for_chat('description_for_chat.txt')
    tables = db.get_tables()
    views = db.get_views()
    db.create_description_for_kroki('description_for_kroki.txt')


    svg_diagram = get_diagram_svg('description_for_kroki.txt', 'kroki.io')
    save_svg_diagram('diagram.svg', svg_diagram)
    convert_svg_to_png('diagram.svg')


    val = DescriptionGenerator.runner(tables, views, lang)
    print(val)


if __name__ == '__main__':

    load_dotenv()
    logging.basicConfig()
    logging.root.setLevel(logging.NOTSET)
    logging.basicConfig(level=logging.NOTSET)

    menu = Menu()
    menu.run(run)
