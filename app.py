from flask import Flask, send_file

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return ""

@app.route('/data_latest', methods=['GET'])
def about():
	return send_file('data_latest.txt', attachment_filename='data_latest.txt')