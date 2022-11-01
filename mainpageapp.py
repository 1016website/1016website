from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/<path>')
def get_path(path):
    return render_template(path+'.html')

