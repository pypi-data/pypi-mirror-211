import tkinter as tk
from tkinter import messagebox
import csv


class PhoneBookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Телефонная книга")

        # Создание элементов интерфейса
        self.label = tk.Label(root, text="Телефонная книга")
        self.label.pack()

        self.listbox = tk.Listbox(root, width=50)
        self.listbox.pack()

        self.entry_name = tk.Entry(root, width=30)
        self.entry_name.pack()

        self.entry_phone = tk.Entry(root, width=30)
        self.entry_phone.pack()

        self.add_button = tk.Button(root, text="Добавить", command=self.add_entry)
        self.add_button.pack()

        self.edit_button = tk.Button(root, text="Редактировать", command=self.edit_entry)
        self.edit_button.pack()

        self.delete_button = tk.Button(root, text="Удалить", command=self.delete_entry)
        self.delete_button.pack()

        self.search_button = tk.Button(root, text="Поиск", command=self.search_entries)
        self.search_button.pack()

        self.save_button = tk.Button(root, text="Сохранить", command=self.save_entries)
        self.save_button.pack()

        self.load_button = tk.Button(root, text="Загрузить", command=self.load_entries)
        self.load_button.pack()

        # Загрузка данных из файла (если есть)
        self.load_entries()

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for entry in self.entries:
            self.listbox.insert(tk.END, f"{entry['name']}: {entry['phone']}")

    def add_entry(self):
        name = self.entry_name.get()
        phone = self.entry_phone.get()
        if name and phone:
            new_entry = {'name': name, 'phone': phone}
            self.entries.append(new_entry)
            self.update_listbox()
            self.entry_name.delete(0, tk.END)
            self.entry_phone.delete(0, tk.END)

    def edit_entry(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            name = self.entry_name.get()
            phone = self.entry_phone.get()
            if name and phone:
                self.entries[selected_index]['name'] = name
                self.entries[selected_index]['phone'] = phone
                self.update_listbox()
                self.entry_name.delete(0, tk.END)
                self.entry_phone.delete(0, tk.END)

    def delete_entry(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            confirmation = messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить запись?")
            if confirmation:
                del self.entries[selected_index]
                self.update_listbox()

    def search_entries(self):
        search_query = self.entry_name.get()
        if search_query:
            search_results = [entry for entry in self.entries if search_query.lower() in entry['name'].lower()]
            self.listbox.delete(0, tk.END)
            for entry in search_results:
                self.listbox.insert(tk.END, f"{entry['name']}: {entry['phone']}")
        else:
            self.update_listbox()

    def save_entries(self):
        file_name = "phonebook.txt"
        try:
            with open(file_name, "w", newline="") as file:
                writer = csv.writer(file)
                for entry in self.entries:
                    writer.writerow([entry['name'], entry['phone']])
            messagebox.showinfo("Сохранение", "Данные успешно сохранены в файле " + file_name)
        except Exception as e:
            messagebox.showerror("Ошибка", "Не удалось сохранить данные: " + str(e))

    def load_entries(self):
        file_name = "phonebook.txt"
        try:
            with open(file_name, "r") as file:
                reader = csv.reader(file)
                self.entries = [{'name': row[0], 'phone': row[1]} for row in reader]
            self.update_listbox()
            messagebox.showinfo("Загрузка", "Данные успешно загружены из файла " + file_name)
        except FileNotFoundError:
            self.entries = []
            messagebox.showinfo("Загрузка", "Файл " + file_name + " не найден")
        except Exception as e:
            messagebox.showerror("Ошибка", "Не удалось загрузить данные: " + str(e))


root = tk.Tk()
app = PhoneBookApp(root)
root.mainloop()
