import tkinter as tk
from tkinter import ttk
from db_connection import connect_to_db
from datetime import datetime


def format_date(date_obj):
    """Функция для форматирования даты в формат DD-MM-YYYY"""
    if isinstance(date_obj, str):
        try:
            date_obj = datetime.strptime(date_obj, "%Y-%m-%d %H:%M:%S")  # Преобразуем строку в datetime
            return date_obj.strftime("%d-%m-%Y %H:%M")  # Форматируем в DD-MM-YYYY HH:MM
        except ValueError:
            return "Ошибка"
    elif isinstance(date_obj, datetime):
        return date_obj.strftime("%d-%m-%Y %H:%M")
    return "Ошибка"


def update_class_table(tree):
    """Обновляет таблицу занятий"""
    for row in tree.get_children():
        tree.delete(row)

    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        # Выполняем JOIN с таблицами Course и Professor для получения названия курса и ФИО преподавателя
        cursor.execute('''
            SELECT c.date_time, c.type, c.id_course, co.name, c.shifr, c.id_professor, c.class_number, p.fio
            FROM "Class" c
            JOIN "Course" co ON c.id_course = co.id_course
            JOIN "Professor" p ON c.id_professor = p.id_professor
        ''')
        rows = cursor.fetchall()

        for index, row in enumerate(rows, 1):  # Используем enumerate для добавления порядкового номера
            formatted_date_time = format_date(row[0])  # Форматируем дату и время

            # Вставляем строку с порядковым номером, названием курса и ФИО преподавателя
            tree.insert('', 'end', values=(index, formatted_date_time, row[1], row[2], row[3], row[4], row[5], row[7], row[6]))

        conn.close()
    else:
        print("Ошибка подключения к базе данных.")


def create_class_tab(tab_control):
    """Создает вкладку "Занятия" с таблицей"""
    class_tab = ttk.Frame(tab_control)
    tab_control.add(class_tab, text="Занятия")

    # Создаем таблицу
    columns = ("№", "Дата и Время занятия", "Тип", "ID курса", "Название курса", "Группа", "ID преподавателя", "ФИО преподавателя", "Аудитория")
    tree = ttk.Treeview(class_tab, columns=columns, show="headings", style="Treeview")

    # Настройка столбцов
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150, anchor="center")  # Ширина столбцов может быть увеличена по мере необходимости

    tree.pack(fill="both", expand=True)

    # Заполняем таблицу данными
    update_class_table(tree)
