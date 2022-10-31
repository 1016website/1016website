from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.shbwsw1.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

import requests
from bs4 import BeautifulSoup

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/save", methods=["POST"])
def save_post():
    url_receive = request.form['url_give']
    star_receive = request.form['star_give']
    comment_receive = request.form['comment_give']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    title = soup.title.text
    desc = soup.select_one('meta[property="og:description"]')['content']

    image = soup.select_one('meta[property="og:image"]')['content']
    print(image)

    doc = {'star': star_receive,
           'comment': comment_receive,
           'title': title,
           'desc': desc,
           'image' : image
           }
    db.toy.insert_one(doc)

    return jsonify({'msg':'POST 연결 완료!'})

@app.route("/show", methods=["GET"])
def show_post():
    all_videos = list(db.toy.find({}, {'_id': False}))
    return jsonify({'videos':all_videos})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)