from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from contextlib import asynccontextmanager

Base = declarative_base()


class User(Base):
    __tablename__ = 'medtrack_admin_user'
    id = Column(Integer, primary_key=True)
    full_name = Column(String(255), nullable=False)
    username = Column(String(255))
    telegram_id = Column(Integer, unique=True, nullable=False)
    registered_time = Column(DateTime, default=datetime.utcnow)


class Database:
    def __init__(self, database_url):
        self.engine = create_async_engine(database_url, echo=True)

    async def async_session(self):
        async with self.engine.begin() as conn:
            async_session = sessionmaker(
                bind=conn, class_=AsyncSession, expire_on_commit=False
            )
            async with async_session() as session:
                yield session

    async def create_tables(self):
        async with self.async_session() as session:
            async with session.begin():
                Base.metadata.create_all(session.get_bind())

    async def add_user(self, full_name, username, telegram_id):
        async with self.async_session() as session:
            new_user = User(
                full_name=full_name, username=username, telegram_id=telegram_id
            )
            session.add(new_user)
            await session.commit()
            return new_user

    @asynccontextmanager
    async def select_all_users(self):
        async with self.async_session() as session:
            tg_users = await session.execute(select(User))
            users = [user async for user in tg_users.scalars()]
            return users

    async def check_user(self, telegram_id):
        async with self.async_session() as session:
            sql = select(User).where(User.telegram_id == telegram_id)
            result = await session.execute(sql)
            return result.scalars().first() is not None
