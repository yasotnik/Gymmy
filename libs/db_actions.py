import MySQLdb


def connect_to_db():
    try:
        db = MySQLdb.connect("192.168.1.67", "lev2", "sasai228", "Gymmy")
        return db;
    except Exception:
        print "Connection failed!"


def add_user(id,pwd):
    """
    :param id: username
    :param pwd: password
    """
    db = connect_to_db()
    cursor = db.cursor()
    sql = "INSERT INTO users(id, \
       password) \
       VALUES ('%s', '%s')" % \
       (id, pwd)
    try:
        cursor.execute(sql)
        db.commit()
    except Exception:
        print "Couldn't insert"
    db.close()


def get_user(id):
    """
    Get user by his id
    :param id: id of the user
    :return: password of user or 0 if was a problem
    """
    db = connect_to_db()
    cursor = db.cursor()
    sql = "SELECT password FROM users \
       WHERE id = '%s'" % (id)
    try:
        cursor.execute(sql)
        password = cursor.fetchone()
        return password
    except Exception as e:
        print "Couldn't find user. Error: " + e
        return 0
    finally:
        db.close()


def insert_start():
    db = connect_to_db()
    cursor = db.cursor()
    sql = "UPDATE statistics SET start='start',stop='' WHERE id=1"
    try:
        cursor.execute(sql)
        db.commit()
        print "MySQL: - Stop + Start"
    except Exception:
        print "Couldn't add start"
    db.close()


def insert_stop():
    db = connect_to_db()
    cursor = db.cursor()
    sql = "UPDATE status SET start='',stop='stop' WHERE id=1"
    try:
        cursor.execute(sql)
        db.commit()
        print "MySQL: + Stop - Start"
    except Exception:
        print "Couldn't add stop"
    db.close()

def start_wr_path(name):
    db = connect_to_db()
    cursor = db.cursor()
    sql = "UPDATE status SET map='%s' WHERE id=1" % (name)
    try:
        cursor.execute(sql)
        db.commit()
        print "MySQL: + Map, name: " + name
    except Exception:
        print "Couldn't add map"
    db.close()


def stop_wr_path():
    db = connect_to_db()
    cursor = db.cursor()
    sql = "UPDATE status SET map='NULL' WHERE id=1"
    try:
        cursor.execute(sql)
        db.commit()
        print "MySQL: + Stop - Start"
    except Exception:
        print "Couldn't add stop"
    db.close()


def add_time(time):
    db = connect_to_db()
    cursor = db.cursor()
    sql = "INSERT INTO statistics VALUES (0, '%d')" % (time)
    try:
        cursor.execute(sql)
        db.commit()
        print "MySQL: + New time"
    except Exception:
        print "Couldn't add new time"
    db.close()


def get_status(str):
    db = connect_to_db()
    cursor = db.cursor()
    start = "SELECT start FROM status \
       WHERE id = 1"
    stop = "SELECT stop FROM status \
       WHERE id = 1"
    try:
        if (str == "start"):
           cursor.execute(start)
        elif (str == "stop"):
            cursor.execute(stop)
        status = cursor.fetchone()
        return status[0]
    except Exception:
        print "Couldn't get status"
        return 0
    finally:
        db.close()


def get_map(str):
    db = connect_to_db()
    cursor = db.cursor()
    sql = "SELECT Map FROM map \
       WHERE Difficulty = '%s'" % (str)
    try:
        cursor.execute(sql)
        map = cursor.fetchone()
        return map[0]
    except Exception as e:
        print "Couldn't get map"
        return 0
    finally:
        db.close()
