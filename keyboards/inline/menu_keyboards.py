from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

menu_keys = InlineKeyboardMarkup(row_width=2)
menu_keys.insert(InlineKeyboardButton("Get my prescriptions", callback_data="prescription"))
menu_keys.insert(InlineKeyboardButton("When is my next pill?", callback_data="next_pill"))
menu_keys.insert(InlineKeyboardButton("Book an appointment", callback_data="appointment"))
menu_keys.insert(InlineKeyboardButton("Get result of my analysis", callback_data="analysis"))
