from contextlib import asynccontextmanager

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from data import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# loading database
DATABASE_URL = 'postgresql://postgres:khamid007@localhost:5432/tg_users'

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


@asynccontextmanager
async def db_session():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
