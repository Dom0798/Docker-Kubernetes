import ast
import json
import os
import sys
import re

import mysql.connector
import pandas as pd
from flask import (Blueprint, Flask, flash, jsonify, redirect, render_template,
                   request, session, url_for)
from flask_restful import Api, Resource, reqparse
from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import HTTPException

# UPLOAD_FOLDER = 'C:\\Patriot\\DDServiceAPI\\uploads'
# ALLOWED_CONTENT_TYPE = set(['image/jpg', 'image/jpeg'])

app = Flask(__name__)#template_folder='templates', static_folder='static')
app.secret_key = 'secretkey'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['JSON_SORT_KEYS'] = False
api = Api(app)

# def conf_database():
#     """Function to return the database configuration set in database.json

#     Returns:
#         data (dict): dict with json info
#     """
#     filename = os.path.join("C:\LSSApps\ManagersForecasting\database.json")
#     with open(filename) as f:
#         data = json.load(f)
#     return data

# class results(Resource):
#     """Class with a GET request handler to fetch the Fabrication Continuation Status.
#     """
#     def get(self):
#         parse = reqparse.RequestParser()                                                                                                    # add two arguments: failed_limit and prev_results_stack
#         parse.add_argument('failed_limit', type=int, location='args', default=2)
#         parse.add_argument('prev_results_stack', type=int, location='args', default=2)
#         args = parse.parse_args()

#         cdb = conf_database()                                                                                                               # connect to database and create cursor
#         mydb = mysql.connector.connect(
#             host= cdb['host'],
#             user= cdb['user'],
#             password= cdb['password'],
#             database= cdb['database']
#         )
#         mycursor = mydb.cursor()
        
#         mycursor.execute(f"SELECT count(*) FROM (select result from defectdetections.parts where status = 100 order by id desc limit {args['prev_results_stack']}) as r where result='Failed'")
#         prev_stack = mycursor.fetchone()[0]                                                                                                 # select previous stack of results of only finished analysis and count the failed ones
#         flim = args['failed_limit']

#         if prev_stack==args['failed_limit']:                                                                                                # if count of failed results is equal to the failed limit, return HALT
#             return {'response': 'HALT','flim':flim,'prevstack': prev_stack}, 200

#         mycursor.execute(f"select result from parts where id=(select max(id) from parts where status = 100)")
#         last_result = mycursor.fetchone()[0]                                                                                                # select the last completed analysis result

#         if last_result == "Passed":                                                                                                         # if last result is Passed, return OK
#             return {'response': 'OK','flim':flim,'prevstack': prev_stack,'result':last_result}, 200

#         return {'response': 'INSPECT','flim':flim,'prevstack': prev_stack,'result':last_result}, 200                                        # if last result is Failed, return INSPECT

# class oneresult(Resource):
#     """Class with a GET rquest handler to fetch the information from a specific part.
#     """
#     def get(self, part_id):
#         cdb = conf_database()                                                                                                               # connect to database and create cursor
#         mydb = mysql.connector.connect(
#             host= cdb['host'],
#             user= cdb['user'],
#             password= cdb['password'],
#             database= cdb['database']
#         )
#         mycursor = mydb.cursor()

#         mycursor.execute(f"select * from parts where part_id={part_id}")                                                                    # select everything from the specific part
#         results = mycursor.fetchall()

#         if results:                                                                                                                         # if a result exist, return the information
#             results = results[0]
#             return {"part_id": results[1], "status": results[2], "form factor": results[3], 
#                     "datetime": str(results[4]), "result": results[5], "defects": results[6], "analysis_path": results[7]}, 200
#         else:
#             return f'No results found for part_id: {part_id}', 500                                                                          # if not, return message

# class upload(Resource):
#     """Class with a POST request hanlder to record the image for the Image Analysis Initiation.
#     """
#     def post(self, part_id):
#         parse = reqparse.RequestParser()                                                                                                    # add the image argument
#         parse.add_argument('image', type=FileStorage, location='files')
#         args = parse.parse_args()

#         image_file = args['image']
#         if not image_file:                                                                                                                  # check if an image was sent in request
#             return 'No image sent', 500

#         if image_file.content_type in ALLOWED_CONTENT_TYPE:                                                                                 # check if image extension is permitted
#             image_file.save(os.path.join(UPLOAD_FOLDER,f"{part_id}.jpeg"))                                                                  # save image in the folder set
#             return f'Image {part_id}.jpeg created in server', 200
#         else:
#             return f'Image type not allowed. Only jpeg or jpg.', 500

# api.add_resource(results, '/results')                                                                                                       # add API resources to API Gateway
# api.add_resource(oneresult, '/oneresult/<string:part_id>')
# api.add_resource(upload, '/upload/<string:part_id>')

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

        # cdb = conf_database()                                                                                                               # connect to database and create cursor
        # mydb = mysql.connector.connect(
        #     host= cdb['host'],
        #     user= cdb['user'],
        #     password= cdb['password'],
        #     database= cdb['database']
        # )
        # mycursor = mydb.cursor()
        # mycursor.execute('SELECT * FROM users WHERE user = %s AND password = %s', (user_name, password,))
        # account = mycursor.fetchone()
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
        # cdb = conf_database()                                                                                                               # connect to database and create cursor
        # mydb = mysql.connector.connect(
        #     host= cdb['host'],
        #     user= cdb['user'],
        #     password= cdb['password'],
        #     database= cdb['database']
        # )
        # mycursor = mydb.cursor()
        # mycursor.execute('SELECT * FROM users WHERE user = %s', (user_name,))
        # account = mycursor.fetchone()
        # if account:
        #     msg = 'Account already exists!'
        # elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
        #     msg = 'Invalid email address!'
        # elif not re.match(r'^[A-Za-z0-9]+$', user_name):
        #     msg = 'Username must contain only characters and numbers!'
        # else:
        #     mycursor.execute('INSERT INTO users VALUES (NULL, %s, %s, %s)', (user_name, password, email,))
        #     mydb.commit()
        #     msg = 'You have successfully registered!'
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
        # cdb = conf_database()                                                                                                               # connect to database and create cursor
        # mydb = mysql.connector.connect(
        #     host= cdb['host'],
        #     user= cdb['user'],
        #     password= cdb['password'],
        #     database= cdb['database']
        # )
        # mycursor = mydb.cursor()

        # # mycursor.execute(f"select * from parts where status=100 order by id desc limit 5")                                                  # select everything from the specific part
        # book = load_workbook("C:\\Users\\H483882\\OneDrive - Honeywell\\Desktop\\dummyhours.xlsx")
        # sheet = book.active
        # results = pd.DataFrame(sheet.values)
        # results.fillna('', inplace=True)
        # return render_template('template.html', sheet= results.to_html())
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
    app.run(host= '0.0.0.0', port= 5000, debug=True)