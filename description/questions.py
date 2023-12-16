class Query:
    class Question:
        def __init__(self, question: str):
            self.question = question

        def builder(self, db_details: str, lang: str):
            language = Query.Lang.map_to_full_name(lang)
            return self.question % (db_details, language)

    class Lang:
        PL = "PL"
        EN = "EN"
        ES = "ES"

        @staticmethod
        def create_from(lang: str):
            if lang.lower() == Query.Lang.PL.lower():
                return Query.Lang.PL
            elif lang.lower() == Query.Lang.EN.lower():
                return Query.Lang.EN
            elif lang.lower() == Query.Lang.ES.lower():
                return Query.Lang.ES
            else:
                raise Exception("Invalid language")

        @staticmethod
        def map_to_full_name(lang: str):
            if lang.lower() == Query.Lang.PL.lower():
                return "Polish"
            elif lang.lower() == Query.Lang.EN.lower():
                return "English"
            elif lang.lower() == Query.Lang.ES.lower():
                return "Spanish"
            else:
                raise Exception("Invalid language")

    DATABASE_EN = Question(
        "Generate a description for the database with the given structure in JSON format name_schema => content: %s Please make the description contain min 400 words. Please return description under the 'database' key in  JSON format: { \"database\": \"database_description\"}. Descriptions should be in %s language. If you want to use new line character please use \\n instead of new line and \" instead of quotes.")

    TABLES_EN = Question(
        "Generate a description for all tables in the relational database with this JSON structure: %s. The description should attempt to guess the semantics and relationships between the tables. The table description should contain a minimum of 3 sentences, a maximum of 5. Return the results in JSON format: { \"table_name_1\": \"table_name_1_description\", \"table_name_2\": \"table_name_2_description\"} and return nothing else. Descriptions should be in %s language. Use the \\n character instead of new lines and \" instead of quotes.")

    VIEWS_EN = Question(
        "Generate a description for all views in the relational database with this JSON structure: %s. The view description should contain a minimum of 3 sentences, a maximum of 5. Return the results in JSON format: { \"view_name_1\": \"view_name_1_description\", \"view_name_2\": \"view_name_2_description\"} and return nothing else. Descriptions should be in %s language. Use the \\n character instead of new lines and \" instead of quotes.")

    FUNCTIONS_EN = Question(
        "Generate a description for all functions in the relational database with this JSON structure: %s. The function description should contain a minimum of 3 sentences, a maximum of 5. Return the results in JSON format: { \"function_name_1\": \"function_name_1_description\", \"function_name_2\": \"function_name_2_description\", ...} and return nothing else. Descriptions should be in %s language. Use the \\n character instead of new lines and \" instead of quotes.")
