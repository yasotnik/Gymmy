import hashlib
import os
from flask import Flask, render_template, request, redirect, url_for, session
from flask_bootstrap import Bootstrap
import time
import sys

sys.path.insert(0, '../libs')
import db_actions

app = Flask(__name__)
Bootstrap(app)
app.secret_key = os.urandom(24)
app.config['SECRET_KEY'] = os.urandom(24)

# Logs
localtime = time.asctime(time.localtime(time.time()))
log_name = 'log' + localtime
log = open(log_name, 'w')


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
        print (" USERNAME:" + username + ",password:" + password)
        log.write(localtime + "USER LOGIN: Credentials username: " + username + ","
                                                                             "password:" +
                  password + "\n")
        if db_actions.get_user(username):
            pwd_md5 = db_actions.get_user(username)
            group = db_actions.get_user_group(username)
            if pwd_md5 == password and group == 'admin':
                # Admin page
                usrnm = username
                print "LOGGED as Admin"
                log.write(localtime + "USER LOGIN: User logged successfully as:" +
                          username + ", group: " + group + "\n"     )
                session['admin'] = 'admin'
                return render_template('index.html', logged=True, name=username,
                                       admin=True, showtime=False)
            elif pwd_md5 == password and group != 'admin':
                # Regular user page
                usrnm = username
                print "LOGGED as" + usrnm
                return render_template('index.html', logged=True, name=username,
                                       admin=False)
            else:
                # Incorrect password
                print "ERR PWD"
                return render_template('index.html', logged=False, name=username,
                                       error='The password is incorrect')
        else:
            # Incorrect user
            print "ERR USR"
            return render_template('index.html', logged=False, name=username,
                                   error='This user doesn\'t exist')
    print "SHIT"
    return 0


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/start_training')
def start_training():
    db_actions.insert_start()
    return render_for_user(session['username'])


@app.route('/stop_training')
def stop_training():
    db_actions.insert_stop()
    stat = db_actions.get_time()
    print stat
    return render_for_user(session['username'], stat)


@app.route('/start_writing', methods=['POST', 'GET'])
def start_writing():
    name = str(request.form['mapname'])
    print "New map name: " + name
    db_actions.start_wr_path(name)
    return render_for_user(session['username'],'')


@app.route('/stop_writing')
def stop_writing():
    db_actions.stop_wr_path()
    return render_for_user(session['username'],'')


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
    return redirect(url_for('index'))


def render_for_user(id,stattime):
    if db_actions.get_user_group(id) == 'admin':
        return render_template('index.html', logged=True, name=session['username'],
                           admin=True,time=stattime)
    elif db_actions.get_user_group(id):
        return render_template('index.html', logged=True, name=session['username'],
                           admin=False,time=stattime)
    else:
        return render_template('index.html', logged=False, name=session['username'],
                           admin=False)


def flask():
    app.run(debug=True, host='0.0.0.0', threaded=True)


if __name__ == '__main__':
    flask()
