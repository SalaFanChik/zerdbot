from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.text == "🧾 О компании")
async def company_info_handler(message: Message):
    """Handler for /company_info command"""
    await message.answer("Welcome to Zerdeli! We provide excellent education services.")
