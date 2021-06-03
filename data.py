import requests

DEFAULTS = {
        "category_url": "https://opentdb.com/api_category.php",
        "data_url": "https://opentdb.com/api.php?",
        "num_questions": 10,
        "question_type": "boolean",
        "category": None
}


class QuestionModel:
    def __init__(self, q_text, q_answer):
        self.question = q_text
        self.answer = q_answer


class Data:
    def __init__(self):
        self.category_response = requests.get(url=DEFAULTS.get("category_url"))

        # Trivia Data Configurations
        self.num_questions = DEFAULTS.get("num_questions")
        self.category = DEFAULTS.get("category")
        self.question_type = DEFAULTS.get("question_type")
        self.available_categories = self.get_category_names()
        self.available_category_ids = self.get_category_ids()

        self.parameters = {"amount": self.num_questions, "type": self.question_type}

        self.data_response = requests.get(url=DEFAULTS.get("data_url"), params=self.parameters)
        self.data = self.data_response.json()

        self.question_data = self.data.get("results")

    def get_category_names(self):

        data = self.category_response.json().get("trivia_categories")

        categories = [category.get("name") for category in data]

        return categories

    def get_category_ids(self):

        data = self.category_response.json().get("trivia_categories")

        ids = [category.get("id") for category in data]

        return ids

    def set_category(self, user_choice):
        pass

    def share_data(self):
        return self.question_data
