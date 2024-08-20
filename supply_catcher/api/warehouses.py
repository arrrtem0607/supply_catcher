import requests
import logging
from ..config import URL_WAREHOUSES, API_KEY

logger = logging.getLogger(__name__)


def get_warehouses():
    try:
        headers = {
            "Authorization": f"{API_KEY}"
        }
        response = requests.get(URL_WAREHOUSES, headers=headers)

        if response.status_code == 200:
            logger.info("Склады успешно получены.")
            return response.json()
        else:
            logger.error(f"Ошибка: {response.status_code}, текст ошибки: {response.text}")
            return []
    except Exception as e:
        logger.error(f"Произошла ошибка при получении складов: {e}")
        return []
