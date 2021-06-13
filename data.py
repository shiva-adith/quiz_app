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

        # Trivia Data Configurations
        self.num_questions = DEFAULTS.get("num_questions")
        # self.category = DEFAULTS.get("category")
        self.category = None
        self.question_type = DEFAULTS.get("question_type")
        # Config request
        self.category_response = requests.get(url=DEFAULTS.get("category_url"))
        self.available_categories = self.get_categories()
        self.available_category_names = self.get_category_names()

        # Retrieve Quiz Data
        self.parameters = {"amount": self.num_questions, "type": self.question_type}
        self.data_response = None
        self.data = None
        self.question_data = None

    def get_categories(self):
        # TODO: Only return categories that contain questions (some categories return empty as of now)
        # TODO: the aPI has a url request for getting number of questions for each category ID.
        data = self.category_response.json().get("trivia_categories")

        categories = {category.get("name"): category.get("id") for category in data}

        return categories

    def get_category_names(self):

        data = self.category_response.json().get("trivia_categories")

        categories = [category.get("name") for category in data]

        return categories

    def set_category(self, user_choice):
        # self.category = user_choice
        id = self.available_categories.get(user_choice)
        self.parameters["category"] = int(id)
        # self.parameters["category"] = self.category
        print(self.parameters)

    def set_num_questions(self, num_questions):
        self.parameters['amount'] = int(num_questions)

    def share_data(self):
        return self.question_data

    def get_data(self):
        print("get data", self.parameters)
        self.data_response = requests.get(url=DEFAULTS.get("data_url"), params=self.parameters)
        self.data = self.data_response.json()
        self.question_data = self.data.get("results")

    def create_quiz(self):
        # print(f"{__name__} Called")
        self.get_data()
        question_bank = []

        for question in self.question_data:
            question_text = question.get("question")
            question_answer = question.get("correct_answer")
            new_question = QuestionModel(question_text, question_answer)
            question_bank.append(new_question)

        return question_bank
