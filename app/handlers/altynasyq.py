from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
import re 
from app.utils.texts import answer
from app.db.db import get_user_lang
from app.keyboards.reply import get_altynasyq_menu, get_main_menu
from app.states.user_state import InfoForm
from app.utils.create_lead import create_amocrm_lead_and_contact


router = Router()

@router.message(F.text.func(lambda text: "Алтын Асық" in text or "Алтын" in text))
async def handle_altynasyq(message: Message):
    lang = get_user_lang(message.from_user.id)
    photo = FSInputFile(r"app\images\alt.jpg")
    caption = answer["altynasyq_info"][lang]
    await message.answer_photo(photo, caption=caption, reply_markup=get_altynasyq_menu(lang))

@router.message(F.text.func(lambda text: "Толығырақ" in text or "Подробнее" in text))
async def handle_more_info(message: Message, state: FSMContext):
    lang = get_user_lang(message.from_user.id)
    await message.answer(answer["ask_name"][lang])
    await state.set_state(InfoForm.name)

@router.message(F.text.func(lambda text: "Артқа" in text or "Назад" in text))
async def handle_back(message: Message, state: FSMContext):
    lang = get_user_lang(message.from_user.id)
    await message.answer(answer["greeting"][lang], reply_markup=get_main_menu(lang))
    await state.clear()

@router.message(InfoForm.name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    lang = get_user_lang(message.from_user.id)
    await message.answer(answer["ask_region"][lang])
    await state.set_state(InfoForm.region)

@router.message(InfoForm.region)
async def process_region(message: Message, state: FSMContext):
    lang = get_user_lang(message.from_user.id)
    
    if not re.fullmatch(r"[А-Яа-яӘәӨөҚқҰұҮүІіЁё\s\-]+", message.text):
        await message.answer("❗ Өтінеміз, облыс атауын тек әріптермен жазыңыз.")
        return

    await state.update_data(region=message.text)
    await message.answer(answer["ask_phone"][lang])
    await state.set_state(InfoForm.phone)

@router.message(InfoForm.phone)
async def process_phone(message: Message, state: FSMContext):
    lang = get_user_lang(message.from_user.id)
    phone = message.text.strip()

    if not re.fullmatch(r"(\+7|8)\d{10}", phone):
        await message.answer("📵 Телефон нөмірі қате. Мысалы: +77001234567 немесе 87001234567")
        return

    await state.update_data(phone=phone)
    data = await state.get_data()

    success, result = await create_amocrm_lead_and_contact(
        name=data.get("name"),
        phone=data.get("phone"),
        region=data.get("region")
    )

    if success:
        await message.answer(answer["thank_you"][lang], reply_markup=get_main_menu(lang))
    else:
        await message.answer("❗ Қате орын алды. Өтініш кейінірек қайталап көріңіз.")
        print(result)

    await state.clear()









