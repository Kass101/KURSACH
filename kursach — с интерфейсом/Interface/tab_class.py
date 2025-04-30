from tkinter import ttk, messagebox
from Interface.db_connection import connect_to_db
from datetime import datetime
from Interface.add_class_form import open_add_class_form

def format_date(date_obj):
    if isinstance(date_obj, str):
        try:
            date_obj = datetime.strptime(date_obj, "%Y-%m-%d %H:%M:%S")
            return date_obj.strftime("%d-%m-%Y %H:%M")
        except ValueError:
            return "Ошибка"
    elif isinstance(date_obj, datetime):
        return date_obj.strftime("%d-%m-%Y %H:%M")
    return "Ошибка"

def update_class_table(tree):
    """Обновляет данные в таблице занятий."""
    for row in tree.get_children():
        tree.delete(row)

    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute(''' 
            SELECT c.id_class, c.date_time, c.type, g.shifr, g.id_course, p.id_professor, p.fio, c.class_number
            FROM "Class" c
            JOIN "Group" g ON c.shifr = g.shifr
            JOIN "Professor" p ON c.id_professor = p.id_professor
        ''')
        rows = cursor.fetchall()

        for index, row in enumerate(rows, 1):
            formatted_date_time = format_date(row[1])

            # Подгружаем название курса из таблицы Course, используя id_course из таблицы Group
            cursor.execute('SELECT name FROM "Course" WHERE id_course = %s', (row[4],))
            course_name = cursor.fetchone()[0]

            # Вставляем строку в таблицу
            tree.insert('', 'end', values=(index, formatted_date_time, row[2], course_name, row[3], *row[5:]))

        conn.close()
    else:
        print("Ошибка подключения к базе данных.")

def create_class_tab(tab_control):
    """Создает вкладку 'Занятия' с таблицей и автоматическим обновлением данных."""
    class_tab = ttk.Frame(tab_control)
    tab_control.add(class_tab, text="Занятия")

    # Определяем столбцы для таблицы
    columns = ("№", "Дата и Время", "Тип", "Курс", "Группа", "ID преподавателя", "Преподаватель", "Аудитория")
    tree = ttk.Treeview(class_tab, columns=columns, show="headings")

    # Настроим заголовки и ширину столбцов
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor="center")

    # Добавляем таблицу на экран
    tree.pack(fill="both", expand=True)

    # Автоматическое обновление таблицы через 1 секунду (1000 миллисекунд)
    def auto_update():
        update_class_table(tree)
        # Регистрируем повторное обновление через 1 секунду
        class_tab.after(1000, auto_update)

    # Инициализируем автоматическое обновление при открытии вкладки
    auto_update()

    # Панель кнопок
    button_frame = ttk.Frame(class_tab)
    button_frame.pack(pady=10)

    # Кнопка для добавления нового занятия
    ttk.Button(button_frame, text="Добавить занятие", command=lambda: open_add_class_form(tree, update_class_table)).pack()
