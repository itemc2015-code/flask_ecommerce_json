from flask import request,abort
from jose import jwt
from dotenv import load_dotenv
import os

load_dotenv()
SECRET_KEY = os.getenv('secretkey')
ALGORITHM = os.getenv('algo')

def get_token():
    auth = request.headers.get("Authorization")

    if not auth:
        abort(401,description="missing authorizaton header")
    try:
        token = auth.split()[1]
        return token
    except:
        abort(401,description="invalid authorization header")

def verify_token():
    token = get_token()
    payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
    return payload