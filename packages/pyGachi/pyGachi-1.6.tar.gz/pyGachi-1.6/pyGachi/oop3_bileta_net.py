import tkinter as tk
from tkinter import messagebox
import csv


class HousingManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Оплата ЖКХ")

        # Создание элементов интерфейса
        self.label = tk.Label(root, text="Владельцы квартир")
        self.label.pack()

        self.listbox = tk.Listbox(root, width=50)
        self.listbox.pack()

        self.entry = tk.Entry(root, width=50)
        self.entry.pack()

        self.add_button = tk.Button(root, text="Добавить", command=self.add_record)
        self.add_button.pack()

        self.edit_button = tk.Button(root, text="Редактировать", command=self.edit_record)
        self.edit_button.pack()

        self.delete_button = tk.Button(root, text="Удалить", command=self.delete_record)
        self.delete_button.pack()

        self.search_button = tk.Button(root, text="Поиск", command=self.search_record)
        self.search_button.pack()

        self.save_button = tk.Button(root, text="Сохранить", command=self.save_records)
        self.save_button.pack()

        self.load_button = tk.Button(root, text="Загрузить", command=self.load_records)
        self.load_button.pack()

        # Загрузка данных из файла (если есть)
        self.load_records()

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for record in self.records:
            self.listbox.insert(tk.END, record)

    def add_record(self):
        new_record = self.entry.get()
        if new_record:
            self.records.append(new_record)
            self.update_listbox()
            self.entry.delete(0, tk.END)

    def edit_record(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            new_record = self.entry.get()
            if new_record:
                self.records[selected_index] = new_record
                self.update_listbox()
                self.entry.delete(0, tk.END)

    def delete_record(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            confirmation = messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить запись?")
            if confirmation:
                del self.records[selected_index]
                self.update_listbox()

    def search_record(self):
        search_query = self.entry.get()
        if search_query:
            search_results = [record for record in self.records if search_query in record]
            self.listbox.delete(0, tk.END)
            for result in search_results:
                self.listbox.insert(tk.END, result)

    def save_records(self):
        file_name = "housing_records.txt"
        try:
            with open(file_name, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(self.records)
            messagebox.showinfo("Сохранение", "Данные успешно сохранены в файле " + file_name)
        except Exception as e:
            messagebox.showerror("Ошибка", "Не удалось сохранить данные: " + str(e))

    def load_records(self):
        file_name = "housing_records.txt"
        try:
            with open(file_name, "r") as file:
                reader = csv.reader(file)
                self.records = list(reader)
            self.update_listbox()
            messagebox.showinfo("Загрузка", "Данные успешно загружены из файла " + file_name)
        except FileNotFoundError:
            self.records = []
            messagebox.showinfo("Загрузка", "Файл " + file_name + " не найден")
        except Exception as e:
            messagebox.showerror("Ошибка", "Не удалось загрузить данные: " + str(e))


root = tk.Tk()
app = HousingManagementApp(root)
root.mainloop()