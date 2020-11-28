from flask import Flask, send_file

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def index():
    return ""

@app.route('/data_latest', methods=['GET','POST'])
def about():
	return send_file('data_latest.txt', attachment_filename='data_latest.txt')