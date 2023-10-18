from aiogram import executor

from loader import dp, engine

from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands

from utils.db_commands import Base

import handlers
import loader


async def on_startup(dispatcher):
    Base.metadata.create_all(engine)
    
    await set_default_commands(dispatcher)
    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
