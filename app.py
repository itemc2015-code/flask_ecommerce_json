from flask import Flask
from product import product_blueprint
from user import create_admin, user_blueprint

app = Flask(__name__)

app.register_blueprint(product_blueprint,url_prefix='/product')
app.register_blueprint(user_blueprint,url_prefix='/user')

@app.before_first_request
def startup_event():
    create_admin()

if __name__ == '__main__':
    app.run(debug=True)

'''
next:
admin delete,update username
normal users, create,view,update,delete order
create cache
admin endpoint is separate 
'''