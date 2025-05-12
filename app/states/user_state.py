from aiogram.fsm.state import State, StatesGroup

class InfoForm(StatesGroup):
    name = State()
    region = State()
    phone = State()
