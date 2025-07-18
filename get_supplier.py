import requests
import json
import os
from dotenv import load_dotenv
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()

def get_suppliers(authorization_id=4):
    """
    Получение списка поставщиков по JWT токену
    
    Args:
        authorization_id (int): ID авторизации для получения поставщиков
        
    Returns:
        dict: Данные поставщиков или None в случае ошибки
    """
    access_token = os.getenv('ACCESS_TOKEN')
    
    # URL для получения поставщиков
    url = "https://postavkamp.ru/api/supply-wb/suppliers/"
    
    # Заголовки с access токеном
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    # Данные для POST запроса
    data = {
        "authorization_id": authorization_id
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
            return response_data
        else:
            logging.error(f"Ошибка при получении поставщиков. Статус: {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        logging.error(f"Ошибка при выполнении запроса: {str(e)}")
        return None

if __name__ == "__main__":
    get_suppliers()
