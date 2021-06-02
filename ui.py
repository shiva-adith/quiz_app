import tkinter as tk
from tkinter import font
from PIL import ImageTk, Image
from main import quiz
from brain import QuizBrain
# from data import data

THEME_COLOR = "#cbf1f5"
MAIN_FONT = ("Arial", 20, "normal")
SCORE_FONT = ("Arial", 10, "bold")


class App(tk.Tk):
    def __init__(self, q_list, master=None, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.master = master
        self.quiz = q_list

        # Fonts
        self.question_font = font.Font(family="Lovelo", size=12, slant="italic", weight="normal")
        self.title_font = font.Font(family='Helvetica', size=20, weight="bold", slant="italic")
        self.score_font = font.Font(family="Lovelo", size=15, weight="bold")

        self.container = tk.Frame(self, bg=THEME_COLOR)
        self.container.pack(side="top", fill="both", expand=True)
        # container.grid(column=0, row=0, sticky="nsew")

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (MainPage, QuizPage):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)

            self.frames[page_name] = frame

            frame.grid(column=0, row=0, sticky="nsew")

        self.show_frame("MainPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def share_quiz(self):
        return self.quiz


class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        main_frame = tk.Frame(self)
        main_frame.place(relx=0.5, rely=0.5, anchor='center')

        bg_img = ImageTk.PhotoImage(Image.open("images/main_page.png"))

        # Background Image
        bg_canvas = tk.Canvas(main_frame, width=500, height=750, highlightthickness=0)
        bg_canvas.background = bg_img
        bg_canvas.create_image(0, 0, anchor=tk.NW, image=bg_img)
        bg_canvas.grid(column=0, row=0, columnspan=2, rowspan=3)
        # bg_canvas.place(relx=0.5, rely=0.5, anchor='center')

        # self.main_label = tk.Label(main_frame, text="Main Page", font=controller.title_font)
        # self.main_label.grid(column=0, row=0)

        # Checkboxes
        num_question_1 = tk.Radiobutton(main_frame, background="orange", borderwidth=0, highlightthickness=0)
        num_question_1.grid(column=0, row=1)

        self.quiz_btn = tk.Button(main_frame, text="Submit", command=lambda: controller.show_frame("QuizPage"))
        self.quiz_btn.grid(column=1, row=2)


class QuizPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        quiz = self.controller.quiz
        q_font = self.controller.question_font
        s_font = self.controller.score_font

        quiz_frame = tk.Frame(self)
        quiz_frame.place(relx=0.5, rely=0.5, anchor='center')

        self.bg_img = ImageTk.PhotoImage(Image.open("images/quiz_page.png"))
        self.bg_canvas = tk.Canvas(quiz_frame, width=500, height=750, highlightthickness=0)
        self.bg_canvas.background = self.bg_img
        self.bg_canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_img)
        self.bg_canvas.grid(column=0, row=0, columnspan=2, rowspan=2)

        # self.score_label = tk.Label(quiz_frame, text="Score: ", font=controller.title_font)
        # self.score_label.place(x=)
        self.score_text = self.bg_canvas.create_text(200, 250, text=f"Score: {quiz.score}",
                                                     fill="red", font=s_font)

        self.question = self.bg_canvas.create_text(250, 375, fill="black",
                                                   font=q_font, width=300)

        self.true_img = ImageTk.PhotoImage(file="images/true.png")
        self.true_btn = tk.Button(quiz_frame, image=self.true_img, command=self.correct)
        # true_btn.place(x=130, y=515)
        self.true_btn.grid(column=0, row=1)

        self.false_img = ImageTk.PhotoImage(file="images/false.png")
        self.false_btn = tk.Button(quiz_frame, image=self.false_img, command=self.incorrect)
        self.false_btn.grid(column=1, row=1)

        if quiz.questions_remaining():
            self.get_next_question()

        # self.home_btn = tk.Button(quiz_frame, text="Main Page", command=lambda: controller.show_frame("MainPage"))
        # self.home_btn.grid(column=1, row=1, pady=20)

    def get_next_question(self):
        if quiz.questions_remaining():
            q_text = quiz.next_question()
            self.bg_canvas.itemconfig(self.question, text=f"{q_text}")
        else:
            self.bg_canvas.itemconfig(self.question, text="You're all out of Questions!")
            self.true_btn.config(state="disabled")
            self.false_btn.config(state="disabled")

    def correct(self):
        self.feedback(quiz.check_answer("True"))

    def incorrect(self):
        self.feedback(quiz.check_answer("False"))

    def feedback(self, right_ans):
        if right_ans:
            print("correct")
            self.bg_canvas.itemconfig(self.score_text, text=f"Score: {quiz.score}")
            # self.bg_canvas.config(bg="green")
        else:
            print("incorrect")

        self.after(1000, func=self.get_next_question())


# quiz = QuizBrain(data)
app = App(q_list=quiz)
app.title("Quiz App")
app.config(bg=THEME_COLOR)
app.minsize(width=500, height=750)
app.maxsize(width=500, height=750)
app.mainloop()
