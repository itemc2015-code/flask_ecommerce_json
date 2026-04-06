from flask import request,jsonify,Blueprint
# from passlib.context import CryptContext
from passlib.hash import sha256_crypt
from dotenv import load_dotenv
import os
from datetime import datetime,timedelta
from jose import jwt
from verify import verify_token
from cache import user_cache,update_user_cache
from model import Users
from pydantic import ValidationError

user_blueprint = Blueprint("user",__name__)

load_dotenv()
data = 'data.json'
users = 'users.json'
# pwd_context = CryptContext(schemes=['bcrypt'],deprecated='auto')
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

    client_request = request.get_json()
    id = client_request['id']

    if not for_payload:
        return jsonify({'message':'token not found'}),401
    if for_payload['role'] == 'admin':
        if_match = next((u for u in user_cached if u['id'] == id), None)
        if not if_match:
            return jsonify({'message': 'user id not found'}), 404
        user_cached.remove(if_match)
        update_user_cache(user_cached)
        return jsonify({'message': 'successfully deleted'}),200
    return jsonify({"message":"not allowed"}),403

@user_blueprint.route('/update_pwd',methods=['post'])
def update_password():
    try:
        for_payload = verify_token()
        if not for_payload:
            return jsonify({'message':'token not found'}),401

        if for_payload['role'] != 'admin':
            return jsonify({'message': 'no permission'}), 403

        user_cached = user_cache()
        client_request = request.get_json()
        if not client_request:
            return jsonify({'message':'invalid request'}),400

        if not for_payload['username']:
            return jsonify({'message':'username not found'}),404

        try:
            data = Users(**client_request)
        except ValidationError as e:
            return jsonify({'message': e.errors()}),400

        user_id = data.id
        user_password = data.password

        # if not user_id:
        #     return jsonify({'message':'id cannot be blank'}),400
        # if not user_password:
        #     return jsonify({'message':'password is required'}),400

        if_match = next((u for u in user_cached if user_id == u['id']), None)

        if not if_match:
            return jsonify({'message': 'user id not found'}), 401

        new_pwd = sha256_crypt.hash(user_password)
        if_match['password'] = new_pwd
        update_user_cache(user_cached)
        return jsonify({'message': 'successfully updated'}),200
    except Exception as e:
        print(f'server error {str(e)}')
        return jsonify({'error message':'server error'}),500


