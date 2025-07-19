import os
import json
import time
import logging
import sys
from pathlib import Path
from dotenv import load_dotenv
import gspread
from google.oauth2.service_account import Credentials

sys.path.append(str(Path(__file__).resolve().parents[1]))

from postavkamp import get_suppliers, get_supply_wb

load_dotenv()

GOOGLE_CREDENTIALS = os.getenv('GOOGLE_CREDENTIALS', 'google_credentials.json')
GOOGLE_SHEET_ID = os.getenv('GOOGLE_SHEET_ID')
AUTHORIZATION_ID = int(os.getenv('AUTHORIZATION_ID', '4'))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def authorize_gspread():
    scopes = ['https://www.googleapis.com/auth/spreadsheets']
    creds = Credentials.from_service_account_file(GOOGLE_CREDENTIALS, scopes=scopes)
    client = gspread.authorize(creds)
    return client


def write_dicts(worksheet, data_list):
    """Записывает список словарей в лист Google Sheets."""
    worksheet.clear()
    if not data_list:
        return
    headers = list(data_list[0].keys())
    rows = [headers]
    for item in data_list:
        rows.append([item.get(h, '') for h in headers])
    worksheet.update(rows)


def update_google_sheet():
    client = authorize_gspread()
    spreadsheet = client.open_by_key(GOOGLE_SHEET_ID)

    suppliers_data = get_suppliers(AUTHORIZATION_ID) or {}
    supplies_data = get_supply_wb(AUTHORIZATION_ID) or {}

    suppliers_list = suppliers_data.get('data') or suppliers_data.get('result') or suppliers_data
    supplies_list = supplies_data.get('data') or supplies_data.get('result') or supplies_data

    suppliers_list = suppliers_list if isinstance(suppliers_list, list) else []
    supplies_list = supplies_list if isinstance(supplies_list, list) else []

    suppliers_sheet = spreadsheet.worksheet('Suppliers')
    write_dicts(suppliers_sheet, suppliers_list)

    supplies_sheet = spreadsheet.worksheet('Supplies')
    write_dicts(supplies_sheet, supplies_list)

    logging.info('Данные успешно обновлены в Google Sheets')


def main_loop():
    while True:
        try:
            update_google_sheet()
        except Exception as e:
            logging.error(f'Ошибка при обновлении таблицы: {e}')
        time.sleep(1800)


if __name__ == '__main__':
    main_loop()
