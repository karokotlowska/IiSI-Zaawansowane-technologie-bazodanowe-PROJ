from dotenv import load_dotenv

from chatGPT import ChatGPT
from context import Context
from config import delete_tmp_dir, delete_output_dir
from menu import Menu
import logging

if __name__ == '__main__':
    load_dotenv()
    logging.basicConfig()
    logging.root.setLevel(logging.NOTSET)
    logging.basicConfig(level=logging.NOTSET)

    try:
        delete_output_dir()
        menu = Menu()
        menu.run(Context.run)
    except ChatGPT.GPTException as e:
        print(e.message)
    except Exception as e:
        raise e
    finally:
        delete_tmp_dir()
