from telebot import TeleBot, types
from constants import api_token_bot, support_photo_url
from db_operations import (
    db_add_user,
    db_date_last_visit,
    db_all_id,
    db_update_loc,
    db_0_loc,
    db_0_city,
    db_read)
from action import (
    log,
    log_city_loc,
    start_menu,
    main_menu,
    action_menu_loc,
    action_menu_city,
    support_menu,
    error_city,
    check_on_0,
    main_menu_city_no_loc,
    main_menu_loc_no_city)
from weather_in_loc import (
    answer_now_w_loc,
    answer_today_f_loc,
    answer_tomorrow_f_loc,
    answer_in_2_days_f_loc,
    answer_in_3_days_f_loc,
    answer_in_4_days_f_loc,
    answer_in_5_days_f_loc)
from weather_in_city import (
    answer_now_w_city,
    answer_today_f_city,
    answer_tomorrow_f_city,
    answer_in_2_days_f_city,
    answer_in_3_days_f_city,
    answer_in_4_days_f_city,
    answer_in_5_days_f_city)
from lists import random_emoji, list_hi, list_yes
from geocoding import save_name_city_country_and_loc, save_name_loc_and_full

bot = TeleBot(api_token_bot)

print(bot.get_me())


@bot.message_handler(commands=['start'])
def handler_start(message: types.Message):
    try:
        if message.from_user.id in db_all_id():
            check_on_0(message)
        else:
            db_add_user(message)
            answer = "Добро пожаловать 🖐🏻"
            bot.send_message(message.from_user.id, answer)
            start_menu(message)
            log(message, answer)
    except Exception as e:
        print("Exception (find):", e)
        pass


@bot.message_handler(commands=['help'])
def handler_help(message: types.Message):
    try:
        answer = "- Отправить геопозицию можно так:\n👉🏻 📎 \n👉🏻 Геопозиция\n👉🏻 Отправить свою геопозицию\n\n" \
                 "- Введя название города 🏙️, бот может выдать не ваш город, " \
                 "так как есть города с одинаковым названием. " \
                 "Для получения точного результата можете воспользоваться:\nПогода по геопозиции 🌍\n\n" \
                 "- Обнаружили ошибки, или слова благодарности пишите сюда:\n@tyurikov87\n\n" \
                 "- Используются ресурсы:\nopenweathermap.org\nopenstreetmap.org\nЯндекс API Геокодер"
        bot.send_message(message.from_user.id, answer)
        log(message, answer)
    except Exception as e:
        print("Exception (find):", e)
        pass


@bot.message_handler(commands=['stop'])
def handler_stop(message: types.Message):
    try:
        answer = "До встречи! \nХотите вызвать меню нажмите /start"
        hide_markup = types.ReplyKeyboardRemove(True)
        bot.send_message(message.from_user.id, answer, reply_markup=hide_markup)
        log(message, answer)
    except Exception as e:
        print("Exception (find):", e)
        pass


@bot.message_handler(commands=['url'])
def url(message: types.Message):
    try:
        markup = types.InlineKeyboardMarkup()
        btn_my_site = types.InlineKeyboardButton(text='Жми давай', callback_data='sss')
        markup.add(btn_my_site)
        answer = "Нажми на кнопку получишь результат."
        bot.send_message(message.from_user.id, answer, reply_markup=markup)
        log(message, answer)
    except Exception as e:
        print("Exception (find):", e)
        pass


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    try:
        if call.data == 'sss':
            answer = "ха-ха-ха я пошутил 🙃"
            bot.send_message(call.from_user.id, answer)
            log(call.message, answer)
    except Exception as e:
        print("Exception (find):", e)
        pass


@bot.message_handler(content_types=['location'])
def handler_location(message: types.Message):
    try:
        db_update_loc(message)
        save_name_loc_and_full(message)
        action_menu_loc(message)
    except Exception as e:
        print("Exception (find):", e)
        pass


@bot.message_handler(
    func=lambda message: message.text == 'Сменить город 🏙️' or message.text == 'Погода по названию города 🌦🏙️')
def handler_message(message: types.Message):
    try:
        answer = "Введите название города 🏙️\nДля лучшего определения местоположение можете воспользоваться " \
                 "\nПогода по геопозиции 🌍"
        hide_markup = types.ReplyKeyboardRemove()
        msg = bot.send_message(message.from_user.id, answer, reply_markup=hide_markup)
        log(message, answer)
        bot.register_next_step_handler(msg, city_in_db)
    except Exception as e:
        print("Exception (find):", e)
        pass


def city_in_db(message):
    try:
        save_name_city_country_and_loc(message)
        action_menu_city(message)
    except Exception as e:
        print("Exception (find):", e)
        error_city(message)


@bot.message_handler(content_types=['text'])
@bot.edited_message_handler(content_types=['text'])
def handler_message(message: types.Message):
    try:
        db_date_last_visit(message)
        if message.text == 'Погода по геопозиции 🌦🌍':
            support_menu(message)
        elif message.text == f'Прогноз погоды 🌦 {db_read(message.from_user.id)[0]} 🌍':
            action_menu_loc(message)
        elif message.text == f'Прогноз погоды 🌦 {db_read(message.from_user.id)[4]} 🏙️':
            action_menu_city(message)
        elif message.text == 'Сменить геопозицию 🌍':
            answer = "Отправте новую геопозицию 🌍\n👉🏻 📎"
            bot.send_message(message.from_user.id, answer)
            log_city_loc(message, answer)
        elif message.text == 'Детали Вашей геопозиции 🌍':
            answer = f"Полная информация о выбранной геопозиции 🌍:\n{db_read(message.from_user.id)[1]}"
            bot.send_message(message.from_user.id, answer)
            log_city_loc(message, answer)
        elif message.text == "Нужна подсказка":
            answer = "Вот Вам инструкция:\nнажмите на скрепку\n👉🏻 📎 \n👉🏻 Геопозиция\n👉🏻 Отправить свою геопозицию"
            bot.send_chat_action(message.from_user.id, 'upload_photo')
            bot.send_photo(message.from_user.id, support_photo_url, answer)
            log(message, answer)
        elif message.text == 'Назад 👈🏻':
            if db_0_loc(message) == 0 and db_0_city(message) == '0':
                start_menu(message)
            elif db_0_loc(message) == 0:
                main_menu_city_no_loc(message)
            # else:
            #     start_menu(message)
        elif message.text == 'Вернуться назад 👈🏻':
            if db_0_city(message) == '0':
                main_menu_loc_no_city(message)
            else:
                main_menu(message)
        # Поменял первое 'е' и 'о' руское на английское для city (где  # замена)
        elif message.text == 'Вeрнуться назад 👈🏻':  # замена
            if db_0_loc(message) == 0:
                main_menu_city_no_loc(message)
            else:
                main_menu(message)
        elif message.text == 'Дeтальная погода сейчас 🌦':  # замена
            try:
                bot.send_message(message.from_user.id, answer_now_w_city(message.from_user.id))
                bot.send_chat_action(message.from_user.id, action='typing')
                log_city_loc(message, answer_now_w_city(message.from_user.id))
            except Exception as e:
                print("Exception (find):", e)
                error_city(message)
                main_menu(message)
        elif message.text == 'Прoгноз на сегодня':  # замена
            try:
                bot.send_message(message.from_user.id, answer_today_f_city(message.from_user.id))
                bot.send_chat_action(message.from_user.id, action='typing')
                log_city_loc(message, answer_today_f_city(message.from_user.id))
            except Exception as e:
                print("Exception (find):", e)
                error_city(message)
                main_menu(message)
        elif message.text == 'Прoгноз на завтра':  # замена
            try:
                bot.send_message(message.from_user.id, f'{db_read(message.from_user.id)[4]} 🏙️\n'
                                                       f'{answer_tomorrow_f_city(message.from_user.id)}')
                bot.send_chat_action(message.from_user.id, action='typing')
                log_city_loc(message, f'{db_read(message.from_user.id)[4]} 🏙️\n'
                                      f'{answer_tomorrow_f_city(message.from_user.id)}')
            except Exception as e:
                print("Exception (find):", e)
                error_city(message)
                main_menu(message)
        elif message.text == 'Прoгноз на 3️⃣ дня':  # замена
            try:
                answer = '{0}\n{1}\n{2}\n{3}'.format(
                    answer_today_f_city(message.from_user.id),
                    answer_tomorrow_f_city(message.from_user.id),
                    answer_in_2_days_f_city(message.from_user.id),
                    answer_in_3_days_f_city(message.from_user.id))
                bot.send_chat_action(message.from_user.id, action='typing')
                bot.send_message(message.from_user.id, answer)
                log_city_loc(message, answer)
            except Exception as e:
                print("Exception (find):", e)
                error_city(message)
                main_menu(message)
        elif message.text == 'Прoгноз на 5️⃣ дней':  # замена
            try:
                answer = '{0}\n{1}\n{2}\n{3}\n{4}\n{5}'.format(
                    answer_today_f_city(message.from_user.id),
                    answer_tomorrow_f_city(message.from_user.id),
                    answer_in_2_days_f_city(message.from_user.id),
                    answer_in_3_days_f_city(message.from_user.id),
                    answer_in_4_days_f_city(message.from_user.id),
                    answer_in_5_days_f_city(message.from_user.id))
                bot.send_message(message.from_user.id, answer)
                bot.send_chat_action(message.from_user.id, action='typing')
                log_city_loc(message, answer)
            except Exception as e:
                print("Exception (find):", e)
                error_city(message)
                main_menu(message)
        elif message.text == 'Детальная погода сейчас 🌦':
            bot.send_message(message.from_user.id, answer_now_w_loc(message.from_user.id))
            bot.send_chat_action(message.from_user.id, action='typing')
            log_city_loc(message, answer_now_w_loc(message.from_user.id))
        elif message.text == 'Прогноз на сегодня':
            bot.send_message(message.from_user.id, answer_today_f_loc(message.from_user.id))
            bot.send_chat_action(message.from_user.id, action='typing')
            log_city_loc(message, answer_today_f_loc(message.from_user.id))
        elif message.text == 'Прогноз на завтра':
            bot.send_message(message.from_user.id, f'Геопозиция 🌍\n{answer_tomorrow_f_loc(message.from_user.id)}')
            bot.send_chat_action(message.from_user.id, action='typing')
            log_city_loc(message, f'Геопозиция\n{answer_tomorrow_f_loc(message.from_user.id)}')
        elif message.text == 'Прогноз на 3️⃣ дня':
            answer = '{0}\n{1}\n{2}\n{3}'.format(
                answer_today_f_loc(message.from_user.id),
                answer_tomorrow_f_loc(message.from_user.id),
                answer_in_2_days_f_loc(message.from_user.id),
                answer_in_3_days_f_loc(message.from_user.id))
            bot.send_chat_action(message.from_user.id, action='typing')
            bot.send_message(message.from_user.id, answer)
            log_city_loc(message, answer)
        elif message.text == 'Прогноз на 5️⃣ дней':
            answer = '{0}\n{1}\n{2}\n{3}\n{4}\n{5}'.format(
                answer_today_f_loc(message.from_user.id),
                answer_tomorrow_f_loc(message.from_user.id),
                answer_in_2_days_f_loc(message.from_user.id),
                answer_in_3_days_f_loc(message.from_user.id),
                answer_in_4_days_f_loc(message.from_user.id),
                answer_in_5_days_f_loc(message.from_user.id))
            bot.send_message(message.from_user.id, answer)
            bot.send_chat_action(message.from_user.id, action='typing')
            log_city_loc(message, answer)

        elif message.text.lower() in list_hi:
            answer = "Приветствую Вас, хатите узнать погоду?"
            bot.send_message(message.from_user.id, answer)
            log(message, answer)
        elif message.text.lower() in list_yes:
            answer = "В этом деле я специалист, используйте встроенные команды, и я Вам предоставлю информацию"
            bot.send_message(message.from_user.id, answer)
            log(message, answer)
        else:
            answer = random_emoji()
            bot.send_message(message.from_user.id, answer)
            log(message, answer)
    except Exception as e:
        print("Exception (find): ", e)
        pass


@bot.message_handler(content_types=['sticker'])
def handler_sticker(message: types.Message):
    try:
        bot.send_sticker(message.from_user.id, message.sticker.file_id)
    except Exception as e:
        print("Exception (find):", e)
        pass


bot.polling(none_stop=True, interval=1)
