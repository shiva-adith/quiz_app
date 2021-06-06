import tkinter as tk
from tkinter import font, StringVar
from PIL import ImageTk, Image
from brain import QuizBrain
from data import Data

THEME_COLOR = "#cbf1f5"
MAIN_FONT = ("Arial", 20, "normal")
SCORE_FONT = ("Arial", 10, "bold")


# class App(tk.Tk):
class App(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        # self.master = master
        self.quiz_config = Data()

        # Fonts
        self.question_font = font.Font(family="Helvetica", size=12, weight="bold")
        self.title_font = font.Font(family='Helvetica', size=20, weight="bold", slant="italic")
        self.score_font = font.Font(family="Helvetica", size=15, weight="bold")

        self.container = tk.Frame(self, bg=THEME_COLOR)
        self.container.pack(side="top", fill="both", expand=True)
        # container.grid(column=0, row=0, sticky="nsew")

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # Create Frames for both pages
        for F in (MainPage, QuizPage):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)

            self.frames[page_name] = frame

            frame.grid(column=0, row=0, sticky="nsew")

        self.show_frame("MainPage")

    def show_frame(self, page_name):
        """
            Displays desired frame/page
        :param page_name: (str) Name of the page to display
        :return: None
        """
        frame = self.frames[page_name]
        frame.tkraise()


class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        """
        Creates the MainPage

        """
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # self.quiz_config = None

        # Create main frame
        main_frame = tk.Frame(self)
        main_frame.place(relx=0.5, rely=0.5, anchor='center')

        # Set Background Image for Main Page
        self.bg_img = ImageTk.PhotoImage(Image.open("images/main_page.png"))
        self.bg_canvas = tk.Canvas(main_frame, width=500, height=750, highlightthickness=0)
        self.bg_canvas.background = self.bg_img
        self.bg_canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_img)
        self.bg_canvas.grid(column=0, row=0, columnspan=2, rowspan=3)

        # Checkboxes
        # num_question_1 = tk.Radiobutton(main_frame, background="orange", borderwidth=0, highlightthickness=0)
        # num_question_1.grid(column=0, row=1)

        # Dropdown Categories
        self.category_list = self.controller.quiz_config.available_category_names
        self.category = StringVar(main_frame)
        # default value -> First on the list
        self.category.set(self.category_list[0])
        category_dropdown = tk.OptionMenu(main_frame, self.category, *self.category_list)
        category_dropdown.grid(column=1, row=1)

        # Buttons:
        # Set category for Quiz
        self.set_quiz_btn = tk.Button(main_frame, text="Submit Category",
                                      command=lambda: self.user_category_selection())
        self.set_quiz_btn.grid(column=0, row=2)

        # Move to QuizPage
        self.quiz_page_btn = tk.Button(main_frame, text="Go To Quiz",
                                       command=lambda: self.controller.show_frame("QuizPage"))

        self.quiz_page_btn.grid(column=1, row=2)

    def user_category_selection(self):
        """
        Obtains user selection from dropdown box and passes it to populate_quiz method.
        :return: None
        """
        print(self.category.get())
        # self.quiz_config = Data(self.category.get())
        self.controller.quiz_config.set_category(self.category.get())
        self.controller.quiz_config.get_data()
        self.controller.frames["QuizPage"].populate_quiz()


class QuizPage(tk.Frame):
    """
    Creates QuizPage

    Args:
        parent: References App container
        controller: References App controller

    Attributes:
        quiz_frame: QuizPage frame that inherits from tk.Frame class
        bg_img: PhotoImage object that loads background image for the QuizPage
        score_text: Display Score which increments with every correct answer
        question: Display questions based on category selected by user. Questions obtained from Data class.

    """
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.quiz = None

        # Fonts
        self.q_font = self.controller.question_font
        self.s_font = self.controller.score_font

        # Create quiz frame
        self.quiz_frame = tk.Frame(self)
        self.quiz_frame.place(relx=0.5, rely=0.5, anchor='center')

        # Set Background Image for Quiz Page
        self.bg_img = ImageTk.PhotoImage(Image.open("images/quiz_page.png"))
        self.bg_canvas = tk.Canvas(self.quiz_frame, width=500, height=750, highlightthickness=0)
        self.bg_canvas.background = self.bg_img
        self.bg_canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_img)
        self.bg_canvas.grid(column=0, row=0, columnspan=2, rowspan=2)

        # Display Score text
        self.score_text = self.bg_canvas.create_text(200, 250, text=f"Score: 0",
                                                     fill="red", font=self.s_font)

        # Display Question text
        self.question = self.bg_canvas.create_text(250, 375, fill="black",
                                                   font=self.q_font, width=300)

        # Buttons
        # True button - calls method: correct()
        self.true_img = ImageTk.PhotoImage(file="images/true.png")
        self.true_btn = tk.Button(self.quiz_frame, image=self.true_img, command=self.correct)
        # true_btn.place(x=130, y=515)
        self.true_btn.grid(column=0, row=1)

        # False button - calls method: incorrect()
        self.false_img = ImageTk.PhotoImage(file="images/false.png")
        self.false_btn = tk.Button(self.quiz_frame, image=self.false_img, command=self.incorrect)
        self.false_btn.grid(column=1, row=1)

        # self.home_btn = tk.Button(quiz_frame, text="Main Page", command=lambda: controller.show_frame("MainPage"))
        # self.home_btn.grid(column=1, row=1, pady=20)

    def populate_quiz(self):
        """Populates the Quiz Text space with questions based on user selection for Category.

            Method is invoked by the Submit Category button.
            Creates QuizBrain object. Its arg is the question bank returned by calling create_quiz method of Data class.
        :return:
        """
        # print("populate quiz called")
        self.quiz = QuizBrain(self.controller.quiz_config.create_quiz())

        if self.quiz.questions_remaining():
            self.get_next_question()

    def get_next_question(self):
        if self.quiz.questions_remaining():
            q_text = self.quiz.next_question()
            # print("get next ques reached")
            self.bg_canvas.itemconfig(self.question, text=f"{q_text}")
        else:
            self.bg_canvas.itemconfig(self.question, text="You're all out of Questions!")
            self.true_btn.config(state="disabled")
            self.false_btn.config(state="disabled")

    def correct(self):
        self.feedback(self.quiz.check_answer("True"))

    def incorrect(self):
        self.feedback(self.quiz.check_answer("False"))

    def feedback(self, right_ans):
        if right_ans:
            print("correct")
            self.bg_canvas.itemconfig(self.score_text, text=f"Score: {self.quiz.score}")
            # self.bg_canvas.config(bg="green")
        else:
            print("incorrect")

        self.after(1000, func=self.get_next_question())
#
#
# root = tk.Tk()
# root.title("Quiz App")
# app = App(root)
# app.pack(fill="both", expand=True)
# root.config(bg=THEME_COLOR)
# root.minsize(width=500, height=750)
# root.maxsize(width=500, height=750)
# root.mainloop()
