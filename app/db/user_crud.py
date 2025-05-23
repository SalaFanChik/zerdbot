from sqlalchemy import select
from app.db.models import User
from sqlalchemy.ext.asyncio import AsyncSession

async def set_user_lang(session: AsyncSession, user_id: int, lang: str):
    user = await session.get(User, user_id)
    if user:
        user.lang = lang
    else:
        user = User(user_id=user_id, lang=lang)
        session.add(user)
    await session.commit()

async def get_user_lang(session: AsyncSession, user_id: int) -> str:
    user = await session.get(User, user_id)
    return user.lang if user else "ru"
