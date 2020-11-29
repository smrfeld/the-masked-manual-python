from flask import Flask, redirect, render_template

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/terms_and_conditions', methods=['GET'])
def terms_and_conditions():
    return render_template('terms_and_conditions.html')

@app.route('/privacy_policy', methods=['GET'])
def privacy_policy():
    return render_template('privacy_policy.html')

@app.route('/github', methods=['GET'])
def github():
    return redirect('https://github.com/smrfeld/the-masked-manual-python')

@app.route('/ios_app_store', methods=['GET'])
def ios_app_store():
    return render_template('index.html')

@app.route('/data_latest', methods=['GET'])
def data_latest():
    return redirect("https://storage.googleapis.com/the-masked-manual-data/data_latest.txt")
	# return send_file('data_latest.txt', attachment_filename='data_latest.txt')