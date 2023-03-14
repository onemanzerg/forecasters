from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from database import last_tour_buttons

main_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
bet_button = KeyboardButton(text="Сделать ставки")
results_button = KeyboardButton(text="Результаты")
match_list_button = KeyboardButton(text="Предстоящие матчи")
main_kb.add(bet_button, results_button, match_list_button)


def last_tour_keyboard(username) -> InlineKeyboardMarkup:
    buttons = [
        types.InlineKeyboardButton(text=f"{match[1]} | {match[5]}", callback_data=f"{match[1]} | {match[5]}") for match in
        last_tour_buttons(username)
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)

    return keyboard

# можно в callback_data засунуть айдишник
# match[1] - вывеска
# match[5] - номер тура
