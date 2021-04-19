import mysql.connector
from mysql.connector import errorcode

# Choose user connection
# 1. Niko
# 2. Lucas
DATABASE = 1


def data_warehouse():
    dw = None
    try:
        # Connections
        # Nicolau Database
        if DATABASE == 1:
            # Data warehouse connection
            dw = mysql.connector.connect(
                host="localhost",
                user="root",
                password="951847",
                database="cs_go_dw",
            )

        # Lucas Database
        if DATABASE == 2:
            # Data warehouse connection
            dw = mysql.connector.connect(
                host="localhost",
                user="lucas",
                password="",
                database="csgo_stats_dw",
                charset='utf8',
                use_unicode=True,
                connect_timeout=2000,
                buffered=True
            )
        return dw
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)


def database():
    db = None

    try:
        # Connections
        # Nicolau Database
        if DATABASE == 1:
            # Database connection
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="951847",
                database="cs_go",
                charset='utf8',
                use_unicode=True,
                connect_timeout=2000,
                buffered=True

            )

        # Lucas Database
        if DATABASE == 2:
            # Database connection
            db = mysql.connector.connect(
                host="localhost",
                user="lucas",
                password="",
                database="csgo_stats",
                charset='utf8',
                use_unicode=True,
                connect_timeout=2000,
                buffered=True
            )

        return db

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)


def close_connection(conn):
    conn.close()
