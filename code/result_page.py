import tkinter as tk
import tkinter.messagebox
import math
import time
import start_page
import list_page
import backend

LARGE_FONT = ("Verdana", 12, "bold")
MEDIUM_FONT = ("Verdana", 10)
ARROW_WAIT_TIME = 0.005

class ResultPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#C6E2FF')
        self.controller = controller

        photo = tk.PhotoImage(file="GDPR_load.png")  # width:533  height:267
        photo = photo.subsample(4)  #zoom
        imageLabel = tk.Label(self, image=photo,bg='#C6E2FF')
        imageLabel.image = photo
        imageLabel.grid(row=0, column=0, columnspan=2, sticky='W', padx=(20,0))

        resTitlelabel = tk.Label(self, text="RESULT", font=("Verdana", 20, "bold"),bg='#C6E2FF',fg='darkblue' )
        resTitlelabel.grid(row=0, column=1, padx=(370,0))

    # scale 1
        self.c1 = tk.Canvas(self, height=240, width=240,bg='#C6E2FF', highlightthickness=0)
        self.c1.grid(row=1, column=1, padx=(0,60))

        self.goodTbLable = tk.Label(self, text=0, font = LARGE_FONT,bg='#7CFC00')
        self.goodTbLable.grid(row=1, column=1, padx=(0,250), pady=(100,130))

        self.badTbLable = tk.Label(self, text=0, font = LARGE_FONT,bg='red')
        self.badTbLable.grid(row=1, column=1, padx=(130,0), pady=(100,130))

        tbLable = tk.Label(self, text="No. of Tables",font = LARGE_FONT,bg='#C6E2FF')
        tbLable.grid(row=1, column=1, padx=(0,60), pady=(180,100))

    #scale 2
        self.c2 = tk.Canvas(self, height=240, width=240,bg='#C6E2FF', highlightthickness=0)
        self.c2.grid(row=1, column=2, padx=10)

        self.goodColLable = tk.Label(self, text=0, font = LARGE_FONT,bg='#7CFC00')
        self.goodColLable.grid(row=1, column=2, padx=(0,190), pady=(100,130))

        self.badColLable = tk.Label(self, text=0, font = LARGE_FONT,bg='red')
        self.badColLable.grid(row=1, column=2, padx=(190,0), pady=(100,130))

        colLable = tk.Label(self, text="No. of Rows",font = LARGE_FONT,bg='#C6E2FF')
        colLable.grid(row=1, column=2, padx=(0,0), pady=(180,100))

     # timeLabel
        self.timeLabel = tk.Label(self, text="Total Time: 11:11:11", font=LARGE_FONT,bg='#C6E2FF')
        self.timeLabel.grid(row=1, column=1, columnspan=2, padx=(85,0), pady=(200,50))

        detailButton = tk.Button(self, text="See Detailed Result", font=LARGE_FONT, command= lambda: self.showDetailResult() )
        detailButton.grid(row=1, column=1, columnspan=2, padx=(85,0), pady=(290,50))

    def animate(self):
        red1 = backend.result.num_of_bad_table
        green1 = backend.result.num_of_good_table
        red2 = backend.result.num_of_bad_row
        green2 = backend.result.num_of_good_row

        # print('time consumed', backend.result.time)
        self.timeLabel['text'] = "Total Time: " + str(int(backend.result.time/60/60)) + ':'+ str(int(backend.result.time/60 %60)) + ':' + str( int(backend.result.time%60))
        self.goodTbLable['text'] = green1
        self.badTbLable['text'] = red1
        self.goodColLable['text'] = green2
        self.badColLable['text'] = red2
        # if red1+green1 == 0
        # print('green1', green1)
        # print('red1', red1)
        redDegree1 = int( 180 * red1 / (red1 + green1))
        redDegree2 = int( 180 * red2 / (red2 + green2))

        if redDegree1 > redDegree2:
            self.red_samll = redDegree2
            self.red_big = redDegree1
            self.big_angle_canvas = self.c1
            self.small_angle_canvas = self.c2
        else:
            self.red_samll = redDegree1
            self.red_big = redDegree2
            self.big_angle_canvas = self.c2
            self.small_angle_canvas = self.c1

        self.moveBothScale()
        self.moveBigScale()

    def moveBothScale(self):
            for degree in range(0, self.red_samll):
                arcGreen1 = self.big_angle_canvas.create_arc(0, 0, 240, 240, start=180, extent=degree-180, fill="#7CFC00")
                arcRed1 = self.big_angle_canvas.create_arc(0, 0, 240, 240, start=0, extent=degree, fill="red")
                arcCenter1 = self.c1.create_arc(45, 45, 195, 195, start=0, extent=180, fill="#C6E2FF", )
                circle1 = self.c1.create_oval(105, 105, 135, 135, fill="black")
                arrow1 = self.big_angle_canvas.create_line(self.getLinePosition(120,120,90,degree), fill="black", width=5, arrow=tk.LAST, arrowshape=(10,20,8))

                arcGreen2 = self.small_angle_canvas.create_arc(0, 0, 240, 240, start=180, extent=degree-180, fill="#7CFC00")
                arcRed2 = self.small_angle_canvas.create_arc(0, 0, 240, 240, start=0, extent=degree, fill="red")
                arcCenter2 = self.c2.create_arc(45, 45, 195, 195, start=0, extent=180, fill="#C6E2FF", )
                circle2 = self.c2.create_oval(105, 105, 135, 135, fill="black")
                arrow2 = self.small_angle_canvas.create_line(self.getLinePosition(120,120,90,degree), fill="black", width=5, arrow=tk.LAST, arrowshape=(10,20,8))

                time.sleep(ARROW_WAIT_TIME)
                self.big_angle_canvas.update()
                self.small_angle_canvas.update()
                self.big_angle_canvas.delete(arcGreen1)
                self.big_angle_canvas.delete(arcRed1)
                self.big_angle_canvas.delete(arrow1)
                self.big_angle_canvas.delete(arcCenter1)
                self.big_angle_canvas.delete(circle1)

                self.small_angle_canvas.delete(arcGreen2)
                self.small_angle_canvas.delete(arcRed2)
                self.small_angle_canvas.delete(arrow2)
                self.small_angle_canvas.delete(arcCenter2)
                self.small_angle_canvas.delete(circle2)


    def moveBigScale(self):
        self.small_arcGreen_stop = self.small_angle_canvas.create_arc(0, 0, 240, 240, start=180, extent=self.red_samll - 180, fill="#7CFC00")
        self.small_arcRed_stop = self.small_angle_canvas.create_arc(0, 0, 240, 240, start=0, extent=self.red_samll, fill="red")
        self.small_arcCenter_stop = self.small_angle_canvas.create_arc(45, 45, 195, 195, start=0, extent=180, fill="#C6E2FF", )
        self.small_circle_stop = self.small_angle_canvas.create_oval(105, 105, 135, 135, fill="black")
        self.small_arrow_stop = self.small_angle_canvas.create_line(self.getLinePosition(120, 120, 90, self.red_samll), fill="black", width=5, arrow=tk.LAST, arrowshape=(10, 20, 8))

        for degree in range(self.red_samll, self.red_big):
            arcGreen = self.big_angle_canvas.create_arc(0, 0, 240, 240, start=180, extent=degree - 180, fill="#7CFC00")
            arcRed = self.big_angle_canvas.create_arc(0, 0, 240, 240, start=0, extent=degree, fill="red")
            arcCenter= self.big_angle_canvas.create_arc(45, 45, 195, 195, start=0, extent=180, fill="#C6E2FF", )
            circle= self.big_angle_canvas.create_oval(105, 105, 135, 135, fill="black")
            arrow  = self.big_angle_canvas.create_line(self.getLinePosition(120, 120, 90, degree), fill="black", width=5, arrow=tk.LAST, arrowshape=(10, 20, 8))

            time.sleep(ARROW_WAIT_TIME)
            self.big_angle_canvas.update()
            self.big_angle_canvas.delete(arcGreen)
            self.big_angle_canvas.delete(arcRed)
            self.big_angle_canvas.delete(arcCenter)
            self.big_angle_canvas.delete(circle)
            self.big_angle_canvas.delete(arrow)

        self.big_arcGreen_stop = self.big_angle_canvas.create_arc(0, 0, 240, 240, start=180, extent=self.red_big - 180, fill="#7CFC00")
        self.big_arcRed_stop = self.big_angle_canvas.create_arc(0, 0, 240, 240, start=0, extent=self.red_big, fill="red")
        self.big_arcCenter_stop = self.big_angle_canvas.create_arc(45, 45, 195, 195, start=0, extent=180, fill="#C6E2FF", )
        self.big_circle_stop = self.big_angle_canvas.create_oval(105, 105, 135, 135, fill="black")
        self.big_arrow_stop = self.big_angle_canvas.create_line(self.getLinePosition(120, 120, 90, self.red_big), fill="black", width=5, arrow=tk.LAST, arrowshape=(10, 20, 8))

    def deleteStopGraph(self):
        self.big_angle_canvas.delete(self.big_arcGreen_stop)
        self.big_angle_canvas.delete(self.big_arcRed_stop)
        self.big_angle_canvas.delete(self.big_arrow_stop)
        self.big_angle_canvas.delete(self.big_arcCenter_stop)
        self.big_angle_canvas.delete(self.big_circle_stop)

        self.small_angle_canvas.delete(self.small_arcGreen_stop)
        self.small_angle_canvas.delete(self.small_arcRed_stop)
        self.small_angle_canvas.delete(self.small_arrow_stop)
        self.small_angle_canvas.delete(self.small_arcCenter_stop)
        self.small_angle_canvas.delete(self.small_circle_stop)

    def getLinePosition(self, x, y, radius, redRatio):
        xx = x + radius* math.cos(math.radians(redRatio))
        yy = y - radius* math.sin(math.radians(redRatio))
        return x,y,xx, yy;

    def showDetailResult(self):
        if backend.result.num_of_bad_table > 0:
            self.deleteStopGraph()
            self.controller.show_frame(list_page.ListPage)
        else:
            tk.messagebox.showinfo("GDPR Message", "All data is clean. Go to Home Page")
            self.controller.show_frame( start_page.StartPage)

