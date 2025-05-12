from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.utils.texts import answer
from app.db.db import get_user_lang
from app.states.user_state import InfoForm
from app.keyboards.reply import get_main_menu, get_course_back_menu
import re 
from app.utils.create_lead import create_amocrm_lead_and_contact



router = Router()

info_text_ru = """
<b>О компании Zerdeli Online</b>

Zerdeli Online — ведущая казахстанская онлайн образовательный центр, специализирующаяся на интеллектуальном развитии школьников и подготовке к поступлению в престижные учебные заведения. Мы создаём мощную образовательную экосистему для новых поколений лидеров, основанную на технологиях, опыте и высоких академических стандартах.

---

<b>Наши направления</b>

📌 Подготовка к элитным школам  
Курсы и тесты для поступления в НИШ, БИЛ, РФММ — с учётом всех актуальных требований и форматов.

📌 Курсы ЕНТ и олимпиады  
Комплексные программы для успешной сдачи ЕНТ и участия в предметных олимпиадах.

---

<b>Что нас отличает</b>

💻 Современная онлайн-платформа  
📍 Удобный доступ к обучению из любой точки Казахстана и за его пределами.

👩‍🏫 Лучшие преподаватели страны  
🏅 Опытные педагоги, победители республиканских олимпиад и конкурсов.

🎓 Более 100 000 успешных учеников  
Мы гордимся нашими выпускниками, поступившими в НИШ, БИЛ, РФММ, а также зарубежные школы и вузы.

---

<b>Наша миссия</b>  
Мы формируем поколение думающих, уверенных в себе и академически сильных молодых людей, готовых решать глобальные задачи и строить будущее Казахстана.
"""

info_text_kz = """
<b>Zerdeli Online компаниясы туралы</b>

Zerdeli Online — Қазақстандағы жетекші онлайн білім беру орталығы. Біз оқушылардың интеллектуалдық дамуына және НИШ, БИЛ, РФММ сияқты үздік мектептерге дайындалуына көмектесеміз. Біздің мақсатымыз — жаңа буын көшбасшыларына арналған технологиялық, тәжірибелік және жоғары академиялық деңгейдегі білім беру экожүйесін құру.

---

<b>Біздің бағыттар</b>

📌 Элиталық мектептерге дайындық  
НИШ, БИЛ, РФММ емтихандарына толық курс және тестілер — соңғы талаптарға сай.

📌 ҰБТ және олимпиадалар  
ҰБТ-ға және пәндік олимпиадаларға кешенді дайындық.

---

<b>Артықшылықтарымыз</b>

💻 Заманауи онлайн-платформа  
📍 Қазақстанның кез келген нүктесінен оқу мүмкіндігі.

👩‍🏫 Еліміздің үздік мұғалімдері  
🏅 Республикалық олимпиадалардың жеңімпаз ұстаздары.

🎓 100 000-нан астам табысты түлек  
Олар НИШ, БИЛ, РФММ және шетелдік мектептерге, университеттерге түсті.

---

<b>Біздің миссия</b>  
Біз өз болашағына сенімді, сыни ойлайтын және академиялық деңгейі жоғары жастарды қалыптастырамыз.
"""

@router.message(F.text.func(lambda text: "Курс" in text or "курс" in text))
async def handle_course(message: Message, state: FSMContext):
    lang = get_user_lang(message.from_user.id)

    text = info_text_kz if lang == "kz" else info_text_ru
    await message.answer(text, parse_mode="HTML")

    await message.answer(answer["ask_name"][lang], reply_markup=get_course_back_menu(lang))
    await state.set_state(InfoForm.name)

@router.message(F.text.func(lambda text: "Артқа" in text or "Назад" in text))
async def handle_back(message: Message, state: FSMContext):
    lang = get_user_lang(message.from_user.id)

    await state.clear()

    await message.answer(answer["greeting"][lang], reply_markup=get_main_menu(lang))

@router.message(InfoForm.name)
async def process_name_course(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    lang = get_user_lang(message.from_user.id)
    await message.answer(answer["ask_region"][lang])
    await state.set_state(InfoForm.region)

@router.message(InfoForm.region)
async def process_region_course(message: Message, state: FSMContext):
    lang = get_user_lang(message.from_user.id)
    
    if not re.fullmatch(r"[А-Яа-яӘәӨөҚқҰұҮүІіЁё\s\-]+", message.text):
        await message.answer("❗ Өтінеміз, облыс атауын тек әріптермен жазыңыз.")
        return

    await state.update_data(region=message.text)
    await message.answer(answer["ask_phone"][lang])
    await state.set_state(InfoForm.phone)

@router.message(InfoForm.phone)
async def process_phone_course(message: Message, state: FSMContext):
    lang = get_user_lang(message.from_user.id)
    phone = message.text.strip()

    # Валидатор казахстанского номера
    if not re.fullmatch(r"(\+7|8)\d{10}", phone):
        await message.answer("📵 Телефон нөмірі қате. Мысалы: +77001234567 немесе 87001234567")
        return

    await state.update_data(phone=phone)
    data = await state.get_data()

    # Вызов асинхронной функции создания сделки и контакта
    success, result = await create_amocrm_lead_and_contact(
        name=data.get("name"),
        phone=data.get("phone"),
        region=data.get("region")
    )

    if success:
        await message.answer(answer["thank_you"][lang], reply_markup=get_main_menu(lang))
    else:
        await message.answer("❗ Қате орын алды. Өтініш кейінірек қайталап көріңіз.")
        print(result)  # Для логов, можно сохранить в файл

    await state.clear()