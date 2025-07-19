import json
import logging
import os
from pathlib import Path
from typing import Optional

import requests
from dotenv import load_dotenv


load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def get_suppliers(authorization_id: int = 4) -> Optional[dict]:
    """Return suppliers list using a given authorization id."""
    access_token = os.getenv("ACCESS_TOKEN")
    url = "https://postavkamp.ru/api/supply-wb/suppliers/"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    data = {"authorization_id": authorization_id}
    Path("data").mkdir(exist_ok=True)
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            result = response.json()
            with open("data/suppliers_result.json", "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            logging.info("Результат сохранен в data/suppliers_result.json")
            return result
        logging.error("Ошибка при получении поставщиков. Статус: %s", response.status_code)
        return None
    except requests.RequestException as exc:
        logging.error("Ошибка при выполнении запроса: %s", exc)
        return None
