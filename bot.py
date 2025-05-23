# bot.py
import asyncio
from aiogram import Dispatcher
from app.bot_instance import bot
from app.db.session import async_session_maker
from app.middlewares.db_middleware import DbSessionMiddleware
from app.handlers import user, courses, zerdeli_app

dp = Dispatcher()

dp.update.middleware(DbSessionMiddleware(async_session_maker))
dp.include_router(user.router)
dp.include_router(courses.router)
dp.include_router(zerdeli_app.router)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
