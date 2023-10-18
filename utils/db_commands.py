from pytz import timezone
from sqlalchemy import Column, Integer, String, DateTime, func, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from loader import db_session
from sqlalchemy import select
Base = declarative_base()

uz_timezone = timezone('Asia/Tashkent')


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    name = Column(String)
    tg_id = Column(String)
    joined_time = Column(DateTime, server_default=func.now(tz=uz_timezone))


async def get_user_by_id(user_id):
    async with db_session() as session:
        stmt = select(User).where(User.tg_id == user_id)
        result = await session.execute(stmt)
        user = result.scalar()
    return user


async def add_user(username, name, tg_id):
    user = User(username=username, name=name, tg_id=tg_id)
    async with db_session() as session:
        session.add(user)
        session.commit()
