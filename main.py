from ui import *
from brain import QuizBrain
from data import QuestionModel, Data


# def main():
#     question_data = Data()
#     question_bank = []
#
#     for question in question_data.share_data():
#         question_text = question.get("question")
#         question_answer = question.get("correct_answer")
#         new_question = QuestionModel(question_text, question_answer)
#         question_bank.append(new_question)
#
#     return question_bank


# if "__name__" == "__main__":

# data = Data()
# quiz = QuizBrain(q_bank.create_quiz())

root = tk.Tk()
root.title("Quiz App")
app = App(root)
app.pack(fill="both", expand=True)
root.config(bg=THEME_COLOR)
root.minsize(width=500, height=750)
root.maxsize(width=500, height=750)
root.mainloop()
