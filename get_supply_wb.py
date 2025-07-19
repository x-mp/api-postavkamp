import requests
import json
import os
from dotenv import load_dotenv
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_supply_wb(authorization_id):
    """
    Получение списка поставщиков и их поставок по токену авторизации
    
    Args:
        authorization_id (int): ID авторизации
        
    Returns:
        dict: Данные о поставках или None в случае ошибки
    """
    load_dotenv()
    
    access_token = os.getenv('ACCESS_TOKEN')
    
    # URL для получения поставок
    url = "https://postavkamp.ru/api/supply-wb/supply/"
    
    # Заголовки с access токеном
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "accept": "application/json"
    }
    
    # Данные для POST запроса
    data = {
        "authorization_id": authorization_id
    }
    
    # Создание директории data, если она не существует
    os.makedirs('data', exist_ok=True)
    
    try:
        # Отправка POST запроса для получения поставок
        response = requests.post(url, headers=headers, json=data)
        
        # Проверка статуса ответа
        if response.status_code == 200:
            response_data = response.json()
            logging.info(f"Результат: {response_data}")
            # Сохранение результата в JSON файл в папку data
            with open('data/supply_wb_result.json', 'w', encoding='utf-8') as f:
                json.dump(response_data, f, ensure_ascii=False, indent=2)
            logging.info("Результат сохранен в data/supply_wb_result.json")
            return response_data
        else:
            logging.error(f"Ошибка при получении поставок. Статус: {response.status_code}")
            logging.error(f"Ответ сервера: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        logging.error(f"Ошибка при выполнении запроса: {str(e)}")
        return None
    except json.JSONDecodeError as e:
        logging.error(f"Ошибка при декодировании JSON: {str(e)}")
        return None

if __name__ == "__main__":
    # Пример использования функции
    authorization_id = 4
    result = get_supply_wb(authorization_id)



