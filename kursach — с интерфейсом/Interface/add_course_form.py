import tkinter as tk
from tkinter import messagebox
import re
from Interface.db_connection import connect_to_db


def open_add_course_form(tree, update_callback):
    _open_course_form("Добавить курс", tree, update_callback)


def open_edit_course_form(course_data, tree, update_callback):
    _open_course_form("Редактировать курс", tree, update_callback, course_data)


def _open_course_form(title, tree, update_callback, course_data=None):
    window = tk.Toplevel()
    window.title(title)

    labels = ["ID курса", "Название курса", "Кол-во часов"]
    entries = {}

    for i, label in enumerate(labels):
        tk.Label(window, text=label).grid(row=i, column=0, sticky="e", padx=10, pady=5)
        entry = tk.Entry(window, width=50)
        entry.grid(row=i, column=1, padx=10, pady=5)
        entries[label] = entry

    if course_data:
        entries["ID курса"].insert(0, course_data["id_course"])
        entries["Название курса"].insert(0, course_data["name"])
        entries["Кол-во часов"].insert(0, course_data["hours"])
        entries["ID курса"].config(state="disabled")  # ID нельзя менять

    def save():
        course = {
            "id_course": entries["ID курса"].get().strip(),
            "name": entries["Название курса"].get().strip(),
            "hours": entries["Кол-во часов"].get().strip()
        }

        try:
            validate_course_fields(course)
        except Exception as e:
            messagebox.showerror("Ошибка валидации", str(e))
            return

        conn = connect_to_db()
        if conn is None:
            messagebox.showerror("Ошибка подключения", "Нет подключения к базе данных")
            return

        try:
            with conn.cursor() as cur:
                if course_data:
                    cur.execute("""
                        UPDATE "Course"
                        SET name = %(name)s,
                            hours = %(hours)s
                        WHERE id_course = %(id_course)s
                    """, course)
                else:
                    cur.execute('SELECT COUNT(*) FROM "Course" WHERE id_course = %s', (course["id_course"],))
                    if cur.fetchone()[0] > 0:
                        raise ValueError("Такой ID курса уже существует")

                    cur.execute("""
                        INSERT INTO "Course" (id_course, name, hours)
                        VALUES (%(id_course)s, %(name)s, %(hours)s)
                    """, course)

            conn.commit()
            messagebox.showinfo("Успех", "Курс успешно сохранен")
            window.destroy()
            update_callback(tree)

        except Exception as e:
            conn.rollback()
            messagebox.showerror("Ошибка БД", str(e))
        finally:
            conn.close()

    tk.Button(window, text="Сохранить", command=save).grid(row=len(labels), column=0, columnspan=2, pady=10)


def validate_course_fields(course):
    errors = []

    if not course["id_course"] or not course["name"] or not course["hours"]:
        errors.append("• Все поля должны быть заполнены")

    if not re.fullmatch(r"\d{12}", course["id_course"]):
        errors.append("• ID курса должен содержать ровно 12 цифр")

    if len(course["name"]) > 50:
        errors.append("• Название курса не должно превышать 50 символов")

    if not course["hours"].isdigit():
        errors.append("• Кол-во часов должно быть числом")

    if errors:
        raise ValueError("\n".join(errors))
