import ui
from brain import QuizBrain
from data import Data, QuestionModel


def main():
    question_data = Data()
    question_bank = []

    for question in question_data.share_data():
        question_text = question.get("question")
        question_answer = question.get("correct_answer")
        new_question = QuestionModel(question_text, question_answer)
        question_bank.append(new_question)

    return question_bank


# if "__name__" == "__main__":
q_bank = main()
quiz = QuizBrain(q_bank)
# app = ui.App(q_list=quiz)
