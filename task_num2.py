import json
import os

class Book:
    def __init__(self, title, author, description="", is_read=False, is_favorite=False):
        self.title = title
        self.author = author
        self.description = description
        self.is_read = is_read
        self.is_favorite = is_favorite

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def from_dict(data):
        return Book(**data)


class Library:
    def __init__(self, filename="library.json"):
        self.filename = filename
        self.books = []
        self.load()

    def add_book(self, book):
        self.books.append(book)
        self.save()

    def remove_book(self, index):
        if 0 <= index < len(self.books):
            del self.books[index]
            self.save()

    def save(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump([b.to_dict() for b in self.books], f, ensure_ascii=False, indent=4)

    def load(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding="utf-8") as f:
                self.books = [Book.from_dict(b) for b in json.load(f)]

    def search(self, keyword):
        keyword = keyword.lower()
        return [
            b for b in self.books
            if keyword in b.title.lower()
            or keyword in b.author.lower()
            or keyword in b.description.lower()
        ]

library = Library()

import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
icon = tk.PhotoImage(file='icon.png')
root.iconphoto(False, icon)
root.title('Т-Библиотека')
root.geometry('700x700+500+200')

title_label = tk.Label(root, text="Ваша библиотека",
                       font=('Times New Roman', 20),
                       anchor='center')
title_label.pack()

listbox = tk.Listbox(root, width=80, height=20)
listbox.pack(pady=10)


def refresh_list():
    listbox.delete(0, tk.END)
    for i, b in enumerate(library.books):
        status = "✓" if b.is_read else "✗"
        fav = "★" if b.is_favorite else ""
        listbox.insert(tk.END, f"{i}. {b.title} — {b.author} [{status}] {fav}")

def add_book():
    title = title_entry.get()
    author = author_entry.get()


    if not title or not author:
        messagebox.showwarning("Ошибка", "Введите название и автора")
        return

    book = Book(title, author)
    library.add_book(book)

    refresh_list()

def delete_book():
    selected = listbox.curselection()
    if not selected:
        messagebox.showinfo("Инфо", "Выберите книгу")
        return

    index = selected[0]

    confirm = messagebox.askyesno("Удаление", "Удалить книгу?")
    if confirm:
        library.remove_book(index)
        refresh_list()

def toggle_read():
    try:
        index = listbox.curselection()[0]
    except IndexError:
        messagebox.showwarning("Ошибка", "Сначала выбери книгу")
        return

    book = library.books[index]
    book.is_read = not book.is_read
    library.save()
    refresh_list()

def toggle_favorite():
    try:
        index = listbox.curselection()[0]
    except IndexError:
        messagebox.showwarning("Ошибка", "Сначала выбери книгу")
        return

    book = library.books[index]
    book.is_favorite = not book.is_favorite
    library.save()
    refresh_list()

title_entry = tk.Entry(root, width=40)
title_entry.pack()
title_entry.insert(0, "Название")

author_entry = tk.Entry(root, width=40)
author_entry.pack()
author_entry.insert(0, "Автор")


tk.Button(root, text="Добавить книгу", command=add_book).pack(pady=5)
tk.Button(root, text="Удалить книгу", command=delete_book).pack(pady=5)
tk.Button(root, text="Прочитано / Не прочитано", command=toggle_read).pack(pady=5)
tk.Button(root, text="В избранное", command=toggle_favorite).pack(pady=5)

refresh_list()

root.mainloop()