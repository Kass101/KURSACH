import psycopg2
from psycopg2 import errors

def connect_to_db():
    try:
        return psycopg2.connect(
            dbname='BD_CPK',
            user='postgres',
            password='123',
            host='localhost',
            port='5432'
        )
    except psycopg2.OperationalError as e:
        print(f"Ошибка при подключении к БД: {e}")
        return None
    except Exception as e:
        print(f"Неизвестная ошибка при подключении к БД: {e}")
        return None
