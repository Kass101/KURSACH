from tkinter import ttk, messagebox
from Interface.db_connection import connect_to_db
from datetime import datetime
from Interface.add_class_form import open_add_class_form, open_edit_class_form

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

            # Получаем название курса по id_course
            cursor.execute('SELECT name FROM "Course" WHERE id_course = %s', (row[4],))
            course_name = cursor.fetchone()[0]

            tree.insert('', 'end', values=(index, formatted_date_time, row[2], course_name, row[3], *row[5:], row[0]))

        conn.close()
    else:
        print("Ошибка подключения к базе данных.")

def create_class_tab(tab_control):
    """Создает вкладку 'Занятия' с таблицей и кнопками управления."""
    class_tab = ttk.Frame(tab_control)
    tab_control.add(class_tab, text="Занятия")

    # Столбцы таблицы
    columns = ("№", "Дата и Время", "Тип", "Курс", "Группа", "ID преподавателя", "Преподаватель", "Аудитория", "ID_занятия")
    tree = ttk.Treeview(class_tab, columns=columns, show="headings", selectmode="browse")

    for col in columns[:-1]:  # последний не отображаем
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor="center")

    tree["displaycolumns"] = columns[:-1]
    tree.pack(fill="both", expand=True)

    # Обновим таблицу сразу
    update_class_table(tree)

    # Кнопки управления
    button_frame = ttk.Frame(class_tab)
    button_frame.pack(pady=10)

    ttk.Button(
        button_frame,
        text="Добавить занятие",
        command=lambda: open_add_class_form(tree, update_class_table)
    ).pack(side="left", padx=10)

    def on_edit_class():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Пожалуйста, выберите занятие для редактирования.")
            return

        item = tree.item(selected[0])["values"]
        class_data = {
            "id_class": item[8],
            "date_time": item[1],
            "type": item[2],
            "course": item[3],
            "shifr": item[4],
            "id_professor": item[5],
            "fio": item[6],
            "class_number": item[7],
        }

        open_edit_class_form(tree, update_class_table, class_data)

    ttk.Button(button_frame, text="Редактировать занятие", command=on_edit_class).pack(side="left", padx=10)

    def on_delete_class():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Пожалуйста, выберите занятие для удаления.")
            return

        item = tree.item(selected[0])["values"]
        class_id = item[8]

        confirm = messagebox.askyesno("Подтверждение удаления", "Вы уверены, что хотите удалить выбранное занятие?")
        if not confirm:
            return

        conn = connect_to_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM "Class" WHERE id_class = %s', (class_id,))
            conn.commit()
            conn.close()
            update_class_table(tree)
            messagebox.showinfo("Уведомление", "Занятие было удалено.")
        else:
            print("Ошибка подключения к базе данных.")

    ttk.Button(button_frame, text="Удалить занятие", command=on_delete_class).pack(side="left", padx=10)
