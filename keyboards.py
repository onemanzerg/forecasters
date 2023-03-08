from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

main_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
bet_button = KeyboardButton(text="Сделать ставки")
results_button = KeyboardButton(text="Результаты")
match_list_button = KeyboardButton(text="Предстоящие матчи")
main_kb.add(bet_button, results_button, match_list_button)

# def actual_tour_keyboard():
