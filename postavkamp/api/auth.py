import json
import logging
import os
from pathlib import Path
from typing import Optional

import requests
from dotenv import load_dotenv


load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def get_active_authorizations() -> Optional[dict]:
    """Return a list of active authorizations from postavkamp."""
    access_token = os.getenv("ACCESS_TOKEN")
    url = "https://postavkamp.ru/api/authorization-wb/get-authorization/"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "accept": "*/*",
    }
    Path("data").mkdir(exist_ok=True)
    try:
        response = requests.post(url, headers=headers, data="")
        if response.status_code == 200:
            data = response.json()
            with open("data/active_authorizations.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logging.info("Результат сохранен в data/active_authorizations.json")
            return data
        logging.error("Ошибка при получении авторизаций. Статус: %s", response.status_code)
        return None
    except (requests.RequestException, json.JSONDecodeError) as exc:
        logging.error("Ошибка при выполнении запроса: %s", exc)
        return None
