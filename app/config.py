# app/config.py
import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    GROUP_IDS = [int(id) for id in os.getenv("GROUP_IDS", "").split(",") if id]
    WEBHOOK_URL = os.getenv("WEBHOOK_URL")
    WEBAPP_HOST = os.getenv("WEBAPP_HOST", "0.0.0.0")
    WEBAPP_PORT = int(os.getenv("WEBAPP_PORT", 8000))
