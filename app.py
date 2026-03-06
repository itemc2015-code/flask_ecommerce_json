from flask import Flask,abort
import json
from passlib.context import CryptContext

app = Flask(__name__)
data = 'data.json'
users = 'users.json'
pwd_context = CryptContext(schemes=['bcrypt'],deprecated='auto')

def create_admin():
    password = 'admin1234'
    hash_pwd = pwd_context.hash(password)
    with open(users,'r') as f:
        user_list=json.load(f)
    if len(user_list) == 0:
        default_login = {'id':1,'username':'admin','password':hash_pwd}
        with open(users, 'w') as f:
            json.dump(default_login,f,indent=4)

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


if __name__ == '__main__':
    app.run(debug=True)