import tkinter as tk
from tkinter import ttk
from db_connection import connect_to_db
import re

def update_group_table(tree):
    """Обновляет таблицу групп"""
    for row in tree.get_children():
        tree.delete(row)

    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT g.shifr, g.id_course, c.name, g.begin_date, g.end_date
            FROM "Group" g
            JOIN "Course" c ON g.id_course = c.id_course
        ''')
        rows = cursor.fetchall()

        for index, row in enumerate(rows, 1):  # Используем enumerate для добавления порядкового номера
            # Вставляем строку с порядковым номером и данными
            tree.insert('', 'end', values=(index, row[0], row[1], row[2], row[3], row[4]))

        conn.close()


def create_group_tab(tab_control):
    """Создает вкладку "Группы" с таблицей"""
    group_tab = ttk.Frame(tab_control)
    tab_control.add(group_tab, text="Группы")

    # Создаем таблицу
    columns = ("№", "Шифр", "ID курса", "Название курса", "Дата начала", "Дата окончания")
    tree = ttk.Treeview(group_tab, columns=columns, show="headings", style="Treeview")

    # Настройка столбцов
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor="center")

    tree.pack(fill="both", expand=True)

    # Заполняем таблицу данными
    update_group_table(tree)
