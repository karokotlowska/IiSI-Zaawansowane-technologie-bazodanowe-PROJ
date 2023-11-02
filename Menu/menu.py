import argparse


class Menu:
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('--uri', help='URI for the database')
        self.parser.add_argument('--db', help='Database name')
        self.parser.add_argument('-u', '--user', help='Database user')
        self.parser.add_argument('--password', help='Database password')
        self.parser.add_argument('-p', '--port', help='Database port')
        self.parser.add_argument('-h', '--host', help='Database host')
        self.parser.add_argument('-l', '--lang', help='Output language for the chatbot', default='en')

    def run(self):
        args = self.parser.parse_args()
        lang = args.lang

        if args.uri:
            db_url = args.uri
        elif args.db and args.user and args.password and args.host and args.port:
            db_url = f"postgresql://{args.user}:{args.password}@{args.host}:{args.port}"
        elif args.db and args.user and args.host and args.port:
            db_url = f"postgresql://{args.user}@{args.host}:{args.port}"
        else:
            raise Exception("Invalid arguments")

        # run.....
