import mysql.connector
from mysql.connector import errorcode

try:
    # Connections

    # Database connection

    # Nicolau Database
    #  db = mysql.connector.connect(
    #      host="localhost",
    #      user="",
    #      password="",
    #      database=""
    #  )
    #
    # # Datawarehouse connection
    #  dw = mysql.connector.connect(
    #      host="localhost",
    #      user="",
    #      password="",
    #      database=""
    #  )

    # Lucas Database
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
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)


def close_connections():
    db.close()
    dw.close()
