# Учёт заказов

Веб-приложение на Flask и SQLite: добавление, поиск, фильтрация заказов, смена статуса, удаление, сводная статистика.

## Запуск
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```
Откройте http://127.0.0.1:5000

## Структура
- `app.py`: маршруты и работа с базой
- `schema.sql`: схема БД (ограничения CHECK, индекс по статусу)
- `templates/index.html`: интерфейс

Все запросы к базе параметризованы (защита от SQL-инъекций), вывод экранируется Jinja2.
