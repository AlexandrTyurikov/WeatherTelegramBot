import pyowm

from db_operations import db_read
from datetime import datetime, timedelta
from constants import api_key_pyowm
from lists import week_day


def answer_now_w_loc(user_id):
    owm = pyowm.OWM(api_key_pyowm, language='ru')
    obs = owm.weather_at_coords(db_read(user_id)[2], db_read(user_id)[3])
    w = obs.get_weather()
    d = w.get_pressure()['press']  # Атмосферное давление гПА
    drs = round(d / 1.333224)  # Атмосферное давление мм.рт.ст
    time_r_obs = w.get_sunrise_time('date')
    time_r = time_r_obs + timedelta(hours=3)
    time_s_obs = w.get_sunset_time('date')
    time_s = time_s_obs + timedelta(hours=3)
    light_day = time_s - time_r
    answer = "{0} 🌍\nСейчас {1} {2}, {3}\nВлажность: {4} %\nСкорость ветра: {5} м/с\nДавление: {6} мм.рт.ст\n" \
             "Время восхода: {7} (GMT+3)\nВремя заката: {8} (GMT+3)\nСветовой день: {9}" \
        .format(
            db_read(user_id)[0],
            round(w.get_temperature('celsius')['temp']),
            u'\u2103',
            w.get_detailed_status(),
            w.get_humidity(),
            w.get_wind()['speed'],
            drs,
            time_r.strftime('%H:%M'),
            time_s.strftime('%H:%M'),
            light_day)
    return answer


def answer_today_f_loc(user_id):
    owm = pyowm.OWM(api_key_pyowm, language='ru')
    fc = owm.three_hours_forecast_at_coords(db_read(user_id)[2], db_read(user_id)[3])
    f = fc.get_forecast()
    answer = '{0} 🌍\n{1}, {2}\n'.format(
        db_read(user_id)[0],
        week_day[datetime.now().weekday()],
        datetime.now().strftime('%d.%m.%Y'))
    for weather in f:
        time_obs = weather.get_reference_time('date')
        time_minsk = time_obs + timedelta(hours=3)
        if time_minsk.day == datetime.now().day:
            answer_str = "{0}   {1} {2}, {3}".format(
                time_minsk.strftime('%H:%M'),
                round(weather.get_temperature('celsius')['temp']),
                u'\u2103',
                weather.get_detailed_status())
            answer += answer_str + '\n'
    return answer


def answer_tomorrow_f_loc(user_id):
    owm = pyowm.OWM(api_key_pyowm, language='ru')
    fc = owm.three_hours_forecast_at_coords(db_read(user_id)[2], db_read(user_id)[3])
    f = fc.get_forecast()
    date_tomorrow = datetime.now() + timedelta(days=1)
    answer = '{0}, {1}\n'.format(week_day[date_tomorrow.weekday()], date_tomorrow.strftime('%d.%m.%Y'))
    for weather in f:
        time_obs = weather.get_reference_time('date')
        time_minsk = time_obs + timedelta(hours=3)
        if time_minsk.day == date_tomorrow.day:
            answer_str = "{0}   {1} {2}, {3}".format(
                time_minsk.strftime('%H:%M'),
                round(weather.get_temperature('celsius')['temp']),
                u'\u2103',
                weather.get_detailed_status())
            answer += answer_str + '\n'
    return answer


def answer_in_2_days_f_loc(user_id):
    owm = pyowm.OWM(api_key_pyowm, language='ru')
    fc = owm.three_hours_forecast_at_coords(db_read(user_id)[2], db_read(user_id)[3])
    f = fc.get_forecast()
    date_in_2_days = datetime.now() + timedelta(days=2)
    answer = '{0}, {1}\n'.format(week_day[date_in_2_days.weekday()], date_in_2_days.strftime('%d.%m.%Y'))
    for weather in f:
        time_obs = weather.get_reference_time('date')
        time_minsk = time_obs + timedelta(hours=3)
        if time_minsk.day == date_in_2_days.day:
            answer_str = "{0}   {1} {2}, {3}".format(
                time_minsk.strftime('%H:%M'),
                round(weather.get_temperature('celsius')['temp']),
                u'\u2103',
                weather.get_detailed_status())
            answer += answer_str + '\n'
    return answer


def answer_in_3_days_f_loc(user_id):
    owm = pyowm.OWM(api_key_pyowm, language='ru')
    fc = owm.three_hours_forecast_at_coords(db_read(user_id)[2], db_read(user_id)[3])
    f = fc.get_forecast()
    date_in_3_days = datetime.now() + timedelta(days=3)
    answer = '{0}, {1}\n'.format(week_day[date_in_3_days.weekday()], date_in_3_days.strftime('%d.%m.%Y'))
    for weather in f:
        time_obs = weather.get_reference_time('date')
        time_minsk = time_obs + timedelta(hours=3)
        if time_minsk.day == date_in_3_days.day:
            answer_str = "{0}   {1} {2}, {3}".format(
                time_minsk.strftime('%H:%M'),
                round(weather.get_temperature('celsius')['temp']),
                u'\u2103',
                weather.get_detailed_status())
            answer += answer_str + '\n'
    return answer


def answer_in_4_days_f_loc(user_id):
    owm = pyowm.OWM(api_key_pyowm, language='ru')
    fc = owm.three_hours_forecast_at_coords(db_read(user_id)[2], db_read(user_id)[3])
    f = fc.get_forecast()
    date_in_4_days = datetime.now() + timedelta(days=4)
    answer = '{0}, {1}\n'.format(week_day[date_in_4_days.weekday()], date_in_4_days.strftime('%d.%m.%Y'))
    for weather in f:
        time_obs = weather.get_reference_time('date')
        time_minsk = time_obs + timedelta(hours=3)
        if time_minsk.day == date_in_4_days.day:
            answer_str = "{0}   {1} {2}, {3}".format(
                time_minsk.strftime('%H:%M'),
                round(weather.get_temperature('celsius')['temp']),
                u'\u2103',
                weather.get_detailed_status())
            answer += answer_str + '\n'
    return answer


def answer_in_5_days_f_loc(user_id):
    owm = pyowm.OWM(api_key_pyowm, language='ru')
    fc = owm.three_hours_forecast_at_coords(db_read(user_id)[2], db_read(user_id)[3])
    f = fc.get_forecast()
    date_in_5_days = datetime.now() + timedelta(days=5)
    answer = '{0}, {1}\n'.format(week_day[date_in_5_days.weekday()], date_in_5_days.strftime('%d.%m.%Y'))
    for weather in f:
        time_obs = weather.get_reference_time('date')
        time_minsk = time_obs + timedelta(hours=3)
        if time_minsk.day == date_in_5_days.day:
            answer_str = "{0}   {1} {2}, {3}".format(
                time_minsk.strftime('%H:%M'),
                round(weather.get_temperature('celsius')['temp']),
                u'\u2103',
                weather.get_detailed_status())
            answer += answer_str + '\n'
    return answer
