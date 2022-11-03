# 기본
from flask import Flask, request, jsonify, render_template
# DB
from pymongo import MongoClient
# 로그인과 회원가입
from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, get_jwt_identity, unset_jwt_cookies, create_refresh_token,
    set_access_cookies, set_refresh_cookies, get_jwt)
from datetime import timedelta, datetime, timezone
# 크롤링
import requests
from bs4 import BeautifulSoup
# 맥 보안
import certifi

ca = certifi.where()
client = MongoClient('mongodb+srv://test:sparta@cluster0.hqmjigh.mongodb.net/Cluster0?retryWrites=true&w=majority',
                     tlsCAFile=ca)
db = client.dbsparta
app = Flask(__name__)
bcrypt = Bcrypt(app)

# ----------------------------------------------------------------------

# __name__ 변수는 모듈의 이름을 가진 변수로 실행하는 기준이 되는 py의 이름은 __main__에 해당한다.
# 만약 app.py에서 another.py라는 모듈을 사용했다면 app.py의 __name__ == __main__ , another.py의 __name__ == another가 된다.
# Flask(__name__) 라우팅 경로를 설정. 해당 라우팅 경로로 요청이 올 때 실행할 함수를 아래에 작성한다.
app = Flask(__name__)

# jwt 가장 기초세팅 start -----------------------------------------------
app.config["JWT_COOKIE_SECURE"] = False  # https를 통해서만 cookie가 갈수 있는지
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]  # 토큰을 어디서 찾을지 설정
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)  # 토큰 만료시간 설정 기본은 30분
app.config["JWT_SECRET_KEY"] = "TOYPROJECT16TH"  # 토큰 암호화에 이용되는 히든키로 직접 정의 해주면 된다
# JWTManager에 app을 등록한다
jwt = JWTManager(app)
# jwt 가장 기초세팅 end -------------------------------------------------

@app.route('/')
def home():
    return render_template('landing.html')


# 로그인
@app.route("/login", methods=["POST"])
def login():
    user = request.get_json()
    email = user['email']
    password = user['password']

    one = db.users.find_one({'email': email}, {'_id': False})  # 검색이 됬다면 None은 아닐터

    if one is None:
        return jsonify({"msg": "해당하는 이메일이 존재하지 않습니다"})  # 접근불가 오류

    p = check_password_hash(one['password'],password) # 암호 비교

    if p is not True:
        return jsonify({"msg": "비밀번호가 맞지 않습니다"})  # 불일치 접근 불가

    access_token = create_access_token(identity=email)  # jwt token 생성
    refresh_token = create_refresh_token(identity=email)  # 갱신을 위한 refresh_token 생성
    # 이걸 리턴해서 화면단에서 어떻게 쓰는거지? > 쿠키에 저장한다

    response = jsonify({"msg": "로그인 성공", "login": True})  # resp을 만든이유가 단지 메세지를 위한게 아니라 쿠키를 같이 보내야하기 때문에 만든듯
    set_access_cookies(response, access_token)  # 쿠키에 토큰을 넣어 response 안에 jwt cookie를 넣어 리턴하려고
    set_refresh_cookies(response, refresh_token)  # 쿠키에 토큰을 넣어 response 안에 jwt cookie를 넣어 리턴하려고

    return response, 200  # 서버가 제대로 요청을 처리했다는 성공


@app.route('/signup', methods=['POST'])
def signup():
    # id, password 받아오고 저장
    user_email = request.form['user_email']
    user_pwd = request.form['user_pwd']
    user_nick = request.form['user_nick']
    pw_hash = generate_password_hash(user_pwd)

    # id 중복확인
    if db.user.count_documents({'user_email': user_email}) == 0:
        db.user.insert_one({'user_email': user_email, 'user_pwd': pw_hash, 'user_nick': user_nick})
        return jsonify({'result': 'SUCCESS', 'message': 'SIGN UP SUCCESS'})
    else:
        return jsonify({'result': 'FAIL', 'message': 'user_id already exists'})


# 유효성 검사
@app.route("/protected", methods=["GET"])
@jwt_required(optional=True)  # 토큰이 인정된 (로그인된) 유저만이 이 API를 사용할 수 있다. 유효성 테스트 + optional=true는 분기처리가능
def protected():
    current_user = get_jwt_identity()  # token에 저장된 데이터를 불러온다
    if not current_user:
        return jsonify({"result": "fail"})

    return jsonify({"result": "success", "logged_in_as": current_user})

# 로그아웃
@app.route("/logout", methods=["GET"])
def logout():
    resp = jsonify({"msg": "로그아웃 성공"})
    unset_jwt_cookies(resp)  # 쿠키 없애는
    return resp

# 토큰갱신
@app.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]  # 만료시간을 찍는
        now = datetime.now(timezone.utc)  # 현재시간 기준의 협정 세계시
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))  # 지금 시간으로 부터 30분 추가한 대상시
        if target_timestamp > exp_timestamp:  # 대상시가 만료시간보다 크면
            access_token = create_access_token(identity=get_jwt_identity())  # 다시 토큰을 갱신
            set_access_cookies(response, access_token)  # 갱신한 토큰을 다시 쿠키에 저장
        return response  # 갱신한 토큰이 담긴 쿠키가 있는 response를 반환
    except (RuntimeError, KeyError):
        return response  # 유효하지 않은 jwt라 갱신하지 않고 오리지날을 반환


@app.route("/save", methods=["POST"])
def save_post():
    url_receive = request.form['url_give']
    star_receive = request.form['star_give']
    comment_receive = request.form['comment_give']
    language_receive = request.form['language_give']

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
           'image': image,
           'url': url_receive,
           'language': language_receive
           }
    db.toy.insert_one(doc)

    return jsonify({'msg': '포스팅 완료!'})


@app.route("/show", methods=["GET"])
def show_post():
    all_videos = list(db.toy.find({}, {'_id': False}))
    return jsonify({'videos': all_videos})

@app.route('/<path>')
def get_path(path):
    return render_template(path + '.html')

@app.route('/specific/<path>')
def get_specific_path(path):
    return render_template('specific.html')


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
