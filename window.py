import tkinter as tk
from tkinter import ttk
import os, datetime, getpass

class Window:
    def __init__(self, master):
        self.master = master
        self.master.title('Test for UBISOFT')
        self.master.geometry('600x300+200+100')
        self.choiceCombo = False
        self.directory = os.getcwd() + '\\unused'
        self.files = os.listdir(self.directory)
        self.files_names = [name.split('.')[0] for name in self.files]
        self.labKeysBatch = tk.Label(self.master, text='Keys Batch').place(x=10, y=10, width=80)
        self.combobox = ttk.Combobox(self.master, values=self.files_names, state='readonly')
        self.combobox.place(x=90, y=10, width=400)
        self.butGet = tk.Button(self.master, text='Get')
        self.butGet.place(x=90, y=60, width=150)
        self.butCancel = tk.Button(self.master, text='Cancel')
        self.butCancel.place(x=250, y=60, width=150)
        self.text1 = tk.Text(self.master)
        self.text1.place(x=0, y=120, height=180, width=700)
        self.butGet.bind('<Button-1>', self.pressGet)
        self.butCancel.bind('<Button-1>', self.pressCancel)
        self.combobox.bind("<<ComboboxSelected>>", self.choiceCombobox)
        self.master.mainloop()

    def choiceCombobox(self, event):
        if self.choiceCombo:
            self.text1.delete(1.0, tk.END)
        self.choiceCombo = True
        f = open(self.get_choice_file(), 'r')
        line = f.readline()
        self.text1.insert(1.0, line)
        f.close()

    def pressGet(self, event):
        if self.choiceCombo:
            file_name = self.combobox.get()
            new_f_name = self.directory + '\\' + file_name + '_new.txt'
            used_file = os.getcwd() + '\\used\\' + file_name + '_used.txt'
            time_format = "%Y-%m-%d %H:%M:%S"
            with open(self.get_choice_file(), 'r') as f, open(new_f_name, 'w') as f1:
                line = f.readline()
                used_f = open(used_file, 'a')
                date = datetime.datetime.today()
                if line[len(line) - 1:len(line)] == '\n':
                    line = line[:len(line) - 1]
                # if line[len(line) - 1:len(line)] != '\n':
                #     line = line[:len(line)] + '\n'
                used_f.writelines(line + '-' + getpass.getuser() + '-' + f"{date:{time_format}}" + '\n')
                used_f.close()
                for line in f:
                    f1.write(line)
            f.close()
            f1.close()
            os.remove(self.get_choice_file())
            os.rename(new_f_name, self.get_choice_file())
            self.choiceCombobox('')

    def pressCancel(self, event):
        self.master.destroy()

    def get_choice_file(self):
        file_name = self.combobox.get()
        index_f = self.files_names.index(file_name)
        nameFiles = (self.files[index_f])
        old_f_name = self.directory + '\\' + nameFiles
        return old_f_name