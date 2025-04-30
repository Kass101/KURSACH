import tkinter as tk
from tkinter import ttk, messagebox
from Interface.db_connection import connect_to_db
from Interface.add_professor_form import open_add_professor_form, open_edit_professor_form

def create_professor_tab(notebook):
    professor_tab = ttk.Frame(notebook)
    notebook.add(professor_tab, text="Преподаватели")

    tree = ttk.Treeview(professor_tab, columns=("No", "ID", "ФИО", "Телефон", "Email"), show="headings")
    tree.heading("No", text="№")
    tree.heading("ID", text="ID преподавателя")
    tree.heading("ФИО", text="ФИО")
    tree.heading("Телефон", text="Телефон")
    tree.heading("Email", text="Email")
    tree.column("No", width=50)
    tree.column("ID", width=120)
    tree.column("ФИО", width=200)
    tree.column("Телефон", width=120)
    tree.column("Email", width=200)
    tree.pack(fill="both", expand=True, padx=0, pady=0)

    def update_professor_table(tree_widget):
        conn = connect_to_db()
        if conn is None:
            messagebox.showerror("Ошибка", "Не удалось подключиться к базе данных")
            return
        try:
            with conn.cursor() as cur:
                cur.execute('SELECT id_professor, fio, phone_number, email FROM "Professor" ORDER BY fio')
                rows = cur.fetchall()
                tree_widget.delete(*tree_widget.get_children())
                for i, row in enumerate(rows, 1):
                    tree_widget.insert("", "end", values=(i, *row))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {e}")
        finally:
            conn.close()

    # Кнопки
    button_frame = ttk.Frame(professor_tab)
    button_frame.pack(anchor="center", pady=10)

    def on_add():
        open_add_professor_form(tree, update_professor_table)

    def on_edit():
        selected_item = tree.focus()
        if not selected_item:
            messagebox.showwarning("Выбор записи", "Пожалуйста, выберите преподавателя для редактирования.")
            return
        values = tree.item(selected_item, "values")
        professor_data = {
            "id_professor": values[1],
            "fio": values[2],
            "phone_number": values[3],
            "email": values[4]
        }
        open_edit_professor_form(professor_data, tree, update_professor_table)

    add_button = ttk.Button(button_frame, text="Добавить преподавателя", command=on_add)
    edit_button = ttk.Button(button_frame, text="Редактировать преподавателя", command=on_edit)

    add_button.grid(row=0, column=0, padx=10)
    edit_button.grid(row=0, column=1, padx=10)

    update_professor_table(tree)
