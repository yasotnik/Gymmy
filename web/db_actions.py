import sqlite3


def connect_to_db(database):
    """
    Connecting to specific database
    :param database: Name of the DB
    :return: -1 if could not connect to DB
    """
    try:
        return sqlite3.connect(database)
    except Exception:
        print ("DB connection error!")
        return None


def add_user(id,pwd):
    """
    :param id: username
    :param pwd: password
    """

    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (id, password) VALUES (?,?)", (id, pwd))
    conn.commit()
    conn.close()
