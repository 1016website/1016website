from pymongo import MongoClient
from flask import Flask, render_template, jsonify, request
from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, set_refresh_cookies, JWTManager, get_jwt, \
    set_access_cookies, jwt_required, get_jwt_identity
from datetime import timedelta, datetime, timezone

import certifi

ca = certifi.where()
client = MongoClient('mongodb+srv://test:sparta@cluster0.hqmjigh.mongodb.net/Cluster0?retryWrites=true&w=majority',
                     tlsCAFile=ca)
db = client.dbsparta
app = Flask(__name__)
bcrypt = Bcrypt(app)

# JWT
jwt = JWTManager(app)

JWT_ACCESS_COOKIE_PATH = '/'  # access cookie를 보관할 url (Frontend 기준)
JWT_REFRESH_COOKIE_PATH = '/'  # refresh cookie를 보관할 url (Frontend 기준)
# CSRF 토큰 역시 생성해서 쿠키에 저장할지
# (이 경우엔 프론트에서 접근해야하기 때문에 httponly가 아님)

app.config["JWT_COOKIE_SECURE"] = False
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=30)
app.config["JWT_SECRET_KEY"] = "OK"





@app.route("/", methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/user/signup')
def move_signup():
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


@app.route('/user/login')
def move_login():
    return render_template('login.html')


@app.route('/user/login', methods=['POST'])
def login():
    # id, password 받아오귀
    user_id = request.form['user_id']
    user_pwd = request.form['user_pwd']
    # id 확인
    if db.user.count_documents({'user_id': user_id}) == 0:
        # 401 error : 인증 자격 없음
        return jsonify({'result': 'FAIL', 'message': 'WRONG ID'})  # , 401
    # else:
    # 비번 확인
    # count_documents VS findone?
    check_pwd = db.user.find_one({"user_id": user_id})
    # 로그인 시 입력한 암호를 암호화해서 저장된 비밀번호와 비교하기
    if check_password_hash(check_pwd.get('user_pwd'), user_pwd):

        access_token = create_access_token(identity=user_id)
        refresh_token = create_refresh_token(identity=user_id)
        response = jsonify({'result': 'SUCCESS', 'access_token': access_token})

        set_access_cookies(response, access_token)
        set_refresh_cookies(response, refresh_token)
        return response, 200
    else:
        return jsonify({'result': 'FAIL', 'message': 'WRONG PWD'})  # , 401


@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()  # 식별자로 넣어준 값들을 조회 할 수 있다

    return jsonify(logged_in_as=current_user), 200


@app.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]  # 만료시간을 찍는
        now = datetime.now(timezone.utc)  # 현재시간 출력하는데, 기준시는 협정 세계시
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))  # 지금 시간으로 부터 30분 추가한 대상시
        if target_timestamp > exp_timestamp:  # 대상시가 만료시간보다 크면
            access_token = create_access_token(identity=get_jwt_identity())  # 다시 토큰을 갱신
            set_access_cookies(response, access_token)  # 갱신한 토큰을 다시 쿠키에 저장
        return response  # 갱신한 토큰이 담긴 쿠키가 있는 response를 반환
    except (RuntimeError, KeyError):
        return response  # 유효하지 않은 jwt라 갱신하지 않고 오리지날을 반환


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
