import os
import sys

from flask import (Blueprint, Flask, flash, jsonify, redirect, render_template,
                   request, session, url_for)
from flask_restful import Api, Resource, reqparse
from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import HTTPException

app = Flask(__name__)#template_folder='templates', static_folder='static')
app.secret_key = 'secretkey'
app.config['JSON_SORT_KEYS'] = False
api = Api(app)

@app.route('/')
def index():
    if 'loggedin' in session:
        return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route('/dashboard/login', methods=['GET','POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        user_name = request.form['username']
        password = request.form['password']

        with open ("data/user.txt","a") as f:
            f.write(user_name)
        account = [user_name, password]
        if account:
            session['loggedin'] = True
            session['id'] = account[0]
            session['user'] = account[1]
            return redirect(url_for('home'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('template_login.html', msg=msg)

@app.route('/dashboard/register', methods=['GET','POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        user_name = request.form['username']
        password = request.form['password']
        email = request.form['email']

    return render_template('template_register.html', msg=msg)

@app.route('/dashboard/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('user', None)
    # Redirect to login page
    return redirect(url_for('login'))

@app.route('/dashboard/home', methods=['GET','POST'])
def home():
    if 'loggedin' in session:
        if request.method == 'POST' and 'message' in request.form:
            message = request.form['message']
            with open ("data/messages.txt","a") as f:
                f.write(message)
            print(message, file=sys.stderr)
        return render_template('template.html')
    return redirect(url_for('login'))

@app.route('/dashboard/stats')
def stats():
    if 'loggedin' in session:
        return render_template('template_stats.html')
    return redirect(url_for('login'))

@app.route('/dashboard/settings')
def settings():
    if 'loggedin' in session:
        return render_template('template_settings.html', user_name=session['user'])
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host= '0.0.0.0', port= os.environ.get('PORT'), debug=True)