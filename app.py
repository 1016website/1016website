from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
import certifi

ca = certifi.where()
client = MongoClient('mongodb+srv://test:sparta@cluster0.sx4vg7k.mongodb.net/?retryWrites=true&w=majority',tlsCAFile=ca)
db = client.dbsparta



@app.route('/')
def home():
    return render_template('index.html')

@app.route('/<path>')
def get_path(path):
    return render_template(path+'.html')


if __name__ == '__main__':
    app.run('0.0.0.0', port=5002, debug=True)