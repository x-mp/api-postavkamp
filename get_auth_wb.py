import requests
import json
import os
import logging
from dotenv import load_dotenv

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Загрузка переменных окружения
load_dotenv()

access_token = os.getenv('ACCESS_TOKEN')

def get_active_authorizations():
    """
    Получение списка активных авторизаций по JWT токену
    
    Returns:
        dict: Результат выполнения запроса
    """
    
    # URL для получения активных авторизаций
    url = "https://postavkamp.ru/api/authorization-wb/get-authorization/"

    # Заголовки с access токеном
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "accept": "*/*"
    }

    # Создание директории data, если она не существует
    os.makedirs('data', exist_ok=True)

    try:
        # Отправка POST запроса для получения активных авторизаций
        response = requests.post(url, headers=headers, data='')
        
        # Проверка статуса ответа
        if response.status_code == 200:
            data = response.json()
            logging.info(f"Результат: {data}")
            # Сохранение результата в JSON файл в папку data
            with open('data/active_authorizations.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logging.info("Результат сохранен в data/active_authorizations.json")
            return data
        else:
            logging.error(f"Ошибка при получении авторизаций. Статус: {response.status_code}")
            return None
          
            
    except requests.exceptions.RequestException as e:
        logging.error(f"Ошибка при выполнении запроса: {str(e)}")
    except json.JSONDecodeError as e:
        logging.error(f"Ошибка при декодировании JSON: {str(e)}")

if __name__ == "__main__":
    get_active_authorizations()
