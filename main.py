from tkinter import *
from tkinter import ttk
import tkinter.font as font
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import re
import google_sheet
import os
import webbrowser



def main():
    root = Tk()
    gui = Window(root)
    gui.root.mainloop()
    return None


class Window:
    def __init__(self, root):
        self.user_pdf_name = None
        self.electric_current = None
        self.electrical_resistance = None
        self.time_value = None
        self.energy = None
        self.current_date = None
        self.df = pd.DataFrame()
        self.files_in_dir = dict()
        self.path = "test_dir"


        def row_generator(number):
            i = 0
            while i < number:
                yield i
                i += 1

        def create_entry_field(description, default_text=""):
            r = next(row)
            Label(self.root, text=description, font=("Helvetica", 14)).grid(row=r, column=0)
            temp = Entry(self.root, width=width)
            temp.insert(END, default_text)
            temp.grid(row=r, column=1)
            return temp

        row = row_generator(20)
        self.root = root
        self.root.title("Лабораторная работа № 6")
        self.root.geometry('600x720')
        self.root.resizable(False, False)

        width = 40

        r = next(row)
        Label(self.root, text="Вычисление работы тока", font=("Helvetica", 24)).grid(row=r, column=0, padx=120, pady=40,
                                                                                     columnspan=2)

        self.user_pdf_name_entry = create_entry_field("Название pdf", "Работа тока")
        self.electric_current_entry = create_entry_field("Сила тока")
        self.electrical_resistance_entry = create_entry_field("Сопротивление")
        self.time_value_entry = create_entry_field("Время")

        r = next(row)
        self.error_label_text = StringVar()
        self.error_label_text.set("")
        self.error_label = Label(self.root, textvariable=self.error_label_text, font=('Arial', 9, 'bold'))
        self.error_label.grid(row=r, column=0, columnspan=2, stick='we')

        r = next(row)
        button1 = Button(self.root, text="Calculate", command=self.data_validation, background='#D3CBBD', height=1,
                         width=30, activebackground='#B8B1A5', font=font.Font(size=12), )
        button1.grid(row=r, column=0, columnspan=2, pady=10)
        self.root.bind("<Return>", self.data_validation)



        r = next(row)
        Label(self.root, text="Открыть файл", font=("Helvetica", 20)).grid(row=r, column=0, padx=120, pady=40,
                                                                                     columnspan=2)


        r = next(row)
        Label(self.root, text="Выберите файл", font=("Helvetica", 14)).grid(row=r, column=0)
        self.update_files_in_dir()
        self.file_name_combobox = ttk.Combobox(self.root, width=width, values= list(self.files_in_dir.keys()), postcommand=self.refresh_combobox)
        self.file_name_combobox.current(0)
        self.file_name_combobox.grid(row=r, column=1)


        r = next(row)
        open_button = Button(self.root, text="Открыть файл", command=self.open_file, background='#D3CBBD', height=1,
                         width=30, activebackground='#B8B1A5', font=font.Font(size=12), )
        open_button.grid(row=r, column=0, columnspan=2, pady=10)
        self.root.bind("<Return>", self.open_file)

    def open_file(self):
        webbrowser.open_new(self.files_in_dir[self.file_name_combobox.get()])
        pass

    def refresh_combobox(self):
        self.update_files_in_dir()
        self.file_name_combobox["values"] = list(self.files_in_dir.keys())

    def update_files_in_dir(self):
        self.files_in_dir = dict()
        for root, dirs, files in os.walk(self.path):
            for file in files:
                if (file.endswith(".pdf")):
                    file_name_full = os.path.join(root, file)
                    file_name = file_name_full[len(self.path)+12:-4].replace('_', ' ')
                    self.files_in_dir[file_name] = file_name_full


    def get_valid_filename(self, name):
        # Надо переделать или отказаться
        name = name.strip().replace(' ', '_')
        result = re.findall(r'([А-ЯA-Za-zа-яё_\d]+)', str(name))
        if len(result) > 0:
            print(result)
            return result[0]
        print("Пустое имя файла")
        return ""

    def data_validation(self):
        er_color = '#D3CBBD'

        values = [self.electric_current_entry,
                  self.electrical_resistance_entry,
                  self.time_value_entry]
        incorrect = False
        for elem in values:
            num = elem.get()
            try:
                float(num)
            except:
                incorrect = True
                break

        if incorrect or len(self.get_valid_filename(self.user_pdf_name_entry.get())) == 0:
            self.error_label_text.set("Некорректные данные, проверьте ввод")
            self.error_label.config(bg=er_color)
        else:
            self.update_data()

    def update_data(self):
        self.user_pdf_name = self.get_valid_filename(self.user_pdf_name_entry.get())
        self.electric_current = float(self.electric_current_entry.get())
        self.electrical_resistance = float(self.electrical_resistance_entry.get())
        self.time_value = float(self.time_value_entry.get())
        self.energy = self.electric_current ** 2 * self.electrical_resistance * self.time_value
        self.current_date = re.findall(r'\d{4}-\d{2}-\d{2}', str(datetime.now()))[0]

        self.save_values()

    def save_values(self):
        table_name = self.user_pdf_name_entry.get().replace(' ', '\\ ')
        d = {f'$\\bf{table_name}$': ["", "A", "I", "R", "t"],
             "": ["",
                  self.energy,
                  self.electric_current,
                  self.electrical_resistance,
                  self.time_value],
             f'$\\bf{self.current_date}$': ["",
                                            r'$\mathit{Работа}$' + ' ' + r'$\mathit{тока}$',
                                            r'$\mathit{Сила}$' + ' ' + r'$\mathit{тока}$',
                                            r'$\mathit{Сопротивление}$' + ' ' + r'$\mathit{проводника}$',
                                            r'$\mathit{Время}$']}

        self.df = pd.DataFrame(data=d)

        fig, ax = plt.subplots()
        fig.patch.set_visible(False)
        ax.axis('off')
        ax.axis('tight')

        ax.table(cellText=self.df.values, colLabels=self.df.columns, loc='center', colLoc='center', cellLoc='center')

        fig.tight_layout()
        plt.savefig(f'{self.path}\{self.current_date}-{self.user_pdf_name}.pdf')
        plt.show()

        list_data = [[self.user_pdf_name_entry.get(), '', self.current_date],
                     ['', '', ''],
                     ['A', self.energy, 'Работа тока'],
                     ['I', self.electric_current, 'Сила тока'],
                     ['R', self.electrical_resistance, 'Сопротивление проводника'],
                     ['t', self.time_value, 'Время']]
        google_sheet.update_sheet_value(list_data)


        pass

    pass


main()
