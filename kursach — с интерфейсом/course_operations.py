from db_connection import connect_to_db
import re

def validate_Course(data, conn):
    """Валидация данных курса."""
    # Проверка id_course
    if not re.fullmatch(r"\d{12}", data["id_course"]):
        raise ValueError("id_course должен состоять ровно из 12 цифр.")

    if check_if_id_course_exists(data["id_course"], conn):
        raise ValueError(f"Курс с id_course '{data['id_course']}' уже существует.")

    # Проверка длины названия курса
    if len(data["name"]) > 50:
        raise ValueError("Название курса не может быть длиннее 50 символов.")

    # Проверка количества часов
    if not isinstance(data["hours"], int) or data["hours"] <= 0:
        raise ValueError("Количество часов должно быть положительным числом.")

def check_if_id_course_exists(id_course, conn):
    """Проверка, существует ли курс с таким id_course."""
    try:
        with conn.cursor() as cur:
            cur.execute('SELECT COUNT(*) FROM "Course" WHERE id_course = %s', (id_course,))
            result = cur.fetchone()
            return result[0] > 0
    except Exception as e:
        print(f"Ошибка при проверке существования id_course: {e}")
        return False

def check_if_course_exists(name, hours, conn):
    """Проверка, существует ли курс с таким названием и количеством часов."""
    try:
        with conn.cursor() as cur:
            cur.execute('SELECT COUNT(*) FROM "Course" WHERE name = %s AND hours = %s', (name, hours))
            result = cur.fetchone()
            return result[0] > 0
    except Exception as e:
        print(f"Ошибка при проверке существования курса: {e}")
        return False

def add_Course(data):
    """Добавление курса в базу данных."""
    conn = connect_to_db()
    if conn is None:
        print("Не удалось подключиться к базе данных.")
        return

    try:
        validate_Course(data, conn)
    except ValueError as e:
        print(f"Ошибка валидации: {e}")
        conn.close()
        return

    # Проверяем существование курса с таким названием и количеством часов
    if check_if_course_exists(data["name"], data["hours"], conn):
        print(f"Ошибка: Курс с названием '{data['name']}' и количеством часов {data['hours']} уже существует.")
        conn.close()
        return

    try:
        with conn.cursor() as cur:
            insert_query = """
                INSERT INTO "Course" (id_course, name, hours)
                VALUES (%(id_course)s, %(name)s, %(hours)s)
            """
            cur.execute(insert_query, data)
            conn.commit()
            print("Курс успешно добавлен в базу данных.")

    except Exception as e:
        print(f"Ошибка при добавлении курса: {e}")
        conn.rollback()

    finally:
        conn.close()
        print("Соединение с базой данных закрыто.")
