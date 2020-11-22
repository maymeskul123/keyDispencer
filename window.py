import tkinter as tk
from tkinter import ttk
import os, datetime, getpass

class Window:
    def __init__(self, master):
        self.master = master
        self.master.title('Test for UBISOFT')
        self.master.geometry('600x300+200+100')
        self.choiceCombo = False
        self.found_key = False
        self.current_given_file = ''
        self.directory_unused = os.getcwd() + '\\unused'
        self.directory_used = os.getcwd() + '\\used'
        self.files = os.listdir(self.directory_unused)
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
        line = self.normalizeLine(line)
        self.text1.insert(1.0, line)
        f.close()

    def pressGet(self, event):
        code = self.text1.get(1.0, tk.END)
        if self.choiceCombo and self.found_key and code !='\n' and code !='':
            file_name = self.combobox.get()
            used_file = self.directory_used + '\\' + file_name + '_used.txt'
            self.del_line_unused(self.check_given_away_code(code[:len(code) - 1], used_file), used_file)
            self.choiceCombobox('')

    def del_line_unused(self, add_to_used, used_file):
        buf = list()
        with open(self.get_choice_file(), 'r') as f:
            for line_f in f:
                buf.append(line_f)
        f.close()
        line = buf[0]
        del buf[0]
        file = open(self.get_choice_file(), 'w')
        file.writelines(buf)
        file.close()
        if add_to_used:
            self.app_to_used(used_file, self.normalizeLine(line))

    def app_to_used(self, used_file, line):
        time_format = "%Y-%m-%d %H:%M:%S"
        used_f = open(used_file, 'a')
        date = datetime.datetime.today()
        used_f.writelines(line + '-' + getpass.getuser() + '-' + f"{date:{time_format}}" + '\n')
        used_f.close()

    def pressCancel(self, event):
        self.master.destroy()

    def get_choice_file(self):
        file_name = self.combobox.get()
        index_f = self.files_names.index(file_name)
        nameFiles = (self.files[index_f])
        old_f_name = self.directory_unused + '\\' + nameFiles
        return old_f_name

    def normalizeLine(self, line):
        if line.find('\n') > 0:
            line = line.replace('\n', '')
        if line.find('-') > 0:
            line = line.replace('-', ' ')
        self.found_key = True
        return line

    def check_given_away_code(self, code, used_f):
        key_add = True
        if os.path.exists(used_f):
            with open(used_f, 'r') as f:
                for line in f:
                    if line[:15] == code:
                        key_add = False
                        break
        return key_add
