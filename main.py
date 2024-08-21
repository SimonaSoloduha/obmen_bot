import os
import logging
import sys

from dotenv import load_dotenv

from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram import Bot, Dispatcher, executor
from aiogram.dispatcher import FSMContext
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from messages import (EXCHANGE)

from middleware import get_text, get_text_real, get_images_path

activate_this = '/home/a0951410/domains/a0951410.xsph.ru/obmen_bot/obmen_bot/venv/bin/activate_this.py'
with open(activate_this) as f:
    exec(f.read(), {'__file__': activate_this})

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")

bot = Bot(token=API_TOKEN, parse_mode='HTML')

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


def get_start_keyboard() -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text=EXCHANGE)],
    ]
    start_keyboard = ReplyKeyboardMarkup(keyboard=kb,
                                         resize_keyboard=True,
                                         input_field_placeholder="Выберите гороскоп")
    return start_keyboard


# Старт
@dp.message_handler(commands="start")
async def bot_start(msg: Message):
    await msg.answer("Генерация курса на связи",
                     reply_markup=get_start_keyboard())


# Указание курса
@dp.message_handler(text=EXCHANGE)
async def get_exc_rub_buy(msg: Message, state: FSMContext):
    selection = msg.text
    await state.update_data(selection=selection)

    await msg.answer(f'По чем рубли?{selection}')


# Генерация и сохранение изображений
@dp.message_handler()
async def message_handler(msg: Message, state: FSMContext):
    rub_buy, rub_sell, uah_buy, uah_sell, usd_bay, usd_sell = msg.text.split(",")
    await state.update_data(rub_buy=float(rub_buy), rub_sell=float(rub_sell),
                            uah_buy=float(uah_buy), uah_sell=float(uah_sell),
                            usd_bay=float(usd_bay), usd_sell=float(usd_sell))

    user_data = await state.get_data()
    rub_buy = user_data.get('rub_buy')
    rub_sell = user_data.get('rub_sell')
    uah_buy = user_data.get('uah_buy')
    uah_sell = user_data.get('uah_sell')
    usd_bay = user_data.get('usd_bay')
    usd_sell = user_data.get('usd_sell')

    if rub_buy and rub_sell and uah_buy and uah_sell and usd_bay and usd_sell:
        text_msg = get_text(rub_buy, rub_sell, uah_buy, uah_sell, usd_bay, usd_sell)
        await msg.answer(text_msg)
        text_real = get_text_real(rub_buy, rub_sell, uah_buy, uah_sell)
        await msg.answer(text_real)

        images_path = get_images_path()

        with open(images_path[0], 'rb') as photo:
            await msg.answer_photo(photo)
        with open(images_path[1], 'rb') as photo:
            await msg.answer_photo(photo)
        for foto in images_path:
            os.remove(foto)
        await state.finish()
    else:
        await msg.answer(f"Еще раз",
                         reply_markup=get_start_keyboard())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
