import requests
import json
import os
from dotenv import load_dotenv
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_supply_products(authorization_id, supplier_id, preorder_id):
    """
    Получение продуктов поставки по JWT токену
    
    Args:
        authorization_id (int): ID авторизации
        supplier_id (str): ID поставщика
        preorder_id (int): ID предзаказа
    
    Returns:
        dict: Данные о продуктах поставки или None в случае ошибки
    """
    load_dotenv()
    
    access_token = os.getenv('ACCESS_TOKEN')
    
    # URL для получения продуктов поставки
    url = "https://postavkamp.ru/api/supply-wb/supply-products/"
    
    # Заголовки с access токеном
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "accept": "application/json"
    }
    
    # Данные для POST запроса
    data = {
        "authorization_id": authorization_id,
        "supplier_id": supplier_id,
        "preorder_id": preorder_id
    }
    
    # Создание директории data, если она не существует
    os.makedirs('data', exist_ok=True)
    
    try:
        # Отправка POST запроса для получения продуктов поставки
        response = requests.post(url, headers=headers, json=data)
        
        # Проверка статуса ответа
        if response.status_code == 200:
            response_data = response.json()
            logging.info(f"Результат: {response_data}")
            # Сохранение результата в JSON файл в папку data
            with open('data/supply_products_result.json', 'w', encoding='utf-8') as f:
                json.dump(response_data, f, ensure_ascii=False, indent=2)
            logging.info("Результат сохранен в data/supply_products_result.json")
            return response_data
        else:
            logging.error(f"Ошибка при получении продуктов поставки. Статус: {response.status_code}")
            logging.error(f"Ответ сервера: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        logging.error(f"Ошибка при выполнении запроса: {str(e)}")
        return None

if __name__ == "__main__":
    # Пример использования функции
    supplier_id = "cwewee2de-5dd2-4eea-8380-dwew38584fac"
    preorder_id = 1112324
    authorization_id = 4
    result = get_supply_products(
        authorization_id=authorization_id,
        supplier_id=supplier_id,
        preorder_id=preorder_id
    )
