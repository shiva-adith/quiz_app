import tkinter as tk
from tkinter import font
from PIL import ImageTk, Image
from brain import QuizBrain

THEME_COLOR = "#cbf1f5"
MAIN_FONT = ("Arial", 20, "normal")
SCORE_FONT = ("Arial", 10, "bold")


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = font.Font(family='Helvetica', size=20, weight="bold", slant="italic")

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

        quiz_frame = tk.Frame(self)
        quiz_frame.place(relx=0.5, rely=0.5, anchor='center')

        bg_img = ImageTk.PhotoImage(Image.open("images/quiz_page.png"))
        bg_canvas = tk.Canvas(quiz_frame, width=500, height=750, highlightthickness=0)
        bg_canvas.background = bg_img
        bg_canvas.create_image(0, 0, anchor=tk.NW, image=bg_img)
        bg_canvas.grid(column=0, row=0, columnspan=2, rowspan=2)

        # self.score_label = tk.Label(quiz_frame, text="Score: ", font=controller.title_font)
        # self.score_label.grid(column=0, row=0, pady=20)

        question_text = bg_canvas.create_text(250, 375, text="Sample Text", fill="black",
                                              font=("Helvetica", 15, "italic"))

        self.true_img = ImageTk.PhotoImage(file="images/true.png")
        self.true_btn = tk.Button(quiz_frame, image=self.true_img)
        # true_btn.place(x=130, y=515)
        self.true_btn.grid(column=0, row=1)

        self.false_img = ImageTk.PhotoImage(file="images/false.png")
        self.false_btn = tk.Button(quiz_frame, image=self.false_img)
        self.false_btn.grid(column=1, row=1)

        # self.home_btn = tk.Button(quiz_frame, text="Main Page", command=lambda: controller.show_frame("MainPage"))
        # self.home_btn.grid(column=1, row=1, pady=20)


app = App()
app.title("Quiz App")
app.config(bg=THEME_COLOR)
app.minsize(width=500, height=750)
app.maxsize(width=500, height=750)
app.mainloop()
