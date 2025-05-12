import logging
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command
from app.keyboards.reply import get_main_menu, lang_kb
from aiogram.fsm.context import FSMContext
from app.db.db import set_user_lang, get_user_lang
from app.states.lang_state import Form 
from app.handlers.company import router as company_router
from app.handlers.questions import router as question_router
from app.handlers.products import router as product_router
from app.handlers.altynasyq import router as altynasyq_router
from aiogram import Router
from app.utils.texts import answer
from app.db.db import init_db
from dotenv import load_dotenv
import os
load_dotenv()

TOKEN = os.getenv("TOKEN") 

bot = Bot(token=TOKEN)
dp = Dispatcher()

dp.include_router(company_router)
dp.include_router(product_router)
dp.include_router(altynasyq_router)
dp.include_router(question_router)



@dp.message(Command("start"))
async def start_handler(message: Message, state: FSMContext):
    """ Handler for /start command """
    await message.answer("Сәлеметсіз бе?! Сізге қай тілде жауап алған ыңғайлы?\n\n Здравствуйте! На каком языке вам удобно получить ответ?", reply_markup=lang_kb)
    
    await state.set_state(Form.choose_language) 
    

@dp.message(Form.choose_language, F.text.in_(["Қазақша", "Русский"]))
async def set_language(message: Message, state: FSMContext):
    lang = "kz" if message.text == "Қазақша" else "ru"
    set_user_lang(message.from_user.id, lang)
    await message.answer(answer["greeting"][lang], reply_markup=get_main_menu(lang))
    await state.clear()



async def main():
    init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
