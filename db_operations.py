import sqlite3
from datetime import datetime


def db_add_user(message):
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()

    cursor.execute(
        f"""INSERT INTO location (id, date_create_user, date_last_visit, name_loc, name_loc_full,
                                  latitude, longitude, city, lat_city, lon_city, username, first_name, last_name)
        VALUES (
                '{message.from_user.id}',
                '{datetime.now().strftime('%d.%m.%Y_%H:%M')}',
                '{datetime.now().strftime('%d.%m.%Y_%H:%M')}',
                '0',
                '0',
                '0',
                '0',
                '0',
                '0',
                '0',
                '{message.from_user.username}',
                '{message.from_user.first_name}',
                '{message.from_user.last_name}'
                )""")
    conn.commit()

    cursor.close()
    conn.close()


def db_date_last_visit(message):
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()

    cursor.execute(f"""SELECT * FROM location WHERE id={message.from_user.id}""")
    old = cursor.fetchone()
    cursor.execute(f"""
        UPDATE location SET date_last_visit = '{datetime.now().strftime('%d.%m.%Y_%H:%M')}'
        WHERE date_last_visit = '{old[2]}'""")
    conn.commit()

    cursor.close()
    conn.close()


def db_all_id():
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()

    cursor.execute("""SELECT id FROM location""")
    rez = cursor.fetchall()
    all_id = []
    for id_user in rez:
        all_id.append(id_user[0])

    cursor.close()
    conn.close()
    return all_id


def db_0_loc(message):
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()

    cursor.execute(f"""SELECT latitude FROM location WHERE id={message.from_user.id}""")
    lat = cursor.fetchone()

    cursor.close()
    conn.close()
    return lat[0]


def db_0_city(message):
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()

    cursor.execute(f"""SELECT city FROM location WHERE id={message.from_user.id}""")
    city = cursor.fetchone()

    cursor.close()
    conn.close()
    return city[0]


def db_update_name_loc(message, name):
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()

    cursor.execute(f"""SELECT * FROM location WHERE id = {message.from_user.id}""")
    old = cursor.fetchone()
    cursor.execute(f"""UPDATE location SET name_loc = '{name}' WHERE name_loc = '{old[3]}'""")
    conn.commit()

    cursor.close()
    conn.close()


def db_update_name_loc_full(message, name):
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()

    cursor.execute(f"""SELECT * FROM location WHERE id={message.from_user.id}""")
    old = cursor.fetchone()
    cursor.execute(f"""UPDATE location SET name_loc_full = '{name}' WHERE name_loc_full = '{old[4]}'""")
    conn.commit()

    cursor.close()
    conn.close()


def db_update_loc(message):
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()

    cursor.execute(f"""SELECT * FROM location WHERE id={message.from_user.id}""")
    loc_old = cursor.fetchone()
    cursor.execute(
        f"""UPDATE location SET latitude = {message.location.latitude} WHERE latitude = '{loc_old[5]}'""")
    cursor.execute(
        f"""UPDATE location SET longitude = {message.location.longitude} WHERE longitude = '{loc_old[6]}'""")
    conn.commit()

    cursor.close()
    conn.close()


def db_update_city(message, city):
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()

    cursor.execute(f"""SELECT * FROM location WHERE id={message.from_user.id}""")
    city_old = cursor.fetchone()
    cursor.execute(f"""UPDATE location SET city = '{city}' WHERE city = '{city_old[7]}'""")
    conn.commit()

    cursor.close()
    conn.close()


def db_update_loc_city(message, lat, lon):
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()

    cursor.execute(f"""SELECT * FROM location WHERE id={message.from_user.id}""")
    loc_old = cursor.fetchone()
    cursor.execute(
        f"""UPDATE location SET lat_city = {lat} WHERE lat_city = '{loc_old[8]}'""")
    cursor.execute(
        f"""UPDATE location SET lon_city = {lon} WHERE lon_city = '{loc_old[9]}'""")
    conn.commit()

    cursor.close()
    conn.close()


def db_read(user_id):
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()

    cursor.execute(f"""SELECT * FROM location WHERE id={user_id}""")
    old = cursor.fetchone()
    name_loc = old[3]
    name_loc_full = old[4]
    lat = old[5]
    lon = old[6]
    city = old[7]
    lat_city = old[8]
    lon_city = old[9]

    cursor.close()
    conn.close()
    return name_loc, name_loc_full, lat, lon, city, lat_city, lon_city
