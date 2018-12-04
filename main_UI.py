import tkinter as tk
import start_page
import load_page
import result_page
import list_page

LARGE_FONT = ("Verdana", 12, "bold")
MEDIUM_FONT = ("Verdana", 10)

class GDPRApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("GDPR Database Sanitization")
        container = tk.Frame(self, bg="pink")
        container.pack()
        container.grid_rowconfigure(0, weight=5)    # expand=True
        container.grid_columnconfigure(0, weight=5)

        self.frames = {}    # dic for all frame/page
        for F in (start_page.StartPage, load_page.LoadPage, result_page.ResultPage, list_page.ListPage):
            self.frames[F] = F(container, self)
            self.frames[F].grid(row=0, column=0, sticky='nsew')

        self.show_frame( start_page.StartPage)   # first page to show

    def show_frame(self, page):
        self.frames[page].tkraise()
        self.frames[page].animate()


app = GDPRApp()
# app.geometry("900x1450")
app.mainloop()
