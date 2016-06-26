import errno
import hashlib
import os
import socket
from socket import error as SocketError
from flask import Flask, render_template, request, redirect, url_for, session
from flask_bootstrap import Bootstrap

import sys
sys.path.insert(0, '../libs')
import db_actions

app = Flask(__name__)
Bootstrap(app)
app.secret_key = os.urandom(24)
app.config['SECRET_KEY'] = os.urandom(24)


@app.route('/')
def mainpage():
    return redirect(url_for('index'))


@app.route('/index.html', methods=['POST', 'GET'])
def index():
    if 'username' in session:
        return render_template('index.html', logged=True, name=session['username'])
    return render_template('index.html', logged=False)


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        username = request.form['username']
        password = request.form['password']
        # Encrypting the password
        m = hashlib.md5()
        m.update(password)
        password = m.hexdigest()
        global usrnm
        print ("USERNAME:" + username + ",password:" + password)
        if db_actions.get_user(username):
            pwd_md5 = db_actions.get_user(username)
            if pwd_md5[0] == password and username == "Admin":
                usrnm = username
                print "LOGGED AS ADMIN"
                return render_template('admin.html', logged=True, name=username)
            elif pwd_md5[0] == password:
                usrnm = username
                print "LOGGED"
                return render_template('index.html', logged=True, name=username)
            else:
                # Comparing password with password from DB
                print "ERR PWD"
                return render_template('index.html', logged=False, name=username, error='The password is incorrect')
        else:
            # Comparing password with password from DB
            print "ERR USR"
            return render_template('index.html', logged=False, name=username, error='This user doesn\'t exist')
    print "SHIT"
    return 0


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/start_training')
def start_training():
    db_actions.insert_start()
    return redirect(url_for('index'))


@app.route('/stop_training')
def stop_training():
    db_actions.insert_stop()
    return redirect(url_for('index'))


@app.route('/sign_up.html')
def signup_page():
    return render_template('sign_up.html')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    username = str(request.form['username'])
    password = str(request.form['password'])
    m = hashlib.md5()
    m.update(password)
    pass_md5 = m.hexdigest()
    print pass_md5
    db_actions.add_user(username, pass_md5)
    return render_template('index.html', logged=True, name=username)


def server():
    sock = socket.socket()
    sock.bind(('', 9092))
    sock.listen(1)
    print("Server started!")
    conn, addr = sock.accept()
    print 'Connected from ', addr
    while True:
        try:
            data = conn.recv(256)
            if data:
                print ("Recieved: " + data)
                if data == "1":
                    conn.send("pinLED0")
                    print ("Sent : " + "pinLED0")
                elif data == "0":
                    conn.send("pinLED1")
                    print ("Sent : " + "pinLED1")
                else:
                    conn.send('next nothing')
        except SocketError as e:
            print e
            if e.errno != errno.ECONNRESET:
                pass
            conn.close()
            print("Server restarted!")
            conn, addr = sock.accept()
    conn.close()


def flask():
    app.run(debug=True, host='0.0.0.0', threaded=True)


if __name__ == '__main__':
    flask()
    """
    p1 = Process(target=flask)
    p1.start()
    p2 = Process(target=server)
    p2.start()
    p1.join()
    p2.join()
    """
