from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import ParseMode
from keyboards.inline.menu_keyboards import menu_keys
from loader import dp, db, bot
import datetime
from data.config import ADMINS


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.full_name
    user_address = message.from_user.username
    registered_datetime = datetime.datetime.now()
    if not await db.check_user(user_id):
        await db.add_user(user_name, user_address, user_id, registered_datetime)
        await bot.send_message(chat_id=ADMINS[0], text=f'New Telegram_Users: {user_name} has been added to the database at {registered_datetime}')
    else:
        pass
    await message.answer("Assalomu alaykum, <b>{x}</b>\n\nI am your virtual assitant,"
                         "\nPlease choose what you want to do next".format(x=user_name), parse_mode=ParseMode.HTML,
                         reply_markup=menu_keys)
