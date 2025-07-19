# api-postavkamp

Сервис API для получения данных через API Wildberries, расположенный на postavkamp.ru

## Описание
Набор Python скриптов для работы с API Wildberries через сервис postavkamp.ru. Позволяет получать данные о поставках, товарах и поставщиках.

## API
- **Базовый URL**: https://postavkamp.ru/api
- **Документация**: https://postavkamp.ru/api/docs
- **Получение токена авторизации**: https://postavkamp.ru/api

## Контакты
Для получения доступа и поддержки обращайтесь к администратору:
- **Telegram**: @postavkamp_admin



## Интеграция с Google Sheets

1. Создайте проект в [Google Cloud Console](https://console.cloud.google.com/).
2. Включите API `Google Sheets API` для вашего проекта.
3. Создайте сервисный аккаунт и сгенерируйте JSON‑ключ. Скачайте его и сохраните, например, как `google_credentials.json`.
4. Откройте нужную Google таблицу и поделитесь ею с email сервисного аккаунта.
5. Скопируйте ID таблицы из её URL и укажите в переменной окружения `GOOGLE_SHEET_ID`.
6. Заполните файл `.env` по примеру `.env_example`, добавив путь к ключу `GOOGLE_CREDENTIALS`, `GOOGLE_SHEET_ID` и `AUTHORIZATION_ID`.

Скрипт `update_google_sheet.py` запускает получение данных из API и каждые 30 минут обновляет два листа Google таблицы:

```bash
python update_google_sheet.py
```

В таблице должны существовать листы `Suppliers` и `Supplies`.

