from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from loader import dp, bot
from utils.db_commands import get_user_by_id, add_user

CHANNEL_CHAT_ID = "@multileveltest"


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    user = await get_user_by_id(message.from_user.id)
    if user is None:
        await add_user(message.from_user.username, message.from_user.first_name, message.from_user.id)
    try:
        member = await bot.get_chat_member(CHANNEL_CHAT_ID, user_id=message.from_user.id)
        if member.status == "member" or member.status == "administrator" or member.status == "creator":
            await message.answer("Hello! You are a member of the channel.")
        else:
            await message.answer("You must be a member of the channel to use this bot.")
    except Exception as e:
        await message.answer("An error occurred while checking your channel membership.")
