import requests
import logging
import pandas as pd
from sqlalchemy.orm import sessionmaker
from catcher.config import URL_COEFFICIENTS, API_KEY, update_logger
from catcher.db.models import Coefficient
from catcher.api.warehouses import get_warehouses


def fetch_last_coefficients(session):
    """Fetch the last coefficients from the database."""
    result = session.query(Coefficient).all()
    if not result:
        logging.warning("Предыдущие данные отсутствуют в базе.")
        return pd.DataFrame()  # Возвращаем пустой DataFrame, если данных нет
    return pd.DataFrame([{
        "date": coeff.date,
        "coefficient": coeff.coefficient,
        "warehouse_id": coeff.warehouse_id,
        "warehouse_name": coeff.warehouse_name,
        "box_type_name": coeff.box_type_name,
        "box_type_id": coeff.box_type_id
    } for coeff in result])


def get_warehouses_once():
    warehouses = get_warehouses()

    if not warehouses:
        logging.error("Не удалось получить данные о складах.")
        return []

    logging.info(f"Полученные данные о складах: {warehouses}")

    warehouse_ids = []
    for warehouse in warehouses:
        try:
            warehouse_ids.append(str(warehouse['ID']))
        except KeyError:
            logging.error(f"Ошибка: отсутствует ключ 'ID' в данных склада: {warehouse}")

    if not warehouse_ids:
        logging.error("Не удалось собрать ID складов. Программа завершена.")
    else:
        logging.info(f"Успешно получены ID для {len(warehouse_ids)} складов.")

    return warehouse_ids


def update_coefficients(engine, warehouse_ids):
    logging.info("Начало обновления коэффициентов...")

    params = {
        "warehouseIDs": ",".join(warehouse_ids)
    }

    response = requests.get(URL_COEFFICIENTS, headers={"Authorization": f"{API_KEY}"}, params=params)

    if response.status_code == 200:
        coefficients = response.json()
        logging.info(f"Получено {len(coefficients)} коэффициентов.")

        # Преобразуем данные в DataFrame и переименовываем колонки
        new_df = pd.DataFrame(coefficients)
        new_df.rename(columns={
            "date": "date",
            "warehouseID": "warehouse_id",
            "warehouseName": "warehouse_name",
            "boxTypeName": "box_type_name",
            "boxTypeID": "box_type_id",
        }, inplace=True)

        # Заполняем отсутствующие значения в box_type_id значением по умолчанию (например, 0)
        new_df['box_type_id'] = new_df['box_type_id'].fillna(0)

        # Преобразуем дату в формат datetime64[ns]
        new_df['date'] = pd.to_datetime(new_df['date']).dt.tz_localize(None)

        session_start = sessionmaker(bind=engine)
        session = session_start()

        try:
            for _, row in new_df.iterrows():
                existing_record = session.query(Coefficient).filter(
                    Coefficient.date == row['date'],
                    Coefficient.warehouse_id == row['warehouse_id'],
                    Coefficient.box_type_id == row['box_type_id']
                ).first()

                if existing_record:
                    if (existing_record.coefficient != row['coefficient'] or
                            existing_record.warehouse_name != row['warehouse_name'] or
                            existing_record.box_type_name != row['box_type_name']):
                        # Логируем изменения в общий лог и в лог для обновлений
                        update_message = (
                            f"Обновлена запись для склада {row['warehouse_name']} "
                            f"на дату {row['date'].date()} с коэффициента {existing_record.coefficient} "
                            f"на {row['coefficient']}"
                        )
                        logging.info(update_message)
                        update_logger.info(update_message)

                        existing_record.coefficient = row['coefficient']
                        existing_record.warehouse_name = row['warehouse_name']
                        existing_record.box_type_name = row['box_type_name']
                        session.add(existing_record)
                else:
                    new_coeff = Coefficient(
                        date=row['date'],
                        coefficient=row['coefficient'],
                        warehouse_id=row['warehouse_id'],
                        warehouse_name=row['warehouse_name'],
                        box_type_name=row['box_type_name'],
                        box_type_id=row['box_type_id']
                    )
                    session.add(new_coeff)
                    logging.info(
                        f"Добавлена новая запись для склада {row['warehouse_name']} на дату {row['date'].date()}")
            session.commit()
            logging.info("Обновление данных завершено успешно.")

        except Exception as e:
            session.rollback()
            logging.error(f"Ошибка при обновлении коэффициентов: {str(e)}")
        finally:
            session.close()
    else:
        logging.error(f"Ошибка: {response.status_code}, текст ошибки: {response.text}")
