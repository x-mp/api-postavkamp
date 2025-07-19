import json
import logging
import os
from pathlib import Path
from typing import Optional

import requests
from dotenv import load_dotenv


load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def get_supply_wb(authorization_id: int) -> Optional[dict]:
    """Return supply data for the given authorization."""
    access_token = os.getenv("ACCESS_TOKEN")
    url = "https://postavkamp.ru/api/supply-wb/supply/"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "accept": "application/json",
    }
    data = {"authorization_id": authorization_id}
    Path("data").mkdir(exist_ok=True)
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            result = response.json()
            with open("data/supply_wb_result.json", "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            logging.info("Результат сохранен в data/supply_wb_result.json")
            return result
        logging.error("Ошибка при получении поставок. Статус: %s", response.status_code)
        logging.error("Ответ сервера: %s", response.text)
        return None
    except (requests.RequestException, json.JSONDecodeError) as exc:
        logging.error("Ошибка при выполнении запроса: %s", exc)
        return None


def get_supply_products(
    authorization_id: int, supplier_id: str, preorder_id: int
) -> Optional[dict]:
    """Return products for a supply."""
    access_token = os.getenv("ACCESS_TOKEN")
    url = "https://postavkamp.ru/api/supply-wb/supply-products/"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "accept": "application/json",
    }
    data = {
        "authorization_id": authorization_id,
        "supplier_id": supplier_id,
        "preorder_id": preorder_id,
    }
    Path("data").mkdir(exist_ok=True)
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            result = response.json()
            with open("data/supply_products_result.json", "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            logging.info("Результат сохранен в data/supply_products_result.json")
            return result
        logging.error(
            "Ошибка при получении продуктов поставки. Статус: %s", response.status_code
        )
        logging.error("Ответ сервера: %s", response.text)
        return None
    except (requests.RequestException, json.JSONDecodeError) as exc:
        logging.error("Ошибка при выполнении запроса: %s", exc)
        return None
