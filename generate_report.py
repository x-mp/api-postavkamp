import os
import logging
import pandas as pd
from dotenv import load_dotenv

from get_auth_wb import get_active_authorizations
from get_supplier import get_suppliers
from get_supply_wb import get_supply_wb
from get_supply_product import get_supply_products

import requests

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def send_file_to_telegram(file_path: str) -> None:
    """Send a file to telegram using bot token and chat id from environment."""
    load_dotenv()
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not bot_token or not chat_id:
        logging.error("TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not set")
        return

    url = f"https://api.telegram.org/bot{bot_token}/sendDocument"
    with open(file_path, "rb") as f:
        response = requests.post(url, data={"chat_id": chat_id}, files={"document": f})
    if response.status_code == 200:
        logging.info("File %s sent to Telegram", file_path)
    else:
        logging.error("Failed to send file to Telegram: %s", response.text)


def collect_supply_products(authorization_id: int, supplies: dict) -> list:
    """Collect supply product details for all suppliers/preorders."""
    products = []
    if not supplies:
        return products

    for supplier in supplies.get("suppliers", []):
        supplier_id = supplier.get("supplier_id") or supplier.get("id")
        for preorder in supplier.get("preorders", []):
            preorder_id = preorder.get("preorder_id") or preorder.get("id")
            data = get_supply_products(authorization_id, supplier_id, preorder_id)
            if not data:
                continue
            for item in data.get("products", data if isinstance(data, list) else []):
                if isinstance(item, dict):
                    item.setdefault("supplier_id", supplier_id)
                    item.setdefault("preorder_id", preorder_id)
                products.append(item)
    return products


def generate_report(authorization_id: int) -> tuple[str, str]:
    """Generate Excel and CSV report files and return their paths."""
    os.makedirs("data", exist_ok=True)

    auths = get_active_authorizations()
    suppliers = get_suppliers(authorization_id=authorization_id)
    supplies = get_supply_wb(authorization_id)
    supply_products = collect_supply_products(authorization_id, supplies)

    df_auths = pd.json_normalize(auths) if auths else pd.DataFrame()
    df_suppliers = pd.json_normalize(suppliers) if suppliers else pd.DataFrame()
    df_products = pd.json_normalize(supply_products)

    excel_path = os.path.join("data", "report.xlsx")
    csv_path = os.path.join("data", "report.csv")

    with pd.ExcelWriter(excel_path) as writer:
        df_auths.to_excel(writer, sheet_name="cabinets", index=False)
        df_suppliers.to_excel(writer, sheet_name="suppliers", index=False)
        df_products.to_excel(writer, sheet_name="products", index=False)
    df_products.to_csv(csv_path, index=False)

    logging.info("Reports saved to %s and %s", excel_path, csv_path)
    return excel_path, csv_path


def main() -> None:
    load_dotenv()
    authorization_id = int(os.getenv("AUTHORIZATION_ID", "4"))
    excel_file, csv_file = generate_report(authorization_id)
    send_file_to_telegram(excel_file)
    send_file_to_telegram(csv_file)


if __name__ == "__main__":
    main()
