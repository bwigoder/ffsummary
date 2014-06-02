import os
from flask import Flask
import json

app = Flask(__name__)
app.config.from_pyfile('config.py')

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/campaigns.json')
def campaigns_json():
	f = json.loads(open('campaigns.json').read())
	flask.jsonify(**f)