from tkinter import ttk, messagebox
from Interface.db_connection import connect_to_db

def update_student_group_table(tree):
    """Обновляет таблицу Student_Group"""
    for row in tree.get_children():
        tree.delete(row)

    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id_student, shifr FROM "Student_Group"')
        rows = cursor.fetchall()

        for index, row in enumerate(rows, 1):
            tree.insert('', 'end', values=(index, row[0], row[1]))

        conn.close()
    else:
        print("Ошибка подключения к базе данных.")

def delete_student_from_group(tree):
    """Удаляет выбранных студентов из групп"""
    selected_items = tree.selection()
    if not selected_items:
        messagebox.showwarning("Предупреждение", "Пожалуйста, выберите запись(и) для удаления.")
        return

    conn = connect_to_db()
    if not conn:
        messagebox.showerror("Ошибка", "Не удалось подключиться к базе данных.")
        return

    cursor = conn.cursor()
    deleted = []

    for item in selected_items:
        values = tree.item(item, "values")
        student_id = values[1]
        group_shifr = values[2]

        confirm = messagebox.askyesno("Подтверждение",
            f"Вы действительно хотите удалить студента с ID {student_id} из группы {group_shifr}?")
        if confirm:
            cursor.execute('DELETE FROM "Student_Group" WHERE id_student = %s AND shifr = %s', (student_id, group_shifr))
            deleted.append((student_id, group_shifr))

    conn.commit()
    conn.close()

    update_student_group_table(tree)

    if deleted:
        msg = "\n".join([f"• ID {sid} из группы {shifr}" for sid, shifr in deleted])
        messagebox.showinfo("Удалено", f"Удалены следующие записи:\n{msg}")

def create_student_group_tab(tab_control):
    """Создает вкладку 'Группы студентов' с таблицей и кнопкой удаления"""
    student_group_tab = ttk.Frame(tab_control)
    tab_control.add(student_group_tab, text="Группы студентов")

    # Таблица
    columns = ("№", "ID студента", "Шифр группы")
    tree = ttk.Treeview(student_group_tab, columns=columns, show="headings", selectmode="extended")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=150)

    tree.pack(fill="both", expand=True)

    # Кнопка удаления
    button_frame = ttk.Frame(student_group_tab)
    button_frame.pack(pady=10)

    delete_button = ttk.Button(button_frame, text="Удалить из группы", command=lambda: delete_student_from_group(tree))
    delete_button.pack()

    # Первоначальное заполнение
    update_student_group_table(tree)

    # Обновление при открытии
    student_group_tab.bind("<Visibility>", lambda e: update_student_group_table(tree))
