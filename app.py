from pymongo import MongoClient
from flask import Flask, render_template, jsonify, request
from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash

import certifi

ca = certifi.where()
client = MongoClient('mongodb+srv://test:sparta@cluster0.hqmjigh.mongodb.net/Cluster0?retryWrites=true&w=majority',
                     tlsCAFile=ca)
db = client.dbsparta
app = Flask(__name__)
bcrypt = Bcrypt(app)


@app.route('/')
def home():
    return render_template('signup.html')


@app.route('/user/signup', methods=['POST'])
def signup():
    # id, password 받아오고 저장
    user_id = request.form['user_id']
    user_pwd = request.form['user_pwd']
    user_nick = request.form['user_nick']
    pw_hash = generate_password_hash(user_pwd)

    # id 중복확인
    if db.user.count_documents({'user_id': user_id}) == 0:
        db.user.insert_one({'user_id': user_id, 'user_pwd': pw_hash, 'user_nick': user_nick})
        return jsonify({'result': 'SUCCESS', 'message': 'SIGN UP SUCCESS'})
    else:
        return jsonify({'result': 'FAIL', 'message': 'user_id already exists'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
