from Interface.db_connection import connect_to_db

def validate_Student_Group(data, conn):
    if not check_if_student_exists(data["id_student"], conn):
        raise ValueError(f"Студент с id {data['id_student']} не найден.")

    if not check_if_group_exists(data["shifr"], conn):
        raise ValueError(f"Группа с шифром {data['shifr']} не найдена.")

    if check_if_student_in_group_exists(data["id_student"], data["shifr"], conn):
        raise ValueError(f"Студент {data['id_student']} уже состоит в группе {data['shifr']}.")

def check_if_student_exists(id_student, conn):
    try:
        with conn.cursor() as cur:
            cur.execute('SELECT COUNT(*) FROM "Student" WHERE id_student = %s', (id_student,))
            result = cur.fetchone()
            return result[0] > 0
    except Exception as e:
        print(f"Ошибка при проверке студента: {e}")
        return False

def check_if_group_exists(shifr, conn):
    try:
        with conn.cursor() as cur:
            cur.execute('SELECT COUNT(*) FROM "Group" WHERE shifr = %s', (shifr,))
            result = cur.fetchone()
            return result[0] > 0
    except Exception as e:
        print(f"Ошибка при проверке группы: {e}")
        return False

def check_if_student_in_group_exists(id_student, shifr, conn):
    try:
        with conn.cursor() as cur:
            cur.execute('SELECT COUNT(*) FROM "Student_Group" WHERE id_student = %s AND shifr = %s', (id_student, shifr))
            result = cur.fetchone()
            return result[0] > 0
    except Exception as e:
        print(f"Ошибка при проверке студента в группе: {e}")
        return False

def add_Student_to_Group(data):
    conn = connect_to_db()
    if conn is None:
        print("Не удалось подключиться к базе данных.")
        return

    try:
        validate_Student_Group(data, conn)
    except ValueError as e:
        print(f"Ошибка валидации: {e}")
        conn.close()
        return

    try:
        with conn.cursor() as cur:
            insert_query = """
                INSERT INTO "Student_Group" (id_student, shifr)
                VALUES (%(id_student)s, %(shifr)s)
            """
            cur.execute(insert_query, data)
            conn.commit()
            print(f"Студент {data['id_student']} успешно добавлен в группу {data['shifr']}.")
    except Exception as e:
        print(f"Ошибка при добавлении студента в группу: {e}")
        conn.rollback()
    finally:
        conn.close()
        print("Соединение с базой данных закрыто.")

def add_Multiple_Students_to_Group(id_student_list, shifr):
    """Добавление сразу нескольких студентов в одну группу."""
    conn = connect_to_db()
    if conn is None:
        print("Не удалось подключиться к базе данных.")
        return

    try:
        if not check_if_group_exists(shifr, conn):
            raise ValueError(f"Группа с шифром {shifr} не найдена.")

        with conn.cursor() as cur:
            for id_student in id_student_list:
                try:
                    if not check_if_student_exists(id_student, conn):
                        print(f"Пропуск: Студент с id {id_student} не найден.")
                        continue

                    if check_if_student_in_group_exists(id_student, shifr, conn):
                        print(f"Пропуск: Студент {id_student} уже состоит в группе {shifr}.")
                        continue

                    insert_query = """
                        INSERT INTO "Student_Group" (id_student, shifr)
                        VALUES (%s, %s)
                    """
                    cur.execute(insert_query, (id_student, shifr))
                    print(f"Студент {id_student} добавлен в группу {shifr}.")
                except Exception as e:
                    print(f"Ошибка при добавлении студента {id_student}: {e}")
            conn.commit()
    except Exception as e:
        print(f"Ошибка при добавлении студентов: {e}")
        conn.rollback()
    finally:
        conn.close()
        print("Соединение с базой данных закрыто.")
