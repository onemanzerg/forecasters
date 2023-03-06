from aiogram import Bot, Dispatcher, executor, types
from os import getenv
from sys import exit
from aiogram.dispatcher.filters import Text
from scheduled import parse_scheduled
from keyboards import main_kb
from database import create_player_table

bot_token = getenv("BOT_TOKEN")
if not bot_token:
    exit("Error: no token provided")

bot = Bot(token=bot_token)
dp = Dispatcher(bot=bot)


@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message) -> None:
    create_player_table(message.from_user.username)
    await message.answer(f'Добро пожаловать в битву прогнозистов! Выберите футбольную лигу!', reply_markup=main_kb)
    print(type(message.from_user.username))


@dp.message_handler(Text(equals="Сделать ставки"))
async def betting_cmd(message: types.Message) -> None:
    buttons = [
        types.InlineKeyboardButton(text=f"{match[0]}", callback_data=f"{match[1]}") for match in
        parse_scheduled()
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    await message.answer("Это предстоящие матчи.", reply_markup=keyboard)


@dp.callback_query_handler(text='—')
async def do_betting(callback: types.CallbackQuery) -> None:
    await callback.answer("Давай прогноз в чат пиши")
    # Подрубаем машину состояний и ждем когда пользователь впишет релевантный прогноз, затем обновляем инлайн клавиатуру, чтобы этот матч пропал
    await callback.answer("Готово!", show_alert=True)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
