import requests


class Data:
    def __init__(self):
        self.url = "https://opentdb.com/api.php?"
        self.parameters = {"amount": 10, "type": "boolean"}

        self.response = requests.get(url=self.url, params=self.parameters)
        self.response.raise_for_status()
        self.data = self.response.json()

        self.question_data = self.data.get("results")
        print(self.question_data[:2])


data = Data()
