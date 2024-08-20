import logging
import time
from api.coefficients import update_coefficients
from db.connection import engine
from api.coefficients import get_warehouses_once

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def main():
    # Получение данных о складах один раз при запуске программы
    warehouse_ids = get_warehouses_once()

    if not warehouse_ids:
        logging.error("Не удалось получить данные о складах. Программа завершена.")
        return

    while True:
        logging.info("Запуск программы.")
        try:
            update_coefficients(engine, warehouse_ids)
        except Exception as e:
            logging.error(f"Произошла ошибка при обновлении коэффициентов: {e}")
        # Задержка перед следующим запуском
        time.sleep(1)  # Устанавливаем интервал в 60 секунд


if __name__ == "__main__":
    main()
