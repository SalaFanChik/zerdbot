from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from app.utils.texts import answer


def get_main_menu(lang: str) -> ReplyKeyboardMarkup:
    """ Returns the main menu keyboard based on the selected language """
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=answer["course"][lang])],
            [KeyboardButton(text=answer["challenges"][lang])],
            [KeyboardButton(text=answer["support"][lang])],
            [KeyboardButton(text=answer["started_education"][lang])]
        ],
        resize_keyboard=True,
        input_field_placeholder="Выберите действие"
    )

lang_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Қазақша")],
        [KeyboardButton(text="Русский")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите действие"
)


def get_altynasyq_menu(lang: str):
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=answer["more_info"][lang])],
            [KeyboardButton(text=answer["back"][lang])]
        ],
        resize_keyboard=True
    )

def get_course_back_menu(lang: str):
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=answer["back"][lang])]
        ],
        resize_keyboard=True
    )



def get_support_menu(lang: str):
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=answer["btn_how_to_register"][lang])],
            [KeyboardButton(text=answer["btn_how_to_view_certificate"][lang])],
            [KeyboardButton(text=answer["back"][lang])]
        ],
        resize_keyboard=True
    )

