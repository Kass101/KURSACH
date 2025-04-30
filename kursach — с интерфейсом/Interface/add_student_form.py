import tkinter as tk
from tkinter import messagebox
import re
from datetime import datetime
from db_connection import connect_to_db

def open_add_student_form(tree, update_callback):
    _open_student_form("Добавить студента", tree, update_callback)

def open_edit_student_form(student_data, tree, update_callback):
    _open_student_form("Редактировать студента", tree, update_callback, student_data)

def _open_student_form(title, tree, update_callback, student_data=None):
    window = tk.Toplevel()
    window.title(title)

    labels = [
        "ID студента", "ФИО", "Дата рождения (YYYY-MM-DD)", "Серия паспорта", "Номер паспорта",
        "Кем выдан", "Дата выдачи паспорта (YYYY-MM-DD)", "Телефон", "Email", "Организация", "Должность"
    ]
    entries = {}

    for i, label in enumerate(labels):
        tk.Label(window, text=label).grid(row=i, column=0, padx=10, pady=5, sticky="e")
        entry = tk.Entry(window, width=50)
        entry.grid(row=i, column=1, padx=10, pady=5)
        entries[label] = entry

    if student_data:
        entries["ID студента"].insert(0, student_data["id_student"])
        entries["ФИО"].insert(0, student_data["fio"])
        entries["Дата рождения (YYYY-MM-DD)"].insert(0, student_data["date"])
        entries["Серия паспорта"].insert(0, student_data["series"])
        entries["Номер паспорта"].insert(0, student_data["number"])
        entries["Кем выдан"].insert(0, student_data["issued_by"])
        entries["Дата выдачи паспорта (YYYY-MM-DD)"].insert(0, student_data["date_of_issue"])
        entries["Телефон"].insert(0, student_data["phone_number"])
        entries["Email"].insert(0, student_data["email"])
        entries["Организация"].insert(0, student_data["organisation"])
        entries["Должность"].insert(0, student_data["position"])
        entries["ID студента"].config(state="disabled")  # ID нельзя менять

    def save():
        student = {
            "id_student": entries["ID студента"].get().strip(),
            "fio": entries["ФИО"].get().strip(),
            "date": entries["Дата рождения (YYYY-MM-DD)"].get().strip(),
            "series": entries["Серия паспорта"].get().strip(),
            "number": entries["Номер паспорта"].get().strip(),
            "issued_by": entries["Кем выдан"].get().strip(),
            "date_of_issue": entries["Дата выдачи паспорта (YYYY-MM-DD)"].get().strip(),
            "phone_number": entries["Телефон"].get().strip(),
            "email": entries["Email"].get().strip(),
            "organisation": entries["Организация"].get().strip(),
            "position": entries["Должность"].get().strip(),
        }

        try:
            validate_student_fields(student)
        except Exception as e:
            messagebox.showerror("Ошибка валидации", str(e))
            return

        conn = connect_to_db()
        if conn is None:
            messagebox.showerror("Ошибка подключения", "Нет подключения к базе данных")
            return

        try:
            with conn.cursor() as cur:
                if student_data:
                    # UPDATE
                    cur.execute(""" 
                        UPDATE "Student"
                        SET fio = %(fio)s,
                            date = %(date)s,
                            series = %(series)s,
                            number = %(number)s,
                            issued_by = %(issued_by)s,
                            date_of_issue = %(date_of_issue)s,
                            phone_number = %(phone_number)s,
                            email = %(email)s,
                            organisation = %(organisation)s,
                            position = %(position)s
                        WHERE id_student = %(id_student)s
                    """, student)
                else:
                    # Проверки на уникальность
                    check_if_exists(conn, 'SELECT COUNT(*) FROM "Student" WHERE id_student = %s', student["id_student"], "Такой ID уже существует")
                    check_if_exists(conn, 'SELECT COUNT(*) FROM "Student" WHERE phone_number = %s', student["phone_number"], "Такой телефон уже существует")
                    check_if_exists(conn, 'SELECT COUNT(*) FROM "Student" WHERE email = %s', student["email"], "Такой email уже существует")
                    check_passport_exists(conn, student["series"], student["number"])

                    cur.execute("""
                        INSERT INTO "Student" 
                        (id_student, date, fio, series, number, issued_by, date_of_issue, phone_number, email, organisation, position)
                        VALUES 
                        (%(id_student)s, %(date)s, %(fio)s, %(series)s, %(number)s, %(issued_by)s, %(date_of_issue)s, %(phone_number)s, %(email)s, %(organisation)s, %(position)s)
                    """, student)

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

    def check_passport_exists(conn, series, number):
        with conn.cursor() as cur:
            cur.execute('SELECT COUNT(*) FROM "Student" WHERE series = %s AND number = %s', (series, number))
            if cur.fetchone()[0] > 0:
                raise ValueError("Паспорт уже зарегистрирован")

    tk.Button(window, text="Сохранить", command=save).grid(row=len(labels), column=0, columnspan=2, pady=10)

def validate_student_fields(data):
    errors = []

    required_fields = {
        "id_student": "ID",
        "fio": "ФИО",
        "date": "Дата рождения",
        "series": "Серия паспорта",
        "number": "Номер паспорта",
        "issued_by": "Кем выдан паспорт",
        "date_of_issue": "Дата выдачи паспорта",
        "phone_number": "Телефон",
        "email": "Email",
        "organisation": "Организация",
        "position": "Должность"
    }

    empty_fields = [name for key, name in required_fields.items() if not data.get(key)]
    if empty_fields:
        errors.append("Заполните поле(я):")
        errors.extend([f"• {field}" for field in empty_fields])

    if not errors:
        if not re.match(r"\d{2}-\d{2}-\d{4}", data["id_student"]):
            errors.append("• ID должен быть в формате хх-хх-хххх (например, 22-06-0001)")

        try:
            datetime.strptime(data["date"], "%Y-%m-%d")
        except ValueError:
            errors.append("• Неверный формат даты рождения. Используйте YYYY-MM-DD")

        try:
            datetime.strptime(data["date_of_issue"], "%Y-%m-%d")
        except ValueError:
            errors.append("• Неверный формат даты выдачи паспорта. Используйте YYYY-MM-DD")

        if not re.match(r"^[А-Яа-яЁё\s]+$", data["fio"]):
            errors.append("• ФИО должно содержать только русские буквы и пробелы")

        if not (data["series"].isdigit() and len(data["series"]) == 4):
            errors.append("• Серия паспорта должна состоять из 4 цифр")

        if not (data["number"].isdigit() and len(data["number"]) == 6):
            errors.append("• Номер паспорта должен состоять из 6 цифр")

        if len(data["issued_by"]) > 50:
            errors.append("• Поле 'Кем выдан' не должно превышать 50 символов")

        if not (data["phone_number"].isdigit() and len(data["phone_number"]) == 11):
            errors.append("• Телефон должен содержать 11 цифр")

        if not re.match(r"^[\w\.-]+@(mail\.ru|gmail\.com)$", data["email"]):
            errors.append("• Email должен быть в домене @mail.ru или @gmail.com")

        if len(data["organisation"]) > 100:
            errors.append("• Слишком длинное название организации (до 100 символов)")

        if len(data["position"]) > 50:
            errors.append("• Слишком длинное название должности (до 50 символов)")

        conn = connect_to_db()
        if conn is None:
            errors.append("• Не удалось подключиться к базе данных для валидации")
        else:
            try:
                with conn.cursor() as cur:
                    cur.execute('SELECT id_student FROM "Student" WHERE email = %s', (data["email"],))
                    row = cur.fetchone()
                    if row and row[0] != data["id_student"]:
                        errors.append("• Такой email уже зарегистрирован у другого студента")

                    cur.execute('SELECT id_student FROM "Student" WHERE phone_number = %s', (data["phone_number"],))
                    row = cur.fetchone()
                    if row and row[0] != data["id_student"]:
                        errors.append("• Такой номер телефона уже зарегистрирован у другого студента")

                    cur.execute('SELECT id_student FROM "Student" WHERE series = %s AND number = %s',
                                (data["series"], data["number"]))
                    row = cur.fetchone()
                    if row and row[0] != data["id_student"]:
                        errors.append("• Такой паспорт уже зарегистрирован у другого студента")
            finally:
                conn.close()

    if errors:
        raise ValueError("\n".join(errors))
