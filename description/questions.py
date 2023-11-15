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

    DATABASE_PL = Question("Wygeneruj opis dla bazy danych o podanej strukturze w formacie JSON nazwa_schematu => zawartosc: %s Prosze aby opis zawieral min 400 slow. Wyniki zwroc w języku polskim w formacie JSON w postaci: {\"database\": \"description\"} i niezwracaj nic wiecej")
    DATABASE_EN = Question("Generate a description for the database with the given structure in JSON format name_schema => content: %s Please make the description contain min 400 words. Return the results in english JSON format in the form: { \"database\": \"description\"} and return nothing else.")

    TABLES_PL = Question(
        "Wygeneruj opis dla tabel w relacyjnej bazie danych o takiej strukturze JSON: %s Opis powinien próbować odgadnąć semantyke oraz relacje pomiędzy tabelami. Opis tabeli powinien zawierać minimalnie 3 zdania, maksymalnie 5. Wyniki zwróć w języku polskim w formacie JSON w postaci: {\"table_name_1\": \"description\", \"table_name_2\": \"description\", ...}  i nie zwracaj nic więcej opócz JSONa")
    TABLES_EN = Question(
        "Generate a description for the tables in the relational database with this JSON structure: %s The description should attempt to guess the semantics and relationships between the tables. The table description should contain a minimum of 3 sentences, a maximum of 5. Return the results in english JSON format in the form: { \"table_name_1\": \"description\", \"table_name_2\": \"description\"} and return nothing else.")

    VIEWS_PL = Question(
        "Wygeneruj opis dla widoków w relacyjnej bazie danych o takiej strukturze JSON: %s . Opis widoku powinien zawierać minimalnie 3 zdania, maksymalnie 5. Wyniki prosze zwróć w jezyku polskim w formacie JSON w postaci: {\"view_name_1\": \"description\", \"view_name_2\": \"description\", ...} i nie zwracaj nic więcej oprócz JSONa")
    VIEWS_EN = Question("Generate a description for the tables in the relational database with this JSON structure: %s . The view description should contain a minimum of 3 sentences, a maximum of 5. Return the results in english JSON format in the form: { \"view_name_1\": \"description\", \"view_name_2\": \"description\"} and return nothing else.")

    FUNCTIONS_PL = Question(
        "Wygeneruj opis dla funkcji w relacyjnej bazie danych o takiej strukturze JSON: %s . Opis funkcji powinien zawierać minimalnie 3 zdania, maksymalnie 5. Wyniki prosze zwróć w języku polskim w formacie JSON w postaci: {\"function_name_1\": \"description\", \"function_name_2\": \"description\", ...} i nie zwracaj nic więcej oprócz JSONa")
    FUNCTIONS_EN = Question(
        "Generate a description for the functions in the relational database with this JSON structure: %s . The function description should contain a minimum of 3 sentences, a maximum of 5. Return the results in english  JSON format in the form: { \"function_name_1\": \"description\", \"function_name_2\": \"description\", ...} and return nothing else."
    )

