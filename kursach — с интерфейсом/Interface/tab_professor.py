from tkinter import ttk
from Interface.db_connection import connect_to_db
import re


def validate_phone_number(phone_number):
    """Проверка формата телефонного номера (11 цифр)"""
    return len(phone_number) == 11 and phone_number.isdigit()


def validate_email(email):
    """Проверка формата email (домен mail.ru или gmail.com)"""
    pattern = r"^[a-zA-Z0-9_.+-]+@(mail\.ru|gmail\.com)$"
    return re.match(pattern, email) is not None


def update_professor_table(tree):
    """Обновляет таблицу преподавателей"""
    for row in tree.get_children():
        tree.delete(row)

    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id_professor, fio, phone_number, email FROM "Professor"')
        rows = cursor.fetchall()

        for index, row in enumerate(rows, 1):  # Используем enumerate для добавления порядкового номера
            id_professor = row[0]
            fio = row[1]
            phone_number = row[2]
            email = row[3]

            # Проверка формата телефонного номера
            if not validate_phone_number(phone_number):
                phone_number = "Ошибка"

            # Проверка формата email
            if not validate_email(email):
                email = "Ошибка"

            # Вставляем строку с порядковым номером
            tree.insert('', 'end', values=(index, id_professor, fio, phone_number, email))

        conn.close()


def create_professor_tab(tab_control):
    """Создает вкладку "Преподаватели" с таблицей"""
    professor_tab = ttk.Frame(tab_control)
    tab_control.add(professor_tab, text="Преподаватели")

    # Создаем таблицу
    columns = ("№", "ID", "ФИО", "Номер телефона", "Электронная почта")  # Добавляем столбец для номера

    tree = ttk.Treeview(professor_tab, columns=columns, show="headings", style="Treeview")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor="center")

    tree.pack(fill="both", expand=True)

    # Заполняем таблицу данными
    update_professor_table(tree)
