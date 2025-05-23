from aiogram import Router, F
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from app.utils.texts import answer  
from app.db.user_crud import set_user_lang
from app.keyboards.reply import get_main_menu, lang_kb
from app.states.lang_state import Form
from aiogram.types import BotCommand
from aiogram.types.bot_command_scope_chat import BotCommandScopeChat
from app.bot_instance import bot  


router = Router()


@router.message(Command("start"))
async def start_handler(message: Message, state: FSMContext):
    """ Handler for /start command """
    await message.answer("Сәлеметсіз бе?! Сізге қай тілде жауап алған ыңғайлы?\n\n Здравствуйте! На каком языке вам удобно получить ответ?", reply_markup=lang_kb)
    
    await state.set_state(Form.choose_language) 
    


@router.message(Form.choose_language, F.text.in_(["Қазақша", "Русский"]))
async def set_language(message: Message, state: FSMContext, session: AsyncSession):
    lang = "kz" if message.text == "Қазақша" else "ru"
    await set_user_lang(session, message.from_user.id, lang)  

    if lang == "kz":
        commands = [
            BotCommand(command="start", description="♻️ Ботты қайта іске қосу"),
            BotCommand(command="support", description="☎️ Қолдау"),
            BotCommand(command="faq", description="ℹ️ Жиі қойылатын сұрақтар"),
            BotCommand(command="lang", description="🌐 Тілді өзгерту"),
            BotCommand(command="log", description="🖨 Логтарды алу"),
        ]
    else:
        commands = [
            BotCommand(command="start", description="♻️ Перезапустить бота"),
            BotCommand(command="support", description="☎️ Поддержка"),
            BotCommand(command="faq", description="ℹ️ FAQ"),
            BotCommand(command="lang", description="🌐 Сменить язык"),
            BotCommand(command="log", description="🖨 Получить логи"),
        ]

    await bot.set_my_commands(
        commands,
        scope=BotCommandScopeChat(chat_id=message.from_user.id)
    )
    await message.answer(answer["greeting"][lang], reply_markup=get_main_menu(lang))
    await state.clear()