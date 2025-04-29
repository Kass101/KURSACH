from db_connection import connect_to_db
import re
from datetime import datetime

def validate_Student(data):
    """Валидация данных студента."""
    if not re.match(r"\d{2}-\d{2}-\d{4}", data["id_student"]):
        raise ValueError("ID должен быть в формате хх-хх-хххх")

    try:
        datetime.strptime(data["date"], "%Y-%m-%d")
    except ValueError:
        raise ValueError("Дата должна быть в формате YYYY-MM-DD")

    try:
        datetime.strptime(data["date_of_issue"], "%Y-%m-%d")
    except ValueError:
        raise ValueError("Дата выдачи паспорта должна быть в формате YYYY-MM-DD")

    if not re.match(r"^[А-Яа-яЁё\s]+$", data["fio"]):
        raise ValueError("ФИО должно содержать только буквы")

    if not (data["series"].isdigit() and len(data["series"]) == 4):
        raise ValueError("Серия должна быть 4 цифры")

    if not (data["number"].isdigit() and len(data["number"]) == 6):
        raise ValueError("Номер должен быть 6 цифр")

    if not re.match(r"^[\w\.-]+@(mail\.ru|gmail\.com)$", data["email"]):
        raise ValueError("Email должен быть @mail.ru или @gmail.com")

    if not (data["phone_number"].isdigit() and len(data["phone_number"]) == 11):
        raise ValueError("Телефон должен содержать 11 цифр")

    if len(data["organisation"]) > 100:
        raise ValueError("Название организации слишком длинное")

    if len(data["position"]) > 50:
        raise ValueError("Название должности слишком длинное")

def check_if_student_exists(id_student, conn):
    """Проверка, существует ли студент с таким ID."""
    try:
        with conn.cursor() as cur:
            cur.execute('SELECT COUNT(*) FROM "Student" WHERE id_student = %s', (id_student,))
            result = cur.fetchone()
            return result[0] > 0
    except Exception as e:
        print(f"Ошибка при проверке существования студента: {e}")
        return False

def check_if_phone_exists(phone_number, conn):
    """Проверка, существует ли телефонный номер в базе данных."""
    try:
        with conn.cursor() as cur:
            cur.execute('SELECT COUNT(*) FROM "Student" WHERE phone_number = %s', (phone_number,))
            result = cur.fetchone()
            return result[0] > 0
    except Exception as e:
        print(f"Ошибка при проверке существования телефонного номера: {e}")
        return False

def check_if_email_exists(email, conn):
    """Проверка, существует ли email в базе данных."""
    try:
        with conn.cursor() as cur:
            cur.execute('SELECT COUNT(*) FROM "Student" WHERE email = %s', (email,))
            result = cur.fetchone()
            return result[0] > 0
    except Exception as e:
        print(f"Ошибка при проверке существования email: {e}")
        return False

def check_if_passport_exists(series, number, conn):
    """Проверка, существует ли комбинация серии и номера паспорта в базе данных."""
    try:
        with conn.cursor() as cur:
            cur.execute('SELECT COUNT(*) FROM "Student" WHERE series = %s AND number = %s', (series, number))
            result = cur.fetchone()
            return result[0] > 0
    except Exception as e:
        print(f"Ошибка при проверке существования серии и номера паспорта: {e}")
        return False

def add_Student(data):
    """Добавление студента в базу данных."""
    conn = connect_to_db()
    if conn is None:
        print("Не удалось подключиться к базе данных.")
        return

    try:
        validate_Student(data)
    except ValueError as e:
        print(f"Ошибка валидации: {e}")
        conn.close()
        return

    if check_if_student_exists(data["id_student"], conn):
        print(f"Ошибка: Студент с ID {data['id_student']} уже существует.")
        conn.close()
        return

    if check_if_phone_exists(data["phone_number"], conn):
        print(f"Ошибка: Студент с таким номером телефона {data['phone_number']} уже существует.")
        conn.close()
        return

    if check_if_email_exists(data["email"], conn):
        print(f"Ошибка: Студент с таким email {data['email']} уже существует.")
        conn.close()
        return

    if check_if_passport_exists(data["series"], data["number"], conn):
        print(f"Ошибка: Студент с таким паспортом (серия {data['series']}, номер {data['number']}) уже существует.")
        conn.close()
        return

    try:
        with conn.cursor() as cur:
            insert_query = """
                INSERT INTO "Student" 
                (id_student, date, fio, series, number, issued_by, date_of_issue, phone_number, email, organisation, position)
                VALUES 
                (%(id_student)s, %(date)s, %(fio)s, %(series)s, %(number)s, %(issued_by)s, %(date_of_issue)s, %(phone_number)s, %(email)s, %(organisation)s, %(position)s)
            """
            cur.execute(insert_query, data)
            conn.commit()
            print("Student успешно добавлен в базу данных.")

    except Exception as e:
        print(f"Ошибка при добавлении Student: {e}")
        conn.rollback()

    finally:
        conn.close()
        print("Соединение с базой данных закрыто.")
