from db_connection import connect_to_db
import re
from datetime import datetime

def validate_Group(data, conn):
    """Валидация данных группы."""

    # Проверка шифра
    if not re.match(r"^[А-Я]{2}-\d{2}$", data["shifr"]):
        raise ValueError("Шифр должен быть в формате: 2 заглавные буквы, тире, 2 цифры (например, ПО-22).")

    # Проверка, что шифр уникален
    if check_if_shifr_exists(data["shifr"], conn):
        raise ValueError(f"Группа с шифром {data['shifr']} уже существует.")

    # Проверка, что id_course существует в таблице Course
    if not check_if_course_id_exists(data["id_course"], conn):
        raise ValueError(f"Курс с id {data['id_course']} не найден.")

    # Проверка дат
    try:
        begin = datetime.strptime(data["begin_date"], "%Y-%m-%d")
        end = datetime.strptime(data["end_date"], "%Y-%m-%d")
        if end <= begin:
            raise ValueError("Дата окончания должна быть позже даты начала.")
    except ValueError:
        raise ValueError("Неверный формат даты. Используйте YYYY-MM-DD.")

def check_if_shifr_exists(shifr, conn):
    """Проверка существования шифра группы."""
    try:
        with conn.cursor() as cur:
            cur.execute('SELECT COUNT(*) FROM "Group" WHERE shifr = %s', (shifr,))
            result = cur.fetchone()
            return result[0] > 0
    except Exception as e:
        print(f"Ошибка при проверке существования шифра: {e}")
        return False

def check_if_course_id_exists(id_course, conn):
    """Проверка существования курса с данным id_course."""
    try:
        with conn.cursor() as cur:
            cur.execute('SELECT COUNT(*) FROM "Course" WHERE id_course = %s', (id_course,))
            result = cur.fetchone()
            return result[0] > 0
    except Exception as e:
        print(f"Ошибка при проверке существования курса: {e}")
        return False

def add_Group(data):
    """Добавление группы в базу данных."""
    conn = connect_to_db()
    if conn is None:
        print("Не удалось подключиться к базе данных.")
        return

    try:
        validate_Group(data, conn)
    except ValueError as e:
        print(f"Ошибка валидации: {e}")
        conn.close()
        return

    try:
        with conn.cursor() as cur:
            insert_query = """
                INSERT INTO "Group" (shifr, id_course, begin_date, end_date)
                VALUES (%(shifr)s, %(id_course)s, %(begin_date)s, %(end_date)s)
            """
            cur.execute(insert_query, data)
            conn.commit()
            print("Группа успешно добавлена в базу данных.")

    except Exception as e:
        print(f"Ошибка при добавлении группы: {e}")
        conn.rollback()

    finally:
        conn.close()
        print("Соединение с базой данных закрыто.")
