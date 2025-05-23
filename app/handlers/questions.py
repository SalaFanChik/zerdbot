from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
from app.utils.texts import answer, FAQ_TEXT_KAZ, FAQ_TEXT_RUS
from app.db.db import get_user_lang
from app.keyboards.reply import get_support_menu, get_main_menu



router = Router()

@router.message(F.text.func(lambda text: "технический" in text.lower() or "техникалық" in text.lower()))
async def handle_support_start(message: Message, state: FSMContext):
    lang = get_user_lang(message.from_user.id)
    await message.answer(answer["choose"][lang], reply_markup=get_support_menu(lang))
    await state.clear()

@router.message(F.text.func(lambda text: "тіркел" in text.lower()))
async def handle_register_help(message: Message):
    lang = get_user_lang(message.from_user.id)
    if lang == "kz":
        video = FSInputFile(r"app\images\IMG_2377.MOV") 
        await message.answer_video(video)
    else:
        video = FSInputFile(r"app\images\IMG_2378.MOV") 
        await message.answer_video(video)


@router.message(F.text.func(lambda text: "сертификат" in text.lower()))
async def handle_certificate_help(message: Message):
    lang = get_user_lang(message.from_user.id)
    if lang == "kz":
        video = FSInputFile(r"app\images\kaz.pdf") 
        await message.answer_document(video)
    else:
        video = FSInputFile(r"app\images\rus.pdf") 
        await message.answer_document(video)



@router.message(F.text.func(lambda text: "Часто задаваемые вопросы" in text or "Жиі қойылатын сұрақтар" in text))
async def handle_frequently_asked(message: Message):
    lang = get_user_lang(message.from_user.id)

    if lang == "kz":
        await message.answer(FAQ_TEXT_KAZ, reply_markup=get_main_menu(lang))
    else:
        await message.answer(FAQ_TEXT_RUS, reply_markup=get_main_menu(lang))