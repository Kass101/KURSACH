import tkinter as tk
from tkinter import ttk
from Interface.db_connection import connect_to_db

def update_student_table():
    # Очищаем старые данные в таблице
    for row in tree.get_children():
        tree.delete(row)

    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        # Выбираем все данные из таблицы
        cursor.execute('SELECT id_student, date, fio, series, number, issued_by, date_of_issue, phone_number, email, organisation, position FROM "Student"')
        rows = cursor.fetchall()

        for row in rows:
            # Вставляем данные в таблицу без изменений формата дат
            tree.insert('', 'end', values=(
                row[0],  # id_student
                row[2],  # fio
                row[1],  # date (Дата рождения)
                row[3],  # series
                row[4],  # number
                row[5],  # issued_by
                row[6],  # date_of_issue (Дата выдачи)
                row[7],  # phone_number
                row[8],  # email
                row[9],  # organisation
                row[10]  # position
            ))
        conn.close()

# Создаем основное окно
root = tk.Tk()
root.title("Интерфейс приложения")

# Создаем панель вкладок
tab_control = ttk.Notebook(root)

# Создаем вкладку "Студент"
student_tab = ttk.Frame(tab_control)
tab_control.add(student_tab, text="Студент")

# Создаем стиль для таблицы (с границами)
style = ttk.Style()

# Стиль для Tableview
style.configure("Treeview",
                borderwidth=1,  # Толщина границы
                relief="solid",  # Рельеф границы
                rowheight=30,  # Высота строки
                highlightthickness=0)  # Отключаем подсветку

style.configure("Treeview.Heading",
                font=("Arial", 10, "bold"),  # Шрифт для заголовков
                anchor="center",  # Выравнивание заголовков по центру
                relief="solid",  # Добавляем границу для заголовков
                borderwidth=1)  # Устанавливаем толщину границы для заголовков

# Создаем таблицу для отображения данных студентов
tree = ttk.Treeview(student_tab, columns=("ID", "FIO", "Birth Date", "Series", "Number", "Issued by", "Issue Date", "Phone", "Email", "Organisation", "Position"), show="headings", style="Treeview")

tree.heading("#1", text="Шифр студента")
tree.heading("#2", text="ФИО студента")
tree.heading("#3", text="Дата рождения")
tree.heading("#4", text="Серия паспорта")
tree.heading("#5", text="Номер паспорта")
tree.heading("#6", text="Кем выдан")
tree.heading("#7", text="Дата выдачи")
tree.heading("#8", text="Номер телефона")
tree.heading("#9", text="Почта")
tree.heading("#10", text="Место работы")
tree.heading("#11", text="Должность")

# Устанавливаем одинаковую ширину для всех столбцов
column_width = 120
for col in tree["columns"]:
    tree.column(col, width=column_width, anchor="center")

tree.pack(fill="both", expand=True)

# Заполняем таблицу данными из базы данных
update_student_table()

# Отображаем вкладки
tab_control.pack(expand=1, fill="both")

# Запуск приложения
root.mainloop()
