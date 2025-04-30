from Interface.db_connection import connect_to_db
import re

def validate_professor(data):
    # Проверка id_professor
    if not re.match(r"\d{2}-\d{3}", data["id_professor"]):
        raise ValueError("ID профессора должен быть в формате 'xx-xxx'")

    # Проверка ФИО
    if len(data["fio"]) > 100:
        raise ValueError("ФИО не должно превышать 100 символов")

    # Проверка номера телефона
    if not (data["phone_number"].isdigit() and len(data["phone_number"]) == 11):
        raise ValueError("Телефон должен содержать 11 цифр")

    # Проверка email
    if not re.match(r"^[\w\.-]+@(mail\.ru|gmail\.com)$", data["email"]):
        raise ValueError("Email должен быть @mail.ru или @gmail.com")

def check_professor_exists(id_professor):
    conn = connect_to_db()
    if conn is None:
        print("Не удалось подключиться к базе данных.")
        return False

    try:
        with conn.cursor() as cur:
            cur.execute("""SELECT COUNT(*) FROM "Professor" WHERE id_professor = %s""", (id_professor,))
            result = cur.fetchone()
            return result[0] > 0
    except Exception as e:
        print(f"Ошибка при проверке существования профессора: {e}")
        return False
    finally:
        conn.close()

def check_email_exists(email):
    conn = connect_to_db()
    if conn is None:
        print("Не удалось подключиться к базе данных.")
        return False

    try:
        with conn.cursor() as cur:
            cur.execute("""SELECT COUNT(*) FROM "Professor" WHERE email = %s""", (email,))
            result = cur.fetchone()
            return result[0] > 0
    except Exception as e:
        print(f"Ошибка при проверке существования email: {e}")
        return False
    finally:
        conn.close()

def check_phone_exists(phone_number):
    conn = connect_to_db()
    if conn is None:
        print("Не удалось подключиться к базе данных.")
        return False

    try:
        with conn.cursor() as cur:
            cur.execute("""SELECT COUNT(*) FROM "Professor" WHERE phone_number = %s""", (phone_number,))
            result = cur.fetchone()
            return result[0] > 0
    except Exception as e:
        print(f"Ошибка при проверке существования phone_number: {e}")
        return False
    finally:
        conn.close()

def add_professor(data):
    conn = connect_to_db()
    if conn is None:
        print("Не удалось подключиться к базе данных.")
        return

    try:
        # Валидация данных
        validate_professor(data)

        # Проверка на существование ID профессора
        if check_professor_exists(data["id_professor"]):
            print("Профессор с таким ID уже существует.")
            return

        # Проверка на уникальность email
        if check_email_exists(data["email"]):
            print("Профессор с таким email уже существует.")
            return

        # Проверка на уникальность phone_number
        if check_phone_exists(data["phone_number"]):
            print("Профессор с таким номером телефона уже существует.")
            return

        with conn.cursor() as cur:
            insert_query = """
                INSERT INTO "Professor" (id_professor, fio, phone_number, email)
                VALUES (%(id_professor)s, %(fio)s, %(phone_number)s, %(email)s)
            """
            cur.execute(insert_query, data)
            conn.commit()
            print("Профессор успешно добавлен в базу данных.")

    except ValueError as ve:
        print(f"Ошибка валидации данных: {ve}")
    except Exception as e:
        print(f"Ошибка при добавлении профессора: {e}")
        conn.rollback()
    finally:
        conn.close()
        print("Соединение с базой данных закрыто.")

