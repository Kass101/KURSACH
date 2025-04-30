import tkinter as tk
from tkinter import ttk
from db_connection import connect_to_db

def update_student_group_table(tree):
    """Обновляет таблицу Student_Group"""
    for row in tree.get_children():
        tree.delete(row)

    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        # Извлекаем только id_student и shifr из таблицы Student_Group
        cursor.execute('''
            SELECT id_student, shifr
            FROM "Student_Group"
        ''')
        rows = cursor.fetchall()

        for index, row in enumerate(rows, 1):  # Используем enumerate для добавления порядкового номера
            # Вставляем строку с порядковым номером, ID студента и шифром группы
            tree.insert('', 'end', values=(index, row[0], row[1]))

        conn.close()
    else:
        print("Ошибка подключения к базе данных.")

def create_student_group_tab(tab_control):
    """Создает вкладку 'Группы студентов' с таблицей"""
    student_group_tab = ttk.Frame(tab_control)
    tab_control.add(student_group_tab, text="Группы студентов")

    # Создаем таблицу
    columns = ("№", "ID студента", "Шифр группы")
    tree = ttk.Treeview(student_group_tab, columns=columns, show="headings", style="Treeview")

    # Настройка столбцов
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150, anchor="center")

    tree.pack(fill="both", expand=True)

    # Заполняем таблицу данными сразу при открытии вкладки
    update_student_group_table(tree)

    # Также добавим обновление данных при изменении вкладки
    student_group_tab.bind("<Configure>", lambda event: update_student_group_table(tree))  # обновление при изменении размера вкладки
