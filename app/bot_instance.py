# app/bot_instance.py
from aiogram import Bot

from app.core.settings import get_settings

config = get_settings()
bot = Bot(token=config.bot_token)
