from sqlalchemy import Column, BigInteger, String
from app.db.session import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(BigInteger, primary_key=True)
    lang = Column(String, nullable=False, default="ru")