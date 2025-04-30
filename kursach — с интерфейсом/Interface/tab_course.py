from tkinter import ttk
from Interface.db_connection import connect_to_db


def update_course_table(tree):
    """Обновляет таблицу курсов"""
    for row in tree.get_children():
        tree.delete(row)

    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id_course, name, hours FROM "Course"')
        rows = cursor.fetchall()

        for index, row in enumerate(rows, 1):  # Используем enumerate для добавления порядкового номера
            # Вставляем данные с порядковым номером в первый столбец
            tree.insert('', 'end', values=(index, row[0], row[1], row[2]))

        conn.close()


def create_course_tab(tab_control):
    """Создает вкладку "Курсы" с таблицей"""
    course_tab = ttk.Frame(tab_control)
    tab_control.add(course_tab, text="Курсы")

    # Создаем таблицу
    columns = ("№", "ID", "Назавание курса", "Кол-во часов")
    tree = ttk.Treeview(course_tab, columns=columns, show="headings", style="Treeview")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor="center")

    tree.pack(fill="both", expand=True)

    # Заполняем таблицу данными
    update_course_table(tree)
