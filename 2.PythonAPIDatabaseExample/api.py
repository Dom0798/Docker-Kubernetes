import os
import sys
import json
import requests

from flask import (Blueprint, Flask, flash, jsonify, redirect, render_template,
                   request, session, url_for)
from flask_restful import Api, Resource, reqparse
import mysql.connector
from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import HTTPException

app = Flask(__name__)#template_folder='templates', static_folder='static')
app.secret_key = 'secretkey'
app.config['JSON_SORT_KEYS'] = False
api = Api(app)

def conf_database():
    """Function to return the database configuration set in database.json

    Returns:
        data (dict): dict with json info
    """
    filename = os.path.join("database.json")
    with open(filename) as f:
        data = json.load(f)
    return data

class infoapi(Resource):
    """Class with a GET
    """
    def get(self, pokemon):
        x = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon}')

        if x.status_code == 200:
            x = x.json()
            return {'pokemon_name':x['forms'][0]['name'], 'id': x['id']
                    ,'type':x['types'][0]['type']['name']}, 200                                        # if last result is Failed, return INSPECT
        else:
            return 'No pokemon with that name', 200
        
class getfromdb(Resource):
    """Class with a GET
    """
    def get(self, poke_name):
        cdb = conf_database()                                                                                                               # connect to database and create cursor
        mydb = mysql.connector.connect(
            host= cdb['host'],
            user= cdb['user'],
            password= cdb['password'],
            database= cdb['database']
        )
        mycursor = mydb.cursor()

        mycursor.execute('SELECT * FROM fav_pokemons WHERE poke_name = %s;', (poke_name,))               # select everything from the specific part
        
        pokeid = mycursor.fetchone()
        if pokeid:
            return {"pokemon": pokeid[1], "is_fav": pokeid[2]}, 200
        else:
            return 'No pokemon with that name in db', 200

class posttodb(Resource):
    def post(self):
        poke_name = request.json['poke_name']
        is_fav = request.json['is_fav']

        cdb = conf_database()                                                                                                               # connect to database and create cursor
        mydb = mysql.connector.connect(
            host= cdb['host'],
            user= cdb['user'],
            password= cdb['password'],
            database= cdb['database']
        )
        mycursor = mydb.cursor()

        try:
            mycursor.execute("insert into fav_pokemons values (NULL, %s, %s);", (poke_name, is_fav))               # select everything from the specific part
            mydb.commit()
        except Exception as e:
            return e, 500

        return f'Added {poke_name} to database', 200
 
api.add_resource(infoapi, '/info/<string:pokemon>')                                                                                                       # add API resources to API Gateway
api.add_resource(getfromdb, '/get/<string:poke_name>')
api.add_resource(posttodb, '/post')

if __name__ == '__main__':
    app.run(host= '0.0.0.0', port= os.environ.get('PORT'), debug=True)