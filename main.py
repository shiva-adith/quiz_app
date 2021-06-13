from ui import *


def main():
    """
    Create Tkinter root window and App object from ui.file.

    """

    root = tk.Tk()
    root.title("Quiz App")
    app = App(root)
    app.pack(fill="both", expand=True)
    root.minsize(width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
    root.maxsize(width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
    root.mainloop()


if __name__ == "__main__":
    main()
