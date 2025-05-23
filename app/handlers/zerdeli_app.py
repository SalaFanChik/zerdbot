from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
from app.utils.texts import answer, FAQ_TEXT_KAZ, FAQ_TEXT_RUS
from app.db.user_crud import get_user_lang
from app.keyboards.reply import get_support_menu, get_main_menu
from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession


router = Router()

BASE_PATH = Path("app") / "images"

@router.message(F.text.func(lambda text: "технический" in text.lower() or "техникалық" in text.lower()))
async def handle_support_start(message: Message, state: FSMContext, session: AsyncSession):
    lang = await get_user_lang(session, message.from_user.id)
    await message.answer(answer["choose"][lang], reply_markup=get_support_menu(lang))
    await state.clear()

@router.message(F.text.func(lambda text: "тіркел" in text.lower()))
async def handle_register_help(message: Message, session: AsyncSession):
    lang = await get_user_lang(session, message.from_user.id)
    file_path = BASE_PATH / ("IMG_2377.MOV" if lang == "kz" else "IMG_2378.MOV")
    video = FSInputFile(file_path)
    await message.answer_video(video)

@router.message(F.text.func(lambda text: "сертификат" in text.lower()))
async def handle_certificate_help(message: Message, session: AsyncSession):
    lang = await get_user_lang(session, message.from_user.id)
    print(lang)
    file_path = BASE_PATH / ("kaz.pdf" if lang == "kz" else "rus.pdf")
    document = FSInputFile(file_path)
    await message.answer_document(document)

@router.message(F.text.func(lambda text: "Часто задаваемые вопросы" in text or "Жиі қойылатын сұрақтар" in text))
async def handle_frequently_asked(message: Message, session: AsyncSession):
    lang = await get_user_lang(session, message.from_user.id)
    text = FAQ_TEXT_KAZ if lang == "kz" else FAQ_TEXT_RUS
    await message.answer(text, reply_markup=get_main_menu(lang))
