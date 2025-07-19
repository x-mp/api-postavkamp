# api-postavkamp

Набор скриптов и библиотека для работы с сервисом [postavkamp.ru](https://postavkamp.ru/) (получение данных Wildberries).

## Структура проекта

- `postavkamp/` — Python‑пакет с функциями для вызова API.
- `scripts/` — примеры и утилиты для запуска из консоли.
- `data/` — сюда сохраняются результаты работы скриптов.

## Быстрый старт

1. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
2. Скопируйте `.env_example` в `.env` и заполните переменные:
   - `ACCESS_TOKEN` — JWT токен PostavkaMP;
   - `TELEGRAM_BOT_TOKEN` и `TELEGRAM_CHAT_ID` — для отправки отчетов в Telegram;
   - `GOOGLE_CREDENTIALS` — путь к файлу сервисного аккаунта Google;
   - `GOOGLE_SHEET_ID` — ID вашей таблицы;
   - `AUTHORIZATION_ID` — ID кабинета Wildberries.

## Запуск

### Создание отчета и отправка в Telegram
```bash
python scripts/generate_report.py
```
Файлы `report.xlsx` и `report.csv` будут сохранены в каталоге `data/` и отправлены в Telegram.

### Обновление Google Sheets каждые 30 минут
```bash
python scripts/update_google_sheet.py
```
Скрипт обновит листы `Suppliers` и `Supplies` указанной таблицы.

### Получение сырых данных
- `scripts/get_auth_wb.py` — список авторизаций;
- `scripts/get_supplier.py` — список поставщиков;
- `scripts/get_supply_wb.py` — данные о поставках;
- `scripts/get_supply_product.py` — продукты конкретной поставки (используйте `SUPPLIER_ID` и `PREORDER_ID` в `.env`).

## API
- **Базовый URL:** <https://postavkamp.ru/api>
- **Документация:** <https://postavkamp.ru/api/docs>
- **Получение токена:** <https://postavkamp.ru/api/get-token/>

## Контакты
По вопросам доступа и поддержки — Telegram: [@postavkamp_admin](https://t.me/postavkamp_admin)
