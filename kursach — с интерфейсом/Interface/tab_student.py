import tkinter as tk
from tkinter import ttk, messagebox
from db_connection import connect_to_db
from Interface.add_student_form import open_add_student_form, open_edit_student_form

def update_student_table(tree):
    for row in tree.get_children():
        tree.delete(row)

    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute(
            'SELECT id_student, date, fio, series, number, issued_by, date_of_issue, phone_number, email, organisation, position FROM "Student"'
        )
        rows = cursor.fetchall()

        for index, row in enumerate(rows, 1):
            tree.insert('', 'end', values=(index, row[0], row[2], row[1], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10]))

        conn.close()

def open_group_selection_window(tree, selected_items):
    def confirm():
        selected_group = group_combobox.get()
        if not selected_group:
            messagebox.showwarning("Предупреждение", "Пожалуйста, выберите группу.")
            return

        conn = connect_to_db()
        cur = conn.cursor()

        added = []
        already_in_group = []

        for item in selected_items:
            student_id = tree.item(item, "values")[1]

            cur.execute('SELECT 1 FROM "Student_Group" WHERE id_student = %s AND shifr = %s', (student_id, selected_group))
            exists = cur.fetchone()

            if exists:
                already_in_group.append(student_id)
            else:
                cur.execute('INSERT INTO "Student_Group" (id_student, shifr) VALUES (%s, %s)', (student_id, selected_group))
                added.append(student_id)

        conn.commit()
        cur.close()
        conn.close()

        message = ""
        if added:
            message += "Студенты добавленные в группу:\n" + "\n".join(f"• ID {sid}" for sid in added) + "\n\n"
        if already_in_group:
            message += "Студенты, которые уже были в группе:\n" + "\n".join(f"• ID {sid}" for sid in already_in_group)

        messagebox.showinfo("Результат", message)
        window.destroy()

    window = tk.Toplevel()
    window.title("Выбор группы")
    window.geometry("300x120")
    window.resizable(False, False)

    label = ttk.Label(window, text="Выберите группу:")
    label.pack(pady=(15, 5))

    group_combobox = ttk.Combobox(window, state="readonly")
    group_combobox.pack(pady=5)

    # Загрузка групп из базы данных
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute('SELECT shifr FROM "Group"')
    groups = [row[0] for row in cur.fetchall()]
    conn.close()

    group_combobox['values'] = groups

    confirm_button = ttk.Button(window, text="ОК", command=confirm)
    confirm_button.pack(pady=10)

def create_student_tab(tab_control):
    student_tab = ttk.Frame(tab_control)
    tab_control.add(student_tab, text="Студенты")

    table_frame = ttk.Frame(student_tab)
    table_frame.pack(fill="both", expand=True)

    columns = (
        "№", "ID", "ФИО", "Дата рождения", "Серия", "Номер", "Кем выдан", "Дата выдачи", "Телефон", "Электронная почта",
        "Организация", "Должность"
    )

    tree = ttk.Treeview(table_frame, columns=columns, show="headings", style="Treeview")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor="center")

    update_student_table(tree)
    tree.pack(fill="both", expand=True)

    # Кнопки
    button_frame = ttk.Frame(student_tab)
    button_frame.pack(fill="x", padx=10, pady=10)

    def on_add():
        open_add_student_form(tree, update_student_table)

    def on_edit():
        selected_item = tree.focus()
        if not selected_item:
            messagebox.showwarning("Выбор записи", "Пожалуйста, выберите студента для редактирования.")
            return
        values = tree.item(selected_item, "values")
        student_data = {
            "id_student": values[1],
            "fio": values[2],
            "date": values[3],
            "series": values[4],
            "number": values[5],
            "issued_by": values[6],
            "date_of_issue": values[7],
            "phone_number": values[8],
            "email": values[9],
            "organisation": values[10],
            "position": values[11]
        }
        open_edit_student_form(student_data, tree, update_student_table)

    def on_add_to_group():
        selected_items = tree.selection()
        if not selected_items:
            messagebox.showwarning("Предупреждение", "Сначала выберите студентов.")
            return
        open_group_selection_window(tree, selected_items)

    ttk.Button(button_frame, text="Добавить студента", command=on_add).pack(side="left", padx=5)
    ttk.Button(button_frame, text="Редактировать студента", command=on_edit).pack(side="left", padx=5)
    ttk.Button(button_frame, text="Добавить в группу", command=on_add_to_group).pack(side="left", padx=5)
