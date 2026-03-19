from flask import abort,Blueprint,jsonify
from verify import verify_token
import json

product_blueprint = Blueprint("products",__name__)

data = 'data.json'

@product_blueprint.route('/',methods=['GET'])
def view_products():
    verify_token()
    try:
        with open(data,'r') as f:
            load_data=json.load(f)
        return jsonify(load_data)
    except FileNotFoundError:
        abort(404, description='json not found')
    except json.JSONDecodeError:
        abort(500, description='invalid json file')
