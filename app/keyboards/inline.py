from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

local_text = {
    "yearly": {
        "kz": "Жылдық курс",
        "ru": "Годовой курс"
    }
}

def get_courses_kb(lang: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Get Ready", callback_data="course_get_ready")],
        [InlineKeyboardButton(text=local_text["yearly"].get(lang, "Годовой курс"), callback_data="course_yearly")],
        [InlineKeyboardButton(text="Гибрид", callback_data="course_hybrid")]
    ])
    return kb


def get_course_options_kb(course: str, lang: str) -> InlineKeyboardMarkup:
    texts = {
        "ru": {
            "register": "Хочу записаться",
            "faq": "Часто задаваемые вопросы",
            "reviews": "Отзывы",
            "back": "Назад",
            "home": "На главную"
        },
        "kz": {
            "register": "Тіркелгім келеді",
            "faq": "Жиі қойылатын сұрақтар",
            "reviews": "Пікірлер",
            "back": "Артқа",
            "home": "Басты бетке"
        }
    }
    t = texts.get(lang, texts["ru"])

    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t["register"], callback_data=f"{course}_register")],
        [InlineKeyboardButton(text=t["faq"], callback_data=f"{course}_faq")],
        [InlineKeyboardButton(text=t["reviews"], callback_data=f"{course}_reviews")],
        [
            InlineKeyboardButton(text=t["back"], callback_data="back_to_courses"),
            InlineKeyboardButton(text=t["home"], callback_data="go_home")
        ]
    ])
