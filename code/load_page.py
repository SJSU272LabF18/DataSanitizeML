import tkinter as tk
import time
import start_page
import result_page
import backend

LARGE_FONT = ("Verdana", 12, "bold")
MEDIUM_FONT = ("Verdana", 10)

class LoadPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#C6E2FF')
        self.controller = controller

        photo = tk.PhotoImage(file="GDPR_load.png")  # width:533  height:267
        photo = photo.subsample(2)  #zoom
        imageLabel = tk.Label(self, image=photo,bg='#C6E2FF')
        imageLabel.image = photo
        imageLabel.grid(row=0, column=0, padx=(230,0))

        self.label = tk.Label(self, text="Processing...", font=("Verdana", 18, "bold"),bg='#C6E2FF',fg='darkblue' )
        self.label.grid(row=1, column=0, padx=(250,0))

        button1 = tk.Button(self, text="Abort",font=("Verdana", 12, "bold"), command=lambda: self.abort())
        button1.grid(row=2, column=0,padx=(230,0), pady=(40,0))

        # button1 = tk.Button(self, text="result",font=("Verdana", 12, "bold"), command=lambda: controller.show_frame(result_page.ResultPage))
        # button1.grid(row=3, column=0,padx=(230,0), pady=(40,0))

    def animate(self):
        c1 = tk.Canvas(self, bg="yellow", highlightthickness=0, width=5, height=5)
        c1.grid(row=0, column=0, padx=(17,1), pady=(7,0))
        c2 = tk.Canvas(self, bg="yellow", highlightthickness=0, width=5, height=4)
        c2.grid(row=0, column=0, padx=(146,1), pady=(70,0))
        c3 = tk.Canvas(self, bg="yellow", highlightthickness=0, width=5, height=4)
        c3.grid(row=0, column=0, padx=(296,1), pady=(0,70))
        c4 = tk.Canvas(self, bg="yellow", highlightthickness=0, width=5, height=4)
        c4.grid(row=0, column=0, padx=(475,1), pady=(69,0))

        while backend.finish == False:
            c1["bg"] = "White"
            c1.update()
            c2["bg"] = "white"
            c2.update()
            c3["bg"] = "white"
            c3.update()
            c4["bg"] = "white"
            c4.update()
            self.label['fg'] = "deep sky blue"
            time.sleep(1)

            c1["bg"] = "light goldenrod"
            c1.update()
            c2["bg"] = "light goldenrod"
            c2.update()
            c3["bg"] = "light goldenrod"
            c3.update()
            c4["bg"] = "light goldenrod"
            c4.update()
            self.label['fg'] = "blue1"
            time.sleep(1)

            c1["bg"] = "yellow"
            c1.update()
            c2["bg"] = "yellow"
            c2.update()
            c3["bg"] = "yellow"
            c3.update()
            c4["bg"] = "yellow"
            c4.update()
            self.label['fg'] = "dark blue"
            time.sleep(1)

        self.controller.show_frame( result_page.ResultPage)


    def abort(self):
        backend.abort = True
        self.controller.show_frame( start_page.StartPage)

