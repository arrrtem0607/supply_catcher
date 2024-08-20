from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

# Конфигурация базы данных
DB_CONFIG = {
    'dbname': 'catcher',
    'user': 'postgres',
    'password': '',
    'host': '45.144.233.139',
    'port': '5432'
}

DATABASE_URL = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}"


def check_connection():
    try:
        engine = create_engine(DATABASE_URL)
        connection = engine.connect()
        print("Подключение к базе данных прошло успешно")
        connection.close()
    except OperationalError as e:
        print(f"Ошибка подключения: {e}")


if __name__ == "__main__":
    check_connection()