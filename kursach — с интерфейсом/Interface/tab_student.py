import tkinter as tk
from tkinter import ttk, messagebox
from db_connection import connect_to_db
from Interface.add_student_form import open_add_student_form, open_edit_student_form

def update_student_table(tree):
    # Обновление таблицы студентов
    for row in tree.get_children():
        tree.delete(row)

    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute(
            'SELECT id_student, date, fio, series, number, issued_by, date_of_issue, phone_number, email, organisation, position FROM "Student"'
        )
        rows = cursor.fetchall()

        for index, row in enumerate(rows, 1):
            tree.insert('', 'end', values=(
                index, row[0], row[2], row[1], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10]
            ))

        conn.close()

def create_student_tab(tab_control):
    student_tab = ttk.Frame(tab_control)
    tab_control.add(student_tab, text="Студенты")

    table_frame = ttk.Frame(student_tab)
    table_frame.pack(fill="both", expand=True)

    columns = (
        "№", "ID", "ФИО", "Дата рождения", "Серия", "Номер", "Кем выдан", "Дата выдачи", "Телефон", "Электронная почта",
        "Организация", "Должность"
    )

    tree = ttk.Treeview(table_frame, columns=columns, show="headings", style="Treeview")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor="center")

    update_student_table(tree)
    tree.pack(fill="both", expand=True)

    # Кнопки управления
    button_frame = ttk.Frame(student_tab)
    button_frame.pack(fill="x", padx=10, pady=10)

    center_frame = ttk.Frame(button_frame)
    center_frame.pack(anchor="center")

    def on_add():
        open_add_student_form(tree, update_student_table)

    def on_edit():
        selected_item = tree.focus()
        if not selected_item:
            messagebox.showwarning("Выбор записи", "Пожалуйста, выберите студента для редактирования.")
            return

        values = tree.item(selected_item, "values")
        student_data = {
            "id_student": values[1],
            "fio": values[2],
            "date": values[3],
            "series": values[4],
            "number": values[5],
            "issued_by": values[6],
            "date_of_issue": values[7],
            "phone_number": values[8],
            "email": values[9],
            "organisation": values[10],
            "position": values[11],
        }
        open_edit_student_form(student_data, tree, update_student_table)

    add_button = tk.Button(center_frame, text="Добавить", command=on_add)
    add_button.pack(side="left", padx=10)

    edit_button = tk.Button(center_frame, text="Редактировать", command=on_edit)
    edit_button.pack(side="left", padx=10)