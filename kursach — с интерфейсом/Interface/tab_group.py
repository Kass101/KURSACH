from tkinter import ttk, Button, messagebox
from Interface.db_connection import connect_to_db
from Interface.add_group_form import open_group_form


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

        for index, row in enumerate(rows, 1):
            tree.insert('', 'end', values=(index, row[0], row[1], row[2], row[3], row[4]))

        conn.close()


def create_group_tab(tab_control):
    """Создает вкладку "Группы" с таблицей"""
    group_tab = ttk.Frame(tab_control)
    tab_control.add(group_tab, text="Группы")

    columns = ("№", "Шифр", "ID курса", "Название курса", "Дата начала", "Дата окончания")
    tree = ttk.Treeview(group_tab, columns=columns, show="headings", style="Treeview")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor="center")

    tree.pack(fill="both", expand=True)

    # Кнопки управления
    button_frame = ttk.Frame(group_tab)
    button_frame.pack(pady=10)

    add_button = Button(button_frame, text="Добавить группу",
                        command=lambda: open_group_form(lambda: update_group_table(tree)))
    add_button.pack(side="left", padx=5)

    def edit_selected_group():
        selected_item = tree.selection()
        if selected_item:
            values = tree.item(selected_item)["values"]
            open_group_form(lambda: update_group_table(tree), values)
        else:
            messagebox.showwarning("Внимание", "Выберите группу для редактирования")

    edit_button = Button(button_frame, text="Редактировать группу", command=edit_selected_group)
    edit_button.pack(side="left", padx=5)

    update_group_table(tree)
