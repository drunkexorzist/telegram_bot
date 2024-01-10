import asyncio
import logging
import sys
import requests

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.markdown import hbold
from aiogram import F


TOKEN = 'tg_token'

# иницилизация диспачера
dp = Dispatcher()

# функция кнопок главного меню
def after_start_buttons():
    kb = [
    [
        types.KeyboardButton(text="Список пользователей"),
        types.KeyboardButton(text="Вернуться в главное меню")
    ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите действие"
    )

    return keyboard


# функция запуска по комманде /start. 
# 1. Проверяет есть ли юзер в БД и записывает если нет
# 2. Выводит кнопки главного меню
@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    # Отправляем данные пользователя и выводим сообщение с бэкенда

    try:
        # Отправка запроса на проверку юзера в БД
        check_user = (requests.get(f"http://127.0.0.1:8080/check_user/{message.from_user.id}")).json()

        if check_user == 0:
            try:
                # запись юзера в БД
                requests.post(f'http://127.0.0.1:8080/user_registration/{message.from_user.id}/{message.from_user.username}/{message.from_user.full_name}/{message.date}')
                await message.answer(f"{message.from_user.full_name}, вы успешно зарегистрированы!")
            except:
                await message.answer(f"Произошла ошибка в записи данных")
        else:
            await message.answer(f"Вы уже зарегистрированы")

        await message.answer("Что дальше?", reply_markup=after_start_buttons())
    except:
        await message.answer(f"Произошла ошибка, возпользуйтесь ботом позже")

# Дейсвие по кнопке список пользователей
@dp.message(F.text.lower() == "список пользователей")
async def users_list(message: types.Message):
    await message.reply("Вот список пользователей, выбери того с кем хочешь поиграть")


# Дейсвие по кнопке вернуться в главное меню
@dp.message(F.text.lower() == "вернуться в главное меню")
async def back_to_main_menu(message: types.Message):
    await message.reply("Возвращаемся")

# функция инициализации бота
async def main() -> None:
    global bot
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    # запуск бота
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())