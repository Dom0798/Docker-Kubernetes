import os
import sys
import json
import pathlib

from flask import (Blueprint, Flask, flash, jsonify, redirect, render_template,
                   request, session, url_for)
from flask_restful import Api, Resource, reqparse
from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import HTTPException

app = Flask(__name__)#template_folder='templates', static_folder='static')
app.secret_key = 'secretkey'
app.config['JSON_SORT_KEYS'] = False
api = Api(app)
file = os.path.join(pathlib.Path().resolve(), 'story', 'text.txt')

class story(Resource):
    def get(self):
        with open(file,'r') as f:
            content = f.read()
        return content, 200

    def post(self):
        data = request.data.decode()
        with open(file,'a') as f:
            f.write(data+'<br>')
        return 'Story stored!', 200

class error(Resource):
    def get(self):
        return os._exit(1)
 
api.add_resource(story, '/story')
api.add_resource(error, '/error')

if __name__ == '__main__':
    app.run(host= '0.0.0.0', port= os.environ.get('PORT'), debug=True)