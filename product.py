from flask import abort,Blueprint,jsonify
from verify import verify_token
import json
from cache import product_cache

product_blueprint = Blueprint("products",__name__)

data = 'data.json'

@product_blueprint.route('/',methods=['GET'])
def view_products():
    for_payload = verify_token()
    product_cached = product_cache()
    if not for_payload:
        return jsonify({'message':'token not found'}),404
    return jsonify(product_cached),200

