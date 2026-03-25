from flask import abort
import json

users = 'users.json'
data = 'data.json'

def user_cache():
    try:
        with open(users,'r') as f:
            user_list = json.load(f)
            return user_list
    except FileNotFoundError:
        return abort(404,description='json not found')
    except json.JSONDecodeError:
        return abort(500,description='invalid json file')

def update_user_cache(user_update):
    try:
        with open(users,'w') as f:
            json.dump(user_update,f,indent=4)
            user_cache = user_update
    except FileNotFoundError:
        return abort(404,description='json not found')
    except json.JSONDecodeError:
        return abort(500,description='invalid json file')