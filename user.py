from flask import abort,request,jsonify,Blueprint
import json
from passlib.context import CryptContext
from passlib.hash import sha256_crypt
from dotenv import load_dotenv
import os
from datetime import datetime,timedelta
from jose import jwt
from verify import verify_token
from cache import user_cache,update_user_cache

user_blueprint = Blueprint("user",__name__)

load_dotenv()
data = 'data.json'
users = 'users.json'
pwd_context = CryptContext(schemes=['bcrypt'],deprecated='auto')
SECRET_KEY = os.getenv('secretkey')
ALGORITHM = os.getenv('algo')
exp = 15

@user_blueprint.route('/login',methods=['post'])
def user_login():
    data2 = request.get_json()
    username1 = data2['username']
    password1 = data2['password']
    user_cached = user_cache()

    if_match = next((u for u in user_cached if u['username'] == username1), None)
    if if_match:
        verify_pwd = sha256_crypt.verify(password1, if_match['password'])
        if verify_pwd:
            exp_time = datetime.utcnow() + timedelta(minutes=exp)
            for_payload = {'id':if_match['id'],'username':if_match['username'],'exp':exp_time,'role':if_match['role']}
            token = jwt.encode(for_payload,SECRET_KEY,algorithm=ALGORITHM)
            return jsonify({"token":token,"token_type":"bearer"})
        return jsonify({"message":"wrong password"}),400
    return jsonify({"message":"username not found"}),400

@user_blueprint.route('/view',methods=['get'])
def user_view():
    user_cached = user_cache()
    for_payload = verify_token()

    if not for_payload:
        return jsonify({'message':'token not found'}),404
    if for_payload['role'] != 'admin':
        return jsonify({"message":"no permission"}),403
    users_view = [{'user id':u['id'],'username':u['username'],'user role':u['role']} for u in user_cached]
    return jsonify(users_view),200

@user_blueprint.route('/signup',methods=['post'])
def user_signup():

    for_payload = verify_token()
    if not for_payload:
        return jsonify({'message':'token not found'}),404

    client_request = request.get_json()
    username = client_request['username']
    password = client_request['password']
    role = client_request['role']
    user_cached = user_cache()

    if for_payload['role'] != 'admin':
        return jsonify({"message":"not allowed"}),403

    if_match = next((u for u in user_cached if u['username'] == username),None)

    if if_match:
        return jsonify({"message":"username already exist"}),400

    user_id = max(u['id'] for u in user_cached)+1 if user_cached else 1
    hash_pwd = sha256_crypt.hash(password)
    if role not in ['admin','user']:
        return jsonify({'message':'invalid role, choose admin or user'}),400
    new_user = {'id':user_id,'username':username,'password':hash_pwd,'role':role}
    user_cached.append(new_user)
    update_user_cache(user_cached)
    return jsonify({"message":"successfully added"}),201

@user_blueprint.route('/delete',methods=['post'])
def user_delete():
    for_payload = verify_token()
    user_cached = user_cache()

    if not for_payload:
        return jsonify({'message':'token not found'}),401
    if for_payload['role'] != 'admin':
        return jsonify({"message":"invalid"}),403

    client_request = request.get_json()
    id = client_request['id']

    if_match = next((u for u in user_cached if u['id'] == id),None)
    if not if_match:
        return jsonify({'message':'user id not found'}),404
    user_cached.remove(if_match)
    update_user_cache(user_cached)
    return jsonify({'message':'successfully deleted'})
