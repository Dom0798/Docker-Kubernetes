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
    return render_template('welcome.html')

if __name__ == '__main__':
    app.run(host= '0.0.0.0', port= os.environ.get('PORT'))