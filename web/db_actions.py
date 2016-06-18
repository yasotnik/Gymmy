import sqlite3

def connect_to_db(database):
    """
    Connecting to specific database
    :param database: Name of the DB
    :return: -1 if could not connect to DB
    """
    try:
        return sqlite3.connect(database)
    except IOError:
        print ("DB connection error!")
        return -1


def add_user(id,pwd):
    """
    :param id: username
    :param pwd: password
    """
    sql = """ INSERT INTO users()"""