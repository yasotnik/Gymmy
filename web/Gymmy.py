from flask import Flask, render_template, abort, request, redirect, url_for, jsonify, session, escape
from flask_bootstrap import Bootstrap
import os, hashlib
import db_actions
import socket

app = Flask(__name__)
Bootstrap(app)
app.secret_key = os.urandom(24)
led_status = 'Off'


@app.route('/')
def mainpage():
    return redirect(url_for('index'))


@app.route('/index.html', methods=['POST', 'GET'])
def index():
    return render_template('index.html', logged=False)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        m = hashlib.md5()
        m.update(password)
        password = m.hexdigest()
        print ("USERNAME:" + username + ",password:" + password)
        pwd_md5 = db_actions.get_user(username)
        print pwd_md5[0]
        if pwd_md5[0] == password:
            print "LOGGED"
            return render_template('index.html', logged=True, name=username)
    return render_template('index.html', name=username, logged=False)


@app.route('/logout')
def logout():
    session.pop('username', None)
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
    db_actions.add_user(username,pass_md5)
    return render_template('index.html', logged=True, name=username)


def led():
    sock = socket.socket()
    sock.bind(('', 6666))
    sock.listen(1)
    conn, addr = sock.accept()
    print 'Connected from ', addr

    while True:
        data = conn.recv(256)
        if not data:
            break

        conn.send('next')

    conn.close()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
    led()
