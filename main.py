import asyncio
from aiogram import Bot, Dispatcher, executor, types
from os import getenv
from sys import exit
from aiogram.dispatcher.filters import Text
from keyboards import main_kb, last_tour_keyboard
from database import create_player_table, update_player_table, insert_player_table, all_players_tables, \
    last_tour_buttons
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from functions import check_valid_score

bot_token = getenv("BOT_TOKEN")
if not bot_token:
    exit("Error: no token provided")

storage = MemoryStorage()
bot = Bot(token=bot_token)
dp = Dispatcher(bot=bot, storage=storage)


class BetForecast(StatesGroup):
    waiting_for_forecast = State()


# async def start_bot(bot: Bot):
#     await bot.send_message(267850523, text="Бот запущен!")


@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message) -> None:
    create_player_table(message.from_user.username)
    insert_player_table(message.from_user.username)
    await message.answer(f'Добро пожаловать в битву прогнозистов!', reply_markup=main_kb)

@dp.message_handler(commands=['cancel'], state='*')
async def cmd_cancel(message: types.Message, state: FSMContext):
    if state is None:
        return
    await state.finish()
    await message.answer('Вы прервали свой прогноз.', reply_markup=main_kb)


@dp.message_handler(Text(equals="Сделать ставки"), state="*")
async def betting_cmd(message: types.Message) -> None:
    keyboard = last_tour_keyboard(message.from_user.username)
    await message.answer("Это предстоящие матчи. Выбери матч для ставки.", reply_markup=keyboard)


# @dp.callback_query_handler(text='—')
# async def do_betting(callback: types.CallbackQuery) -> None:
#     await callback.answer("Ставка сделана!", show_alert=True)
#     # Пользователь жмет на кнопку, по этой кнопке в столбце title ищется матч и в столбце forecast вставляется то, что воодит юзер
#     # Подрубаем машину состояний и ждем когда пользователь впишет релевантный прогноз, затем обновляем инлайн клавиатуру, чтобы этот матч пропал
#     # await callback.answer("Готово!", show_alert=True)


@dp.callback_query_handler(lambda callback_query: True, state="*")
async def process_callback(callback: types.CallbackQuery, state: FSMContext):
    match = callback.data.split("|")[0].strip()
    tour = callback.data.split("|")[1].strip()
    print(match)
    print(tour)
    await callback.message.answer(f"Вы выбрали матч {match[0]}. Тур {match[1]} Напиши в чат прогноз на игру в формате 0:0")
    # должен сохранить в мемори данные название матча и тура
    async with state.proxy() as data:
        data['match'] = match
    print(match)
    # await callback.message.answer(data['match'], data['tour'])
    await BetForecast.waiting_for_forecast.set()
    # await state.update_data(chosen_match=callback.data)
    # await callback.message.answer(state.get_data())


@dp.message_handler(state=BetForecast.waiting_for_forecast)
async def bet_forecast(message: types.Message, state: FSMContext) -> None:
    if not check_valid_score(message.text):
        await message.answer("Не правильно. Попробуй ещё раз написать матч в формате 0:0.")
        return
    await state.finish()
    keyboard = last_tour_keyboard(message.from_user.username)
    await message.answer("Прогноз принят", reply_markup=keyboard)


async def update_tables_every_hour():
    while True:
        for table in all_players_tables():
            update_player_table(table_name=table[0])
            await asyncio.sleep(600)


if __name__ == '__main__':
    # dp.startup.register(start_bot)
    loop = asyncio.get_event_loop()
    loop.create_task(update_tables_every_hour())
    executor.start_polling(dp, skip_updates=True)
