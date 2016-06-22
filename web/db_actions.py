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
    db = connect_to_db()
    cursor = db.cursor()
    sql = "SELECT password FROM users \
       WHERE id = '%d'" % (id)
    try:
        cursor.execute(sql)
        password = cursor.fetchone()
        return password
    except:
        print "Couldn't find user"
        return 0
    finally:
        db.close()
