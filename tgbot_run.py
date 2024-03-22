from aiogram import Bot, Dispatcher, Router, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.filters.command import Command
from aiogram.types import Message, CallbackQuery
from aiogram.utils.markdown import hbold
from aiogram.client.bot import DefaultBotProperties
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import TOKEN
import asyncio
import logging
import sys
from scraping import update_info
import json

with open('result.json', 'r', encoding='utf-8') as file:
    json_data = json.load(file)

dp = Dispatcher()
router = Router()


async def inline_buttons():
    keyboard = InlineKeyboardBuilder()
    for event_name in json_data:
        keyboard.add(InlineKeyboardButton(text=event_name, callback_data=f'info_{json_data[event_name]["id"]}'))
    return keyboard.adjust(2).as_markup()


@dp.message(Command('dd', prefix='/dd'))
async def download_data(message: Message):
    await message.answer(
        f"{hbold(message.from_user.full_name)}, зачекайте ⏳"
    )
    update_info()
    await message.answer("Виберіть виставу", reply_markup=await inline_buttons())


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        f"Привіт! {hbold(message.from_user.full_name)}, це бот для моніторингу активних білетів на вистави театру імені І. Франка."
    )
    await message.answer(
        'Команди: \n /dd - для завантаження/оновлення даних \n /show - для повторного виведення вистав')


@dp.message(Command('show', prefix='/show'))
async def show(message: Message):
    await message.answer("Виберіть виставу", reply_markup=await inline_buttons())


@dp.callback_query(F.data.startswith("info"))
async def info(callback: CallbackQuery):
    id = int(callback.data.split("_")[-1])
    for key, item in json_data.items():
        if id == item['id']:
            date = item.get("date")
            free_places = item.get("free_places")
            count_free_places = item.get("count_free_places")
            link = item.get("link")
            response = f'<b>Вистава:</b> {key}\n'
            for index in range(len(date)):
                response += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                response += f"<b>Дата:</b> {date[index]}\n"
                response += f"<b>Вільні білети:</b> {free_places[index]}\n"
                response += f"<b>Кількість вільних білетів:</b> {count_free_places[index]}\n"
                response += f"<b>Посилання:</b> <a href='{link[index]}'>{link[index]}</a>\n\n"
            await callback.message.answer(response, parse_mode=ParseMode.HTML)
            await callback.answer(f"Ви вибрали {key}")
            break


async def main():
    bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("exit")
