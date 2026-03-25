from flask import abort,request,jsonify,Blueprint
import json
from passlib.context import CryptContext
from passlib.hash import sha256_crypt
from dotenv import load_dotenv
import os
from datetime import datetime,timedelta
from jose import jwt
from verify import verify_token


user_blueprint = Blueprint("user",__name__)

load_dotenv()
data = 'data.json'
users = 'users.json'
pwd_context = CryptContext(schemes=['bcrypt'],deprecated='auto')
SECRET_KEY = os.getenv('secretkey')
ALGORITHM = os.getenv('algo')
exp = 15

def create_admin():
    password = os.getenv('adminpwd')
    hash_pwd = sha256_crypt.hash(password)
    try:
        user_list = []
        with open(users,'r') as f:
            user_list=json.load(f)
        if len(user_list) == 0:
            default_login = {'id':1,'username':'admin','password':hash_pwd,'role':'admin'}
            user_list.append(default_login)
            with open(users, 'w') as f:
                json.dump(user_list,f,indent=4)
    except FileNotFoundError:
        abort(404,description='json not found')
    except json.JSONDecodeError:
        abort(500,description='invalid json file')


@user_blueprint.route('/login',methods=['post'])
def user_login():
    data2 = request.get_json()
    username1 = data2['username']
    password1 = data2['password']
    try:
        user_list = []
        with open(users,'r') as f:
            user_list = json.load(f)
        if_match = next((u for u in user_list if u['username'] == username1), None)
        if if_match:
            verify_pwd = sha256_crypt.verify(password1, if_match['password'])
            if verify_pwd:
                exp_time = datetime.utcnow() + timedelta(minutes=exp)
                for_payload = {'id':if_match['id'],'username':if_match['username'],'exp':exp_time,'role':if_match['role']}
                token = jwt.encode(for_payload,SECRET_KEY,algorithm=ALGORITHM)
                return jsonify({"token":token,"token_type":"bearer"})
            return jsonify({"message":"wrong password"}),400
        return jsonify({"message":"username not found"}),400
    except FileNotFoundError:
        abort(404,description='json not found')
    except json.JSONDecodeError:
        abort(500,description='invalid json file')

@user_blueprint.route('/signup',methods=['post'])
def user_signup():

    for_payload = verify_token()
    if not for_payload:
        return jsonify({'message':'token not found'}),404
    if for_payload['role'] != 'admin':
        return jsonify({"message":"invalid"}),403

    client_request = request.get_json()
    username = client_request['username']
    password = client_request['password']
    role = client_request['role']

    users_list = []
    try:
        with open(users,'r') as f:
            users_list = json.load(f)
    except FileNotFoundError:
        abort(404,description='json not found')
    except json.JSONDecodeError:
        abort(500,description='invalid json file')
    if_match = next((u for u in users_list if u['username'] == username),None)

    if if_match:
        return jsonify({"message":"username already exist"}),400

    user_id = max(u['id'] for u in users_list)+1 if users_list else 1
    hash_pwd = sha256_crypt.hash(password)
    if role not in ['admin','user']:
        return jsonify({'message':'invalid role, choose admin or user'}),400
    new_user = {'id':user_id,'username':username,'password':hash_pwd,'role':role}
    users_list.append(new_user)
    with open(users,'w') as f:
        json.dump(users_list,f,indent=4)
    return jsonify("successfully added"),201

@user_blueprint.route('/delete',methods=['post'])
def user_delete():
    pass

