from db_connection import connect_to_db


def validate_Class(data, conn):
    """Валидация данных занятия."""

    # Проверка типа занятия
    if data["type"] not in ("лекция", "практика"):
        raise ValueError("Тип занятия должен быть либо 'лекция', либо 'практика'.")

    # Проверка длины class_number
    if len(data["class_number"]) > 10:
        raise ValueError("Номер кабинета (class_number) не может быть длиннее 10 символов.")

    # Проверка id_professor (строка ≤ 10 символов)
    if not isinstance(data["id_professor"], str) or len(data["id_professor"]) > 10:
        raise ValueError("id_professor должен быть строкой длиной не более 10 символов.")

    # Проверка существования курса
    if not check_if_group_exists(data["shifr"], conn):
        raise ValueError(f"Группа с шифром {data['shifr']} не найдена.")

    # Проверка существования профессора
    if not check_if_professor_exists(data["id_professor"], conn):
        raise ValueError(f"Профессор с id {data['id_professor']} не найден.")

    # Проверка занятости группы в это время
    if is_group_busy(data["shifr"], data["date_time"], conn):
        raise ValueError(f"У группы {data['shifr']} уже есть занятие в это время.")

    # Проверка занятости профессора в это время
    if is_professor_busy(data["id_professor"], data["date_time"], conn):
        raise ValueError(f"Профессор с id {data['id_professor']} уже занят в это время.")

    # Проверка занятости кабинета
    if is_class_number_busy(data["class_number"], data["date_time"], conn):
        raise ValueError(f"Кабинет {data['class_number']} уже занят в это время.")


def get_course_id_for_group(shifr, conn):
    """Получение id_course для группы из таблицы Group."""
    try:
        with conn.cursor() as cur:
            cur.execute('SELECT id_course FROM "Group" WHERE shifr = %s', (shifr,))
            result = cur.fetchone()
            if result:
                return result[0]  # Возвращаем id_course
            else:
                return None  # Группа не найдена
    except Exception as e:
        print(f"Ошибка при получении id_course для группы: {e}")
        return None


def check_if_group_exists(shifr, conn):
    try:
        with conn.cursor() as cur:
            cur.execute('SELECT COUNT(*) FROM "Group" WHERE shifr = %s', (shifr,))
            result = cur.fetchone()
            return result[0] > 0
    except Exception as e:
        print(f"Ошибка при проверке группы: {e}")
        return False


def check_if_professor_exists(id_professor, conn):
    try:
        with conn.cursor() as cur:
            cur.execute('SELECT COUNT(*) FROM "Professor" WHERE id_professor = %s', (id_professor,))
            result = cur.fetchone()
            return result[0] > 0
    except Exception as e:
        print(f"Ошибка при проверке профессора: {e}")
        return False


def is_group_busy(shifr, date_time, conn):
    try:
        with conn.cursor() as cur:
            cur.execute('SELECT COUNT(*) FROM "Class" WHERE shifr = %s AND date_time = %s', (shifr, date_time))
            result = cur.fetchone()
            return result[0] > 0
    except Exception as e:
        print(f"Ошибка при проверке занятости группы: {e}")
        return False


def is_professor_busy(id_professor, date_time, conn):
    try:
        with conn.cursor() as cur:
            cur.execute('SELECT COUNT(*) FROM "Class" WHERE id_professor = %s AND date_time = %s',
                        (id_professor, date_time))
            result = cur.fetchone()
            return result[0] > 0
    except Exception as e:
        print(f"Ошибка при проверке занятости профессора: {e}")
        return False


def is_class_number_busy(class_number, date_time, conn):
    try:
        with conn.cursor() as cur:
            cur.execute('SELECT COUNT(*) FROM "Class" WHERE class_number = %s AND date_time = %s',
                        (class_number, date_time))
            result = cur.fetchone()
            return result[0] > 0
    except Exception as e:
        print(f"Ошибка при проверке занятости кабинета: {e}")
        return False


def add_Class(data):
    """Добавление занятия в базу данных."""
    conn = connect_to_db()
    if conn is None:
        print("Не удалось подключиться к базе данных.")
        return

    try:
        # Получаем id_course для группы
        id_course = get_course_id_for_group(data["shifr"], conn)
        if id_course is None:
            print(f"Ошибка: Группа с шифром {data['shifr']} не найдена в базе данных.")
            conn.close()
            return

        # Добавляем id_course в данные для вставки
        data["id_course"] = id_course

        # Валидация данных занятия
        validate_Class(data, conn)
    except ValueError as e:
        print(f"Ошибка валидации: {e}")
        conn.close()
        return

    try:
        with conn.cursor() as cur:
            insert_query = """
                INSERT INTO "Class" (date_time, type, id_course, shifr, id_professor, class_number)
                VALUES (%(date_time)s, %(type)s, %(id_course)s, %(shifr)s, %(id_professor)s, %(class_number)s)
            """
            cur.execute(insert_query, data)
            conn.commit()
            print("Занятие успешно добавлено в базу данных.")

    except Exception as e:
        print(f"Ошибка при добавлении занятия: {e}")
        conn.rollback()

    finally:
        conn.close()
        print("Соединение с базой данных закрыто.")
