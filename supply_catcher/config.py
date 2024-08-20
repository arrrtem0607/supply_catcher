import logging

# Настройка логирования
# Основной логгер
logging.basicConfig(
    filename='supply_catcher.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Логгер для обновлений
update_logger = logging.getLogger('updates')
update_handler = logging.FileHandler('updates.log')
update_handler.setLevel(logging.INFO)
update_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
update_logger.addHandler(update_handler)

# Конфигурация базы данных
DB_CONFIG = {
    'dbname': 'supply_catcher',
    'user': 'artem',
    'password': '',
    'host': 'localhost',
    'port': '5432'
}

# URL для API
URL_WAREHOUSES = "https://supplies-api.wildberries.ru/api/v1/warehouses"
URL_COEFFICIENTS = "https://supplies-api.wildberries.ru/api/v1/acceptance/coefficients"

# API ключ
API_KEY = ("eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjQwODAxdjEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTczOTg0MjYwMSwiaWQiO"
           "iJjY2RhZTFiNC1jYTIwLTRjZDMtOWJlMC0wMmE3YjBmZDhmZmEiLCJpaWQiOjU1ODM4ODgxLCJvaWQiOjI4ODkwMCwicyI6MTA3Mzc1MD"
           "AxNCwic2lkIjoiMWVhOTBlZTAtZmE1Yi00MTQxLThlOGMtZTZlOGZlZWQxMzllIiwidCI6ZmFsc2UsInVpZCI6NTU4Mzg4ODF9.xL7v"
           "Khx5AoBSxqCRFyIrSKrxiPFEcQjl46oQ4Q6p6tUJ2oqDBgvlP5nAc2lrJdpGfUyYAUdrxjwBopuWv4o3Sg")
