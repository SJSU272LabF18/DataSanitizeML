import tkinter as tk
from tkinter import ttk
import start_page
import result_page
import backend

LARGE_FONT = ("Verdana", 12, "bold")
MEDIUM_FONT = ("Verdana", 10)

class ListPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#C6E2FF')
        self.controller = controller

        photo = tk.PhotoImage(file="GDPR_load.png")  # width:533  height:267
        photo = photo.subsample(4)  # zoom
        imageLabel = tk.Label(self, image=photo, bg='#C6E2FF')
        imageLabel.image = photo
        imageLabel.grid(row=0, column=0, sticky='W', padx=(20, 0))

        resTitlelabel = tk.Label(self, text="Suspected Data", font=("Verdana", 20, "bold"), bg='#C6E2FF', fg='darkblue')
        resTitlelabel.grid(row=0, column=0, padx=(340, 0), sticky='w')

     # table
        self.tbTitlelabel = tk.Label(self, text="TableName", font=("Verdana", 12, "bold"), bg='#C6E2FF', fg='darkblue')
        self.tbTitlelabel.grid(row=1, column=0, padx=(120, 0), sticky='w')

        self.preLabel = tk.Button(self, text="Previous Table", font=("Verdana", 13, "bold"), bg='#C6E2FF', fg='darkblue', command=lambda:self.previousTable() )   # if call the function by the button, the table width change.
        self.preLabel.grid(row=1, column=0, padx=(0, 155), sticky='e')

        self.nextLabel = tk.Button(self, text="Next Table", font=("Verdana", 13, "bold"), bg='#C6E2FF', fg='darkblue',command=lambda:self.nextTable())
        self.nextLabel.grid(row=1, column=0, padx=(0, 35), sticky='e')

        self.upButton = tk.Button(self, text="^", font=("Verdana", 13, "bold"), bg='#C6E2FF', fg='darkblue', command=lambda:self.moveUp())
        self.upButton.grid(row=1, column=0, padx=(0, 0), sticky='e')

        #table position

        self.returnButton = tk.Button(self, text="Return", font=("Verdana", 15, "bold"), bg='#C6E2FF', fg='darkblue', command=lambda: self.returnFunc())
        self.returnButton.grid(row=3, column=0, padx=(120, 0), pady=(20, 0), sticky='w')

        self.homeButton = tk.Button(self, text="Home Page", font=("Verdana", 15, "bold"), bg='#C6E2FF', fg='darkblue', command=lambda: controller.show_frame(start_page.StartPage))
        self.homeButton.grid(row=3, column=0, padx=(218, 0), pady=(20, 0), sticky='w')

        self.deleteButton = tk.Button(self, text="Delete Highlighted Data", font=("Verdana", 15, "bold"), bg='#C6E2FF', fg='darkblue', command=lambda:self.deleteData()  )
        self.deleteButton.grid(row=3, column=0, padx=(430, 0), pady=(20, 0), sticky='w')

    def animate(self):
        self.table_list = backend.result.table_list
        self.table_index = 0
        self.col_start_pos = 0
        # self.tree.destroy()
        self.showTable()

    def nextTable(self):
        if self.table_index < len(self.table_list)-1:
            self.table_index += 1
            # self.tree.destroy()
            self.showTable()
        else:
            tk.messagebox.showinfo("GDPR Message", "No More Data.")

    def previousTable(self):
        if self.table_index > 0:
            self.table_index -= 1
            self.tree.destroy()
            self.showTable()
        else:
            tk.messagebox.showinfo("GDPR Message", "No More Data.")

    def showTable(self):
        print('run show table')

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Verdana", 15))
        self.tree = ttk.Treeview(self, height=10, show = 'headings', selectmode='extended')
        self.tree.grid(row=2, column=0, columnspan=1, padx=(120, 0), sticky='nsew')

        ysb = ttk.Scrollbar(self, orient='vertical', command=self.tree.yview)
        self.tree['yscroll'] = ysb.set
        ysb.configure(command=self.tree.yview)
        ysb.grid(row=2, column=1, sticky='wns')

        xsb = ttk.Scrollbar(self, orient='horizontal', command=self.tree.yview)
        self.tree['xscroll'] = xsb.set
        xsb.configure(command=self.tree.xview)
        xsb.grid(row=2, column=0, columnspan=1, padx=(120, 0), sticky='wes')

        # for i in self.tree.get_children():
        #     self.tree.delete(i)

        # for l in self.table_list:
        #     print(l)

        if len(self.table_list) > self.table_index:
            table_item = self.table_list[self.table_index]
            self.tbTitlelabel['text'] = 'Table:'+ table_item.table_name
            col_name = table_item.col_name[self.col_start_pos:]
            print('cloumn num',len(col_name))
            self.tree['columns'] = col_name
            data_list = table_item.data_list

            for col in col_name:
                self.tree.heading(col, text=col)
                self.tree.column(col, width= int(580 / len(col_name)), minwidth=0, anchor='center')

            for list in data_list:
                # print('insert', list[self.col_start_pos:] )
                self.tree.insert('', 'end', values = list[self.col_start_pos:] )

    def moveUp(self):
        selection = self.tree.selection()
        if selection != ():
            table_item = self.table_list[self.table_index]

            for dic in selection:
                # print('select', self.tree.item(dic)['values'])
                row = self.toString(self.tree.item(dic)['values'])
                # print('converted to', row)
                table_item.data_list.remove(row)

            remain = list(table_item.data_list)
            self.table_list[self.table_index].data_list.clear()

            for dic in selection:
                self.table_list[self.table_index].data_list.append( self.toString(self.tree.item(dic)['values']) )

            self.table_list[self.table_index].data_list += remain
            self.tree.destroy()
            self.showTable()

    def deleteData(self):
        selection = self.tree.selection()
        if selection == ():
            tk.messagebox.showinfo("GDPR Message", "No Data Row is Selected.")
        else:
            answer = tk.messagebox.askquestion("GDPR Message", "Are you sure to delete the highlighted data row, Click 'yes' to continue ?")
            if answer == 'yes':
                table_item = self.table_list[self.table_index]
                toDelete_data_list = []
                for dic in selection:
                    # print('delete data row', self.tree.item(dic)['values'])
                    row = self.toString( self.tree.item(dic)['values'])
                    # print('converted to', row)
                    table_item.data_list.remove( row )
                    toDelete_data_list.append( row )
                    self.tree.delete(dic)
                # for l in  table_item.data_list:
                #     print('after delete',l)

                toDelete_table_item = backend.algo.Table_Item(table_item.table_name, table_item.col_name[self.col_start_pos:],toDelete_data_list)
                backend.deleteDataRow(toDelete_table_item)

    def returnFunc(self):
        self.tree.destroy()
        self.controller.show_frame(result_page.ResultPage)

    # when data row is taken from treeview, all numeric data in String type changed to Numeric Type. and so, change it back to Stirng
    def toString(self, list):
        new_list = []
        for l in list:
            new_list.append(str(l))
        return new_list;

