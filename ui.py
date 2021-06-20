import tkinter as tk
from tkinter import font, StringVar
from PIL import ImageTk, Image
from brain import QuizBrain
from data import Data

THEME_COLOR = "#cbf1f5"
MAIN_FONT = ("Arial", 20, "normal")
SCORE_FONT = ("Arial", 10, "bold")
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 750


class App(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        # self.master = master
        self.quiz_config = Data()

        # Fonts
        self.question_font = font.Font(family="Helvetica", size=12, weight="bold")
        self.title_font = font.Font(family="Helvetica", size=20, weight="bold", slant="italic")
        self.score_font = font.Font(family="Helvetica", size=13, weight="bold")

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

        Args:
            page_name: (str) Name of the page to display

        Returns:
            None
        """
        frame = self.frames[page_name]
        frame.tkraise()


class MainPage(tk.Frame):
    """
    Creates the MainPage

    Args:
        parent: References App container
        controller: References App controller

    Attributes:
        main_frame: MainPage frame that inherits from tk.Frame class.
        bg_img: PhotoImage object that loads background image for the MainPage.
        bg_canvas: Creates Canvas object to display background image, question and score texts.
        category_list: List of available category names obtained from Data class.
        category_dropdown: Populates an OptionMenu object with category_list.
        set_quiz_btn: Calls user_selection method.
        quiz_page_btn: Invokes show_frames method from parent and passes QuizPage as args.


    """
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        self.controller = controller
        # self.quiz_config = None

        # Create main frame
        self.main_frame = tk.Frame(self)
        self.main_frame.place(relx=0.5, rely=0.5, anchor='center')

        # Set Background Image for Main Page
        self.bg_img = ImageTk.PhotoImage(Image.open("images/main_page.png"))
        self.bg_canvas = tk.Canvas(self.main_frame, width=500, height=750, highlightthickness=0)
        self.bg_canvas.background = self.bg_img
        self.bg_canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_img)
        self.bg_canvas.grid(column=0, row=0, columnspan=2, rowspan=3)

        # Dropdown Categories
        self.category_list = self.controller.quiz_config.available_category_names
        # get max size of Category labels to set the width of OptionsMenu bar
        max_size = int(max([len(category) for category in self.category_list]))
        self.category = StringVar(self.main_frame)
        # default value -> First on the list
        self.category.set(self.category_list[0])
        self.category_dropdown = tk.OptionMenu(self.main_frame, self.category, *self.category_list)
        self.category_dropdown.config(bd=0, width=max_size, font=('helvetica', 10, 'normal'), text='Choose Category')
        self.category_dropdown.grid(column=0, row=1, sticky='e', padx=20)

        # Spinbox
        self.num_questions = tk.Spinbox(self.main_frame, from_=5, to=30,
                                        bd=0, justify="center")
        self.num_questions.grid(column=1, row=1, sticky='w', padx=20)

        # Buttons:
        # Set category for Quiz
        self.set_quiz_btn = tk.Button(self.main_frame,
                                      text="Submit Category",
                                      relief='groove',
                                      padx=5, pady=5,
                                      command=lambda: self.user_selection())
        self.set_quiz_btn.grid(column=0, row=2, sticky='w', padx=20)

        # Move to QuizPage
        self.quiz_page_btn = tk.Button(self.main_frame,
                                       text="Go To Quiz",
                                       state='disabled',
                                       relief='groove',
                                       padx=5, pady=5,
                                       command=lambda: self.controller.show_frame("QuizPage"))

        self.quiz_page_btn.grid(column=1, row=2, sticky='e', padx=20)
        # self.main_frame.grid_rowconfigure(0, minsize=100, weight=1)
        # self.main_frame.grid_rowconfigure(1, weight=0, pad=10)
        # self.main_frame.grid_rowconfigure(2, weight=1, pad=10)

    def user_selection(self):
        """
        Obtains user selection from dropdown box and passes it to set_category method from Data class.
        Invokes get_data method from Data class and then the populate_quiz method from the QuizPage class.

        Args:
            Category selected by user in the category_dropdown menu

        Returns:
            None
        """
        self.controller.quiz_config.set_num_questions(self.num_questions.get())
        self.controller.quiz_config.set_category(self.category.get())
        self.controller.quiz_config.get_data()
        self.controller.frames["QuizPage"].populate_quiz()

        # Disable set quiz button and enable change page button. (Only after above processes are successful)
        self.set_quiz_btn.config(state="disabled")
        self.quiz_page_btn.config(state='active')


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
        self.score_text = self.bg_canvas.create_text(150, 250, text=f"Score: 0",
                                                     fill="green", font=self.s_font)

        # Display Question text
        self.question = self.bg_canvas.create_text(250, 375, fill="black",
                                                   font=self.q_font, width=300)

        self.indicator_label = self.bg_canvas.create_text(250, 250, fill="green", width=60)

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
        """
        Populates the Quiz text space with questions based on user selection for Category.
        Method is invoked by the Submit Category button in the MainPage.
        Creates QuizBrain object. Its arg is the question bank returned by calling create_quiz method of Data class.
        Invokes get_next_question method if number of question left is less than the selected value.

        Returns:
            None
        """
        # print("populate quiz called")
        self.quiz = QuizBrain(self.controller.quiz_config.create_quiz())

        if self.quiz.questions_remaining():
            self.get_next_question()

    def get_next_question(self):
        """
        If questions are left, it displays the next question on the Canvas. next_question method from QuizBrain is
        invoked.
        If there are no more questions, appropriate text is displayed and the buttons are set to 'disabled' state.

        Returns:
            None
        """
        if self.quiz.questions_remaining():
            q_text = self.quiz.next_question()
            # print("get next ques reached")
            self.bg_canvas.itemconfig(self.question, text=f"{q_text}")
        else:
            self.bg_canvas.itemconfig(self.question, text="You're all out of Questions!")
            self.true_btn.config(state="disabled")
            self.false_btn.config(state="disabled")

    def correct(self):
        """Answer chosen by User is 'True'

        Passes 'True' to check_answer method from QuizBrain class. Uses bool return value as args to feedback method

        Args (implicit args):
            bool: True

        """
        self.feedback(self.quiz.check_answer("True"))

    def incorrect(self):
        """Answer chosen by User is 'False'

        Passes 'False' to check_answer method from QuizBrain class. Uses bool return value as args to feedback method

        Args (implicit args):
           bool: False

        """
        self.feedback(self.quiz.check_answer("False"))

    def feedback(self, right_ans):
        """
        Updates score_text based on User's choice and bool value returned by check_answer method of QuizBrain class.
        Waits 1 second and invokes get_next_question method.

        Args:
            right_ans (bool): True/False based on actual answer to question compared to user's choice

        Returns:
            None
        """
        if right_ans:
            # TODO: The indicator label only flashes once. Doesn't appear for the other correct answers. 
            print("correct")
            self.bg_canvas.itemconfig(self.indicator_label, text="✔")
            self.bg_canvas.itemconfig(self.score_text, text=f"Score: {self.quiz.score}")
            self.after(2000, self.bg_canvas.delete, self.indicator_label)
        else:
            print("incorrect")

        self.after(1000, func=self.get_next_question())
