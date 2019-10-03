import sqlite3


def db_check():
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()

    cursor.execute("""SELECT * FROM location""")
    row = cursor.fetchone()
    # выводим список пользователей в цикле
    while row is not None:
        print(
            f"| id: {str(row[0])} |/| dt_cr_us: {str(row[1])} |/| dt_ls_vs: {str(row[2])} |/| name_loc: {str(row[3])} "
            f"|/| name_loc_full: {str(row[4])} |/| lat: {str(row[5])} |/| lon: {str(row[6])} "
            f"|/| city: {str(row[7])} |/| lat_city: {str(row[8])} |/| lon_city: {str(row[9])} "
            f"|/| username: {str(row[10])} |/| first_name: {str(row[11])} |/| last_name: {str(row[12])} |\n")
        row = cursor.fetchone()

    cursor.close()
    conn.close()


# Удоление поля по id
def db_delete_field(user_id):
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()

    sql = f"""DELETE FROM location WHERE id = {user_id}"""

    cursor.execute(sql)
    conn.commit()

    cursor.close()
    conn.close()


db_check()
