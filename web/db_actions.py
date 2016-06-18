import sqlite3


def connect_to_db():
    """
    Connecting to specific database
    :param database: Name of the DB
    :return: -1 if could not connect to DB
    """
    database = 'static/DB'
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


def get_user(id):
    """
    Parsing user credentials from DB
    :param id: username
    :return: password
    """
    conn = connect_to_db()
    conn.text_factory = sqlite3.OptimizedUnicode
    cursor = conn.cursor()
    sql = "SELECT password FROM users WHERE id = ?"
    cursor.execute(sql, (str(id), ))
    password = cursor.fetchone()
    conn.close()
    return password