import os
from flask import Flask, jsonify, render_template, url_for
import requests
import json
import urllib2

app = Flask(__name__)
app.config.from_pyfile('config.py')

@app.route('/')
def hello():
	return render_template('hello.html')