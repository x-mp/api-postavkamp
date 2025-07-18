import requests
import json
import os
from dotenv import load_dotenv
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()

access_token = os.getenv('ACCESS_TOKEN')

# Получение списка поставщиков по JWT токену

# URL для получения поставщиков
url = "https://postavkamp.ru/api/supply-wb/suppliers/"

# Заголовки с access токеном
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

# Данные для POST запроса
data = {
    "authorization_id": 4
}

# Создание директории data, если она не существует
os.makedirs('data', exist_ok=True)

try:
    # Отправка POST запроса для получения поставщиков
    response = requests.post(url, headers=headers, json=data)
    
    # Проверка статуса ответа
    if response.status_code == 200:
        response_data = response.json()
        logging.info(f"Результат: {response_data}")
        # Сохранение результата в JSON файл в папку data
        with open('data/suppliers_result.json', 'w', encoding='utf-8') as f:
            json.dump(response_data, f, ensure_ascii=False, indent=2)
        logging.info("Результат сохранен в data/suppliers_result.json")
    else:
        logging.error(f"Ошибка при получении поставщиков. Статус: {response.status_code}")
        
except requests.exceptions.RequestException as e:
    logging.error(f"Ошибка при выполнении запроса: {str(e)}")
