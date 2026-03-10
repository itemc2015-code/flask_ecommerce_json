from flask import Flask,abort,request,jsonify
import json
from passlib.context import CryptContext
from passlib.hash import sha256_crypt

app = Flask(__name__)
data = 'data.json'
users = 'users.json'
pwd_context = CryptContext(schemes=['bcrypt'],deprecated='auto')

def create_admin():
    password = '1234'
    hash_pwd = sha256_crypt.hash(password)
    user_list = []
    with open(users,'r') as f:
        user_list=json.load(f)
    if len(user_list) == 0:
        default_login = {'id':1,'username':'admin','password':hash_pwd}
        user_list.append(default_login)
        with open(users, 'w') as f:
            json.dump(user_list,f,indent=4)

@app.before_first_request
def startup_event():
    create_admin()

@app.route('/',methods=['GET'])
def view_products():
    try:
        with open(data,'r') as f:
            load_data=json.load(f)
        return load_data
    except FileNotFoundError:
        abort(404)
    except json.JSONDecodeError:
        abort(500)

@app.route('/login',methods=['post'])
def user_login():
    data2 = request.get_json()
    username1 = data2['username']
    password1 = data2['password']
    user_list = []
    with open(users,'r') as f:
        user_list = json.load(f)
    if_match = next((u for u in user_list if u['username'] == username1),None)
    if if_match:
        verify_pwd = sha256_crypt.verify(password1,if_match['password'])
        if verify_pwd:
            return jsonify({"message":"login successfully"})
    abort(404,description='not found')


if __name__ == '__main__':
    app.run(debug=True)

'''
next:
allow admin for signup and view 
'''