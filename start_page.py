import tkinter as tk
import tkinter.messagebox
import load_page
import backend

LARGE_FONT = ("Verdana", 12, "bold")
MEDIUM_FONT = ("Verdana", 10)

class StartPage(tk.Frame):
    conn = False

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg='#C6E2FF')
        self.controller = controller

        photo = tk.PhotoImage(file="GDPR_logo.png")  # width:533  height:267
        imageLabel = tk.Label(self, image=photo)
        imageLabel.image = photo
        imageLabel.grid(row=0, column=0, padx=(40,10), pady=(30,10), rowspan=5)

        ipLabel = tk.Label(self, text="IP", font = LARGE_FONT,bg='#C6E2FF',fg='darkblue')
        ipLabel.grid(row=0, column=1,sticky='W', pady=(30,0))
        self.ipEntry = tk.Entry(self,font=("Verdana", 10), width=15)
        self.ipEntry.grid(row=0, column=2, padx=(20,40), pady=(30,0))

        portLabel = tk.Label(self, text="Port", font = LARGE_FONT,bg='#C6E2FF',fg='darkblue')
        portLabel.grid(row=1, column=1,sticky='W')
        self.portEntry = tk.Entry(self,font=("Verdana", 10), width=15)
        self.portEntry.grid(row=1, column=2, padx=(20,40))

        dbLabel = tk.Label(self, text="Database", font = LARGE_FONT,bg='#C6E2FF',fg='darkblue')
        dbLabel.grid(row=2, column=1,sticky='W')
        self.dbEntry = tk.Entry(self,font=("Verdana", 10), width=15)
        self.dbEntry.grid(row=2, column=2, padx=(20,40))

        userLabel = tk.Label(self, text="Username", font = LARGE_FONT,bg='#C6E2FF',fg='darkblue')
        userLabel.grid(row=3, column=1,sticky='W')
        self.userEntry = tk.Entry(self,font=("Verdana", 10), width=15)
        self.userEntry.grid(row=3, column=2, padx=(20,40))

        psLabel = tk.Label(self, text="Password", font=LARGE_FONT,bg='#C6E2FF',fg='darkblue')
        psLabel.grid(row=4, column=1,sticky='W')
        self.psEntry = tk.Entry(self,font=("Verdana", 10), width=15)
        self.psEntry.grid(row=4, column=2, padx=(20,40))

    #bottom part
        kwLabel = tk.Label(self, text="Key Words", font = LARGE_FONT,bg='#C6E2FF',fg='darkblue')
        kwLabel.grid(row=6, column=0, sticky='W',padx=(40,0), pady=(20,0))
        self.kwEntry = tk.Entry(self,font = ("Verdana", 10),width=43)
        self.kwEntry.grid(row=6, column=0, columnspan=2,sticky='W',padx=(230,0), pady=(20,0))

        resLabel = tk.Label(self, text="Result File Location", font = LARGE_FONT,bg='#C6E2FF',fg='darkblue')
        resLabel.grid(row=7, column=0,sticky='W',padx=(40,0))
        self.resButton = tk.Button(self, text="Click to add (Optional)",font = ("Verdana", 11, "bold"),width=34,relief="groove", command=lambda:controller.show_frame(load_page.LoadPage))
        self.resButton.grid(row=7, column=0, columnspan=2,sticky='W',pady=(10,20),padx=(230,0))

    #
        self.connButton = tk.Button(self, text="Connect to DB", font=("Verdana", 12, "bold"),fg='black',command=lambda:self.connectToDB())
        self.connButton.grid(row=6, column=1,rowspan=2,columnspan=2, padx=(20,40),pady=(0,60))

        self.scanButton = tk.Button(self, text="SCAN", font=("Verdana", 25, "bold"),fg='black',command=lambda:self.startScan())
        self.scanButton.grid(row=7, column=1,rowspan=2,columnspan=2, padx=(20,40),pady=(30,30))

    def animate(self):
        print('start')
        self.ipEntry.insert(tk.END, '127.0.0.1')
        self.portEntry.insert(tk.END, '3306')
        self.dbEntry.insert(tk.END, 'gdpr_sanitization')
        self.userEntry.insert(tk.END, 'root')
        self.psEntry.insert(tk.END, 'root')

    def connectToDB(self):
        if not self.conn:
            if self.ipEntry.get() is '' or self.dbEntry.get() is '' or self.userEntry.get() is ''or self.psEntry.get() is '' or self.portEntry.get() is '':
                tk.messagebox.showinfo("GDPR Message", "Please fill out information for IP, Port, Database, Username and Password.")
            else:
                self.conn = backend.connectToDB(self.ipEntry.get(), self.portEntry.get(), self.dbEntry.get(), self.userEntry.get(), self.psEntry.get())
                if self.conn:
                    self.ipEntry.config(state='disabled')
                    self.portEntry.config(state='disabled')
                    self.dbEntry.config(state='disabled')
                    self.userEntry.config(state='disabled')
                    self.psEntry.config(state='disabled')
                    self.connButton.config(relief='sunken', text='DB Connected')  # = button[relief] = 'sunken'
                    tk.messagebox.showinfo("GDPR Message", "Database Connection is Successful !")
                else:
                    tk.messagebox.showinfo("GDPR Message", "Database Connection is Failed. Please check IP, Port, Database, Username and Password information.")
        else:
            self.conn = False
            self.ipEntry.config(state='normal')
            self.portEntry.config(state='normal')
            self.dbEntry.config(state='normal')
            self.userEntry.config(state='normal')
            self.psEntry.config(state='normal')
            self.connButton.config(relief='raised', text='Connect to DB')

    def startScan(self):
        if not self.conn:
            tk.messagebox.showinfo("GDPR Message", "Please Connect to Database First.")
        elif(self.kwEntry.get() is '' ):
            tk.messagebox.showinfo("GDPR Message", "Please Enter Key Words to Start Scanning.")
        else:
            answer = tk.messagebox.askquestion("GDPR Message", "It is going to take a while to scan the database. Are you sure to continue ?")
            if answer == 'yes':
                print('enter load')
                backend.Scan(self.kwEntry.get()).start()
                self.controller.show_frame(load_page.LoadPage)
