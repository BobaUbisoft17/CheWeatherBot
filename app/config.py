"""Конфиг со всеми важными переменными.

Все данные экспортируются из переменных окружения
"""

import os


BOT_TOKEN = os.getenv("BOT_TOKEN")

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

RUN_TYPE = os.getenv("RUN_TYPE", "polling")

DATABASE_URL = os.getenv("DATABASE_URL", "subscribers.db")

if RUN_TYPE == "webhook":
    WEBHOOK_URL = os.getenv("WEBHOOK_URL")

    WEBHOOK_PATH = os.getenv("WEBHOOK_PATH", "")

    WEBHOOK_HOST = os.getenv("WEBHOOK_POST", "0.0.0.0")

    WEBHOOK_PORT = os.getenv("WEBHOOK_PORT", 8080)
