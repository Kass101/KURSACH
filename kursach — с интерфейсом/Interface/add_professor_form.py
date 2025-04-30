import tkinter as tk
from tkinter import messagebox
import re
from Interface.db_connection import connect_to_db

def open_add_professor_form(tree, update_callback):
    _open_professor_form("Добавить преподавателя", tree, update_callback)

def open_edit_professor_form(professor_data, tree, update_callback):
    _open_professor_form("Редактировать преподавателя", tree, update_callback, professor_data)

def _open_professor_form(title, tree, update_callback, professor_data=None):
    window = tk.Toplevel()
    window.title(title)

    labels = ["ID преподавателя", "ФИО", "Телефон", "Email"]
    entries = {}

    for i, label in enumerate(labels):
        tk.Label(window, text=label).grid(row=i, column=0, padx=10, pady=5, sticky="e")
        entry = tk.Entry(window, width=50)
        entry.grid(row=i, column=1, padx=10, pady=5)
        entries[label] = entry

    if professor_data:
        entries["ID преподавателя"].insert(0, professor_data["id_professor"])
        entries["ФИО"].insert(0, professor_data["fio"])
        entries["Телефон"].insert(0, professor_data["phone_number"])
        entries["Email"].insert(0, professor_data["email"])
        entries["ID преподавателя"].config(state="disabled")  # ID нельзя менять

    def save():
        professor = {
            "id_professor": entries["ID преподавателя"].get().strip(),
            "fio": entries["ФИО"].get().strip(),
            "phone_number": entries["Телефон"].get().strip(),
            "email": entries["Email"].get().strip(),
        }

        try:
            validate_professor_fields(professor)
        except Exception as e:
            messagebox.showerror("Ошибка валидации", str(e))
            return

        conn = connect_to_db()
        if conn is None:
            messagebox.showerror("Ошибка подключения", "Нет подключения к базе данных")
            return

        try:
            with conn.cursor() as cur:
                if professor_data:
                    # UPDATE
                    cur.execute("""
                        UPDATE "Professor"
                        SET fio = %(fio)s,
                            phone_number = %(phone_number)s,
                            email = %(email)s
                        WHERE id_professor = %(id_professor)s
                    """, professor)
                else:
                    # Проверки на уникальность
                    check_if_exists(conn, 'SELECT COUNT(*) FROM "Professor" WHERE id_professor = %s', professor["id_professor"], "Такой ID уже существует")
                    check_if_exists(conn, 'SELECT COUNT(*) FROM "Professor" WHERE phone_number = %s', professor["phone_number"], "Такой телефон уже существует")
                    check_if_exists(conn, 'SELECT COUNT(*) FROM "Professor" WHERE email = %s', professor["email"], "Такой email уже существует")

                    cur.execute("""
                        INSERT INTO "Professor" 
                        (id_professor, fio, phone_number, email)
                        VALUES 
                        (%(id_professor)s, %(fio)s, %(phone_number)s, %(email)s)
                    """, professor)

            conn.commit()
            messagebox.showinfo("Успех", "Данные сохранены")
            window.destroy()
            update_callback(tree)

        except Exception as e:
            conn.rollback()
            messagebox.showerror("Ошибка БД", str(e))
        finally:
            conn.close()

    def check_if_exists(conn, query, value, message):
        with conn.cursor() as cur:
            cur.execute(query, (value,))
            if cur.fetchone()[0] > 0:
                raise ValueError(message)

    tk.Button(window, text="Сохранить", command=save).grid(row=len(labels), column=0, columnspan=2, pady=10)

def validate_professor_fields(data):
    errors = []

    required_fields = {
        "id_professor": "ID",
        "fio": "ФИО",
        "phone_number": "Телефон",
        "email": "Email"
    }

    empty_fields = [name for key, name in required_fields.items() if not data.get(key)]
    if empty_fields:
        errors.append("Заполните поле(я):")
        errors.extend([f"• {field}" for field in empty_fields])

    if not errors:
        if not re.match(r"\d{2}-\d{3}", data["id_professor"]):
            errors.append("• ID должен быть в формате хх-ххх (например, 22-061)")

        if not re.match(r"^[А-Яа-яЁё\s]+$", data["fio"]):
            errors.append("• ФИО должно содержать только русские буквы и пробелы")

        if not (data["phone_number"].isdigit() and len(data["phone_number"]) == 11):
            errors.append("• Телефон должен содержать 11 цифр")

        if not re.match(r"^[\w\.-]+@(mail\.ru|gmail\.com)$", data["email"]):
            errors.append("• Email должен быть в домене @mail.ru или @gmail.com")

        conn = connect_to_db()
        if conn is None:
            errors.append("• Не удалось подключиться к базе данных для валидации")
        else:
            try:
                with conn.cursor() as cur:
                    cur.execute('SELECT id_professor FROM "Professor" WHERE email = %s', (data["email"],))
                    row = cur.fetchone()
                    if row and row[0] != data["id_professor"]:
                        errors.append("• Такой email уже зарегистрирован у другого преподавателя")

                    cur.execute('SELECT id_professor FROM "Professor" WHERE phone_number = %s', (data["phone_number"],))
                    row = cur.fetchone()
                    if row and row[0] != data["id_professor"]:
                        errors.append("• Такой номер телефона уже зарегистрирован у другого преподавателя")
            finally:
                conn.close()

    if errors:
        raise ValueError("\n".join(errors))
