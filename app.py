from flask import Flask, redirect

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return ""

@app.route('/data_latest', methods=['GET'])
def data_latest():
    return redirect("https://storage.googleapis.com/the-masked-manual-data/data_latest.txt")
	# return send_file('data_latest.txt', attachment_filename='data_latest.txt')