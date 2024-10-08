import tkinter as tk
import os
from tkinter import filedialog, messagebox
from tkinter.ttk import Treeview, Progressbar, Scrollbar
from duplicate_finder import find_duplicates_and_similars, generate_report
from image_processing import display_image


class DuplicateFinderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Поиск дубликатов и схожих изображений")
        self.root.geometry("1000x600")

        self.main_folder = ""

        # Фрейм для таблицы с прокруткой
        table_frame = tk.Frame(root)
        table_frame.pack(fill=tk.BOTH, expand=True)

        self.tree = Treeview(
            table_frame, columns=("File", "Duplicate", "Similar"), show="headings"
        )
        self.tree.heading("File", text="Файл")
        self.tree.heading("Duplicate", text="Дубликат")
        self.tree.heading("Similar", text="Схожий")

        scrollbar_y = Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar_y.set)

        scrollbar_x = Scrollbar(
            table_frame, orient="horizontal", command=self.tree.xview
        )
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.configure(xscrollcommand=scrollbar_x.set)

        self.tree.pack(fill=tk.BOTH, expand=True)

        # Окно предпросмотра изображений
        preview_frame = tk.Frame(root)
        preview_frame.pack(pady=10, fill=tk.X)

        self.original_label = tk.Label(
            preview_frame, text="Исходное изображение", width=20
        )
        self.original_label.pack(side=tk.LEFT, padx=10)

        self.duplicate_label = tk.Label(preview_frame, text="Дубликат/Схожее", width=20)
        self.duplicate_label.pack(side=tk.RIGHT, padx=10)

        self.original_image_label = tk.Label(preview_frame)
        self.original_image_label.pack(side=tk.LEFT, padx=10)

        self.duplicate_image_label = tk.Label(preview_frame)
        self.duplicate_image_label.pack(side=tk.RIGHT, padx=10)

        open_button = tk.Button(root, text="Открыть папку", command=self.open_folder)
        open_button.pack(pady=10)

        search_button = tk.Button(
            root, text="Найти дубликаты", command=self.search_duplicates
        )
        search_button.pack(pady=10)

        self.progress = Progressbar(
            root, orient=tk.HORIZONTAL, length=400, mode="determinate"
        )
        self.progress.pack(pady=10)

        self.tree.bind("<ButtonRelease-1>", self.show_preview)

    def open_folder(self):
        self.main_folder = filedialog.askdirectory()
        if not self.main_folder:
            messagebox.showwarning("Ошибка", "Выберите папку!")

    def update_progress(self, value):
        self.progress["value"] = value
        self.root.update_idletasks()

    def search_duplicates(self):
        if not self.main_folder:
            messagebox.showwarning("Ошибка", "Выберите папку!")
            return

        duplicates, similars = find_duplicates_and_similars(
            self.main_folder, self.update_progress
        )

        self.tree.delete(
            *self.tree.get_children()
        )  # Очищаем дерево перед новым поиском
        for file, duplicate in duplicates.items():
            self.tree.insert("", "end", values=(file, duplicate, ""))

        for file1, file2 in similars.items():
            self.tree.insert("", "end", values=(file1, "", file2))

        generate_report(duplicates, similars)
        messagebox.showinfo("Результат", "Поиск завершен. Отчет сохранен.")

    def show_preview(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            values = self.tree.item(selected_item[0], "values")
            file_path = values[0]
            duplicate_path = values[1] if values[1] else values[2]

            if file_path and os.path.exists(file_path):
                display_image(file_path, self.original_image_label)

            if duplicate_path and os.path.exists(duplicate_path):
                display_image(duplicate_path, self.duplicate_image_label)
