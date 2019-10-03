from telebot import TeleBot, types
from datetime import datetime
from constants import api_token_bot
from db_operations import db_read, db_0_loc, db_0_city

bot = TeleBot(api_token_bot)

answer_action = "Выберите действие 👇🏻"


def log(message, answer):
    print("\n--------------------")
    print(datetime.now())
    print("Сообщение от {0} {1} \nusername: {2}  (id = {3}) \nТекст: {4}".format(
        message.from_user.first_name,
        message.from_user.last_name,
        message.from_user.username,
        str(message.from_user.id),
        message.text,))
    print("Ответ:", answer)


def log_city_loc(message, answer):
    print("\n--------------------")
    print(datetime.now())
    print("Сообщение от {0} {1}\nusername: {2}  (id = {3})\nГеопозиция: {4}, {5}\nГород: {6}\nТекст: {7}".format(
        message.from_user.first_name,
        message.from_user.last_name,
        message.from_user.username,
        str(message.from_user.id),
        db_read(message.from_user.id)[2],
        db_read(message.from_user.id)[3],
        db_read(message.from_user.id)[4],
        message.text,))
    print("Ответ:", answer)


def check_on_0(message):
    if db_0_city(message) == '0' and db_0_loc(message) == 0:
        start_menu(message)
    elif db_0_city(message) == '0':
        main_menu_loc_no_city(message)
    elif db_0_loc(message) == 0:
        main_menu_city_no_loc(message)
    else:
        main_menu(message)


def error_city(message):
    answer = "По вашему запросу ничего не нашлось. Также можете воспользоваться\nПогода по геопозиции 🌍"
    bot.send_message(message.from_user.id, answer)
    check_on_0(message)
    log_city_loc(message, answer)


def start_menu(message):
    user_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    user_markup.row('Погода по названию города 🌦🏙️')
    user_markup.row('Погода по геопозиции 🌦🌍')
    bot.send_message(message.from_user.id, answer_action, reply_markup=user_markup)
    log(message, answer_action)


def main_menu(message):
    user_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    user_markup.row(f'Прогноз погоды 🌦 {db_read(message.from_user.id)[4]} 🏙️')
    user_markup.row(f'Прогноз погоды 🌦 {db_read(message.from_user.id)[0]} 🌍')
    user_markup.row('Детали Вашей геопозиции 🌍')
    bot.send_message(message.from_user.id, answer_action, reply_markup=user_markup)
    log_city_loc(message, answer_action)


def main_menu_loc_no_city(message):
    user_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    user_markup.row('Погода по названию города 🌦🏙️')
    user_markup.row(f'Прогноз погоды 🌦 {db_read(message.from_user.id)[0]} 🌍')
    user_markup.row('Детали Вашей геопозиции 🌍')
    bot.send_message(message.from_user.id, answer_action, reply_markup=user_markup)
    log_city_loc(message, answer_action)


def action_menu_loc(message):
    user_markup3 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    user_markup3.row('Детальная погода сейчас 🌦')
    user_markup3.row('Прогноз на сегодня', 'Прогноз на завтра')
    user_markup3.row('Прогноз на 3️⃣ дня', 'Прогноз на 5️⃣ дней')
    user_markup3.row('Сменить геопозицию 🌍', 'Вернуться назад 👈🏻')
    bot.send_message(message.from_user.id, answer_action, reply_markup=user_markup3)
    log_city_loc(message, answer_action)


def main_menu_city_no_loc(message):
    user_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    user_markup.row(f'Прогноз погоды 🌦 {db_read(message.from_user.id)[4]} 🏙️')
    user_markup.row('Погода по геопозиции 🌦🌍')
    bot.send_message(message.from_user.id, answer_action, reply_markup=user_markup)
    log_city_loc(message, answer_action)


# Поменял первое 'е' и 'о' руское на английское
def action_menu_city(message):
    user_markup3 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    user_markup3.row('Дeтальная погода сейчас 🌦')  # замена
    user_markup3.row('Прoгноз на сегодня', 'Прoгноз на завтра')  # замена
    user_markup3.row('Прoгноз на 3️⃣ дня', 'Прoгноз на 5️⃣ дней')  # замена
    user_markup3.row('Сменить город 🏙️', 'Вeрнуться назад 👈🏻')  # замена
    bot.send_message(message.from_user.id, answer_action, reply_markup=user_markup3)
    log_city_loc(message, answer_action)


def support_menu(message):
    user_markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    user_markup2.row('Нужна подсказка')
    user_markup2.row('Назад 👈🏻')
    answer = "Отправте мне Вашу геопозицию 🌍"
    bot.send_message(message.from_user.id, answer, reply_markup=user_markup2)
    log(message, answer)
