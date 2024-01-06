import argparse
import textwrap

from chatGPT import ChatGPT
from description import Query


class Menu:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            prog="DB Description Generator",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=textwrap.dedent('''\
            READ THIS BEFORE USING:
            Set only --uri argument  or declare all --db, --user, --password, --host, --port arguments.
            If API key is not provided, the key from environment variable OPENAI_API_KEY will be used.
            '''
                                   ))
        self.parser.add_argument('--uri', help='URI for the database')
        self.parser.add_argument('--db', help='Database name')
        self.parser.add_argument('-u', '--user', help='Database user')
        self.parser.add_argument('--password', help='Database password')
        self.parser.add_argument('-p', '--port', help='Database port')
        self.parser.add_argument('-c', '--host', help='Database host')
        self.parser.add_argument('-l', '--lang', help='Output language for the chatbot(en,pl)', default='en')
        self.parser.add_argument('--gpt-version', help='GPT version', default='gpt-3.5-turbo')
        self.parser.add_argument('--tokens', help='Max tokens', default=2048)
        self.parser.add_argument("--api-key", help="OpenAI API key")

    def run(self, runnable):
        args = self.parser.parse_args()
        lang = Query.Lang.create_from(args.lang)

        if args.uri:
            db_url = args.uri
        elif args.db and args.user and args.password and args.host and args.port:
            db_url = f"postgresql://{args.user}:{args.password}@{args.host}:{args.port}"
        elif args.db and args.user and args.host and args.port:
            db_url = f"postgresql://{args.user}@{args.host}:{args.port}"
        else:
            print("Invalid arguments: use --uri or --db, --user, --password, --host, --port")
            exit(1)

        ChatGPT.GTP_VERSION = args.gpt_version
        ChatGPT.MAX_TOKENS = int(args.tokens)

        if args.api_key:
            ChatGPT.KEY = args.api_key
            print("Using custom API key")

        runnable(db_url, lang)
