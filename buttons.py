from scraping import update_info
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
import json

with open('result.json', 'r', encoding='utf-8') as file:
    json_data = file.read()
data = json.loads(json_data)


async def inline_buttons():
    keyboard = InlineKeyboardBuilder()
    for event_name, event_data in data.items():
        keyboard.add(InlineKeyboardButton(text=event_name, callback_data=event_name))
    return keyboard.adjust(1).as_markup()
