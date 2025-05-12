from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

contact_support_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Написать в поддержку", url="https://t.me/support_bot")]
    ]
)

product_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Товар 1", callback_data="product_1"),
            InlineKeyboardButton(text="Товар 2", callback_data="product_2")
        ],
        [InlineKeyboardButton(text="Назад", callback_data="go_back")]
    ]
)