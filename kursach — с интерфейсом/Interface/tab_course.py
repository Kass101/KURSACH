from tkinter import ttk, messagebox
from Interface.db_connection import connect_to_db
from Interface.add_course_form import open_add_course_form, open_edit_course_form


def update_course_table(tree):
    """Обновляет таблицу курсов"""
    for row in tree.get_children():
        tree.delete(row)

    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id_course, name, hours FROM "Course"')
        rows = cursor.fetchall()

        for index, row in enumerate(rows, 1):
            tree.insert('', 'end', values=(index, row[0], row[1], row[2]))

        conn.close()


def create_course_tab(tab_control):
    """Создает вкладку "Курсы" с таблицей"""
    course_tab = ttk.Frame(tab_control)
    tab_control.add(course_tab, text="Курсы")

    columns = ("№", "ID", "Название курса", "Кол-во часов")
    tree = ttk.Treeview(course_tab, columns=columns, show="headings", style="Treeview")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor="center")

    tree.pack(fill="both", expand=True)

    button_frame = ttk.Frame(course_tab)
    button_frame.pack(pady=5)

    ttk.Button(
        button_frame,
        text="Добавить курс",
        command=lambda: open_add_course_form(tree, update_course_table)
    ).pack(side="left", padx=5)

    ttk.Button(
        button_frame,
        text="Редактировать курс",
        command=lambda: edit_selected_course(tree)
    ).pack(side="left", padx=5)

    update_course_table(tree)


def edit_selected_course(tree):
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Внимание", "Выберите курс для редактирования")
        return

    values = tree.item(selected[0])["values"]
    course_data = {
        "id_course": values[1],
        "name": values[2],
        "hours": str(values[3])
    }
    open_edit_course_form(course_data, tree, update_course_table)
