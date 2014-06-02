import os
from flask import Flask, jsonify, render_template, url_for
import json

app = Flask(__name__)
app.config.from_pyfile('config.py')

@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route('/campaigns/')
def campaigns_json():
	f = json.loads(open('campaigns.json').read())
	return jsonify(results=f)