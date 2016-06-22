from flask import Flask, render_template, abort, request, redirect, url_for, jsonify, session, escape
from flask_bootstrap import Bootstrap
#from flask_socketio import SocketIO
import os, hashlib
import db_actions
import socket
import threading, multiprocessing
import thread
from multiprocessing import Process
from socket import error as SocketError
import errno


app = Flask(__name__)
Bootstrap(app)
app.secret_key = os.urandom(24)
app.config['SECRET_KEY'] = os.urandom(24)
led_status = 'Off'
#socketio = SocketIO(app)


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
    app.run(debug=True, host='0.0.0.0')


if __name__ == '__main__':
    p1 = Process(target=flask)
    p1.start()
    p2 = Process(target=server)
    p2.start()
    p1.join()
    p2.join()
