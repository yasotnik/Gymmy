from flask import Flask, render_template, abort, request, redirect, url_for, jsonify, session, escape
from flask_bootstrap import Bootstrap
import os, hashlib
import sqlite3

app = Flask(__name__)
Bootstrap(app)
app.secret_key = os.urandom(24)


@app.route('/')
def mainpage():
    return redirect(url_for('index'))


@app.route('/index.html', methods=['POST', 'GET'])
def index():
    if 'username' in session:
        username = session['username']
        return render_template('index.html', logged=True, name=username)
    return render_template('index.html', logged=False)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        phrase = request.form['password']
        m = hashlib.md5()
        m.update(phrase)
        pass_md5 = m.hexdigest()
        session['password'] = pass_md5
        username = session['username']
        password = session['password']
        print ("USERNAME:" + username + ",password:" + password)
    return render_template('index.html', name=username, logged=True)


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
    database = 'static/DB'
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (id, password) VALUES (?,?)", (username, pass_md5))
    conn.close()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
