from aiogram.types import Message, CallbackQuery
from aiogram import Router, F
from app.keyboards.inline import get_courses_kb, get_course_options_kb
from app.db.user_crud import get_user_lang
from sqlalchemy.ext.asyncio import AsyncSession
from app.keyboards.reply import get_main_menu, get_course_back_menu
from app.utils.texts import hybrid_kaz, hybrid_rus, Yearly_kaz, Yearly_rus, get_ready_kaz, get_ready_rus, answer, faq_data, reviews_data
from aiogram.fsm.context import FSMContext
from app.states.user_state import InfoForm
import re
from app.utils.create_lead import create_amocrm_lead_and_contact
from aiogram.exceptions import TelegramBadRequest

router = Router()

@router.message(F.text.in_([
    "📚 Курстар туралы білгім келеді",
    "📚 Хочу узнать больше о курсах"
]))
async def courses_info_handler(message: Message, session: AsyncSession):
    lang = await get_user_lang(session, message.from_user.id)
    await message.answer(
        "Төмендегі батырмаларды басып, курстар туралы қысқаша ақпарат алыңыз.",
        reply_markup=get_courses_kb(lang)
    )

async def safe_edit_or_send(callback: CallbackQuery, text: str, markup):
    try:
        await callback.message.edit_text(text, reply_markup=markup)
    except TelegramBadRequest:
        await callback.message.answer(text, reply_markup=markup)

@router.callback_query(F.data == "course_get_ready")
async def handle_get_ready(callback: CallbackQuery, session: AsyncSession):
    lang = await get_user_lang(session, callback.from_user.id)
    text = get_ready_kaz if lang == "kz" else get_ready_rus
    markup = get_course_options_kb("get_ready", lang)
    await callback.answer()
    await safe_edit_or_send(callback, text, markup)

@router.callback_query(F.data == "course_yearly")
async def handle_yearly(callback: CallbackQuery, session: AsyncSession):
    lang = await get_user_lang(session, callback.from_user.id)
    text = Yearly_kaz if lang == "kz" else Yearly_rus
    markup = get_course_options_kb("yearly", lang)
    await callback.answer()
    await safe_edit_or_send(callback, text, markup)

@router.callback_query(F.data == "course_hybrid")
async def handle_hybrid(callback: CallbackQuery, session: AsyncSession):
    lang = await get_user_lang(session, callback.from_user.id)
    text = hybrid_kaz if lang == "kz" else hybrid_rus
    markup = get_course_options_kb("hybrid", lang)
    await callback.answer()
    await safe_edit_or_send(callback, text, markup)

@router.callback_query(F.data == "back_to_courses")
async def back_to_courses(callback: CallbackQuery, session: AsyncSession):
    lang = await get_user_lang(session, callback.from_user.id)
    text = "Қай курс туралы білгіңіз келеді?" if lang == "kz" else "Какой курс вас интересует?"
    markup = get_courses_kb(lang)
    await callback.answer()
    await safe_edit_or_send(callback, text, markup)

@router.callback_query(F.data == "go_home")
async def go_home(callback: CallbackQuery, session: AsyncSession):
    lang = await get_user_lang(session, callback.from_user.id)
    text = "Басты бетке оралдыңыз." if lang == "kz" else "Вы вернулись на главную страницу."
    markup = get_main_menu(lang)
    await callback.answer()
    await safe_edit_or_send(callback, text, markup)

@router.callback_query(F.data.endswith("_register"))
async def handle_register(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    lang = await get_user_lang(session, callback.from_user.id)
    await callback.answer()
    await state.set_state(InfoForm.name)
    await callback.message.answer(answer["ask_name"][lang], reply_markup=get_course_back_menu(lang))


@router.message(F.text.func(lambda text: "Артқа" in text or "Назад" in text))
async def handle_back(message: Message, state: FSMContext, session: AsyncSession):
    lang = await get_user_lang(session, message.from_user.id)
    await message.answer(answer["greeting"][lang], reply_markup=get_main_menu(lang))
    await state.clear()

# FSM: Имя
@router.message(InfoForm.name)
async def process_name(message: Message, state: FSMContext, session: AsyncSession):
    await state.update_data(name=message.text)
    lang = await get_user_lang(session, message.from_user.id)
    await message.answer(answer["ask_region"][lang], reply_markup=get_course_back_menu(lang))
    await state.set_state(InfoForm.region)

# FSM: Регион
@router.message(InfoForm.region)
async def process_region(message: Message, state: FSMContext, session: AsyncSession):
    lang = await get_user_lang(session, message.from_user.id)
    if not re.fullmatch(r"[А-Яа-яӘәӨөҚқҰұҮүІіЁё\s\-]+", message.text):
        await message.answer("❗ Өтінеміз, облыс атауын тек әріптермен жазыңыз.")
        return
    await state.update_data(region=message.text)
    await message.answer(answer["ask_phone"][lang], reply_markup=get_course_back_menu(lang))
    await state.set_state(InfoForm.phone)

# FSM: Телефон
@router.message(InfoForm.phone)
async def process_phone(message: Message, state: FSMContext, session: AsyncSession):
    lang = await get_user_lang(session, message.from_user.id)
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

@router.callback_query(F.data.endswith("_faq"))
async def handle_faq(callback: CallbackQuery, session: AsyncSession):
    lang = await get_user_lang(session, callback.from_user.id)
    course = callback.data.replace("_faq", "")
    text = faq_data.get(course, {}).get(lang, "Информация пока недоступна.")
    markup = get_course_options_kb(course, lang)
    await callback.answer()
    await safe_edit_or_send(callback, text, markup)

@router.callback_query(F.data.endswith("_reviews"))
async def handle_reviews(callback: CallbackQuery, session: AsyncSession):
    lang = await get_user_lang(session, callback.from_user.id)
    course = callback.data.replace("_reviews", "")
    text = reviews_data.get(course, {}).get(lang, "Отзывы пока недоступны.")
    markup = get_course_options_kb(course, lang)
    await callback.answer()
    await safe_edit_or_send(callback, text, markup)
