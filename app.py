from flask import Flask
from product import product_blueprint
from user import user_blueprint
# from user import create_admin, user_blueprint
from cache import user_cache,update_user_cache
import  os
from passlib.hash import sha256_crypt

app = Flask(__name__)

app.register_blueprint(product_blueprint,url_prefix='/product')
app.register_blueprint(user_blueprint,url_prefix='/user')

def create_admin():
    user_cached = user_cache()
    password = os.getenv('adminpwd')
    hash_pwd = sha256_crypt.hash(password)
    if len(user_cached) == 0:
        default_login = {'id':1,'username':'admin','password':hash_pwd,'role':'admin'}
        user_cached.append(default_login)
        update_user_cache(user_cached)

@app.before_first_request
def startup_event():
    create_admin()

if __name__ == '__main__':
    app.run(debug=True)

'''
#admin update username
#create cache and apply to all
#don't display user password on view users

ongoing:
normal users, create,view,update,delete order
'''