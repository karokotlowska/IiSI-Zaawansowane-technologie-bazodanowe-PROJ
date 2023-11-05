class Query:
    class Question:
        def __init__(self, question: str):
            self.question = question

        def builder(self, db_details: str):
            return self.question % db_details

    class Lang:
        PL = "PL"
        EN = "EN"

        @staticmethod
        def create_from(lang: str):
            if lang.lower() == Query.Lang.PL.lower():
                return Query.Lang.PL
            elif lang.lower() == Query.Lang.EN.lower():
                return Query.Lang.EN
            else:
                raise Exception("Invalid language")

    PL = Question(
        "Wygeneruj opis dla tabeli o takiej strukturze: %s Opis powinien próbować odgadnąć semantyke oraz relacje pomiędzy tabelami")
    EN = Question(
        "Generate a description for a table with such a structure: %s The description should try to guess the semantics and relationships between tables")
