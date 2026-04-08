from flask import abort,Blueprint,jsonify,request
from verify import verify_token
import json
from cache import product_cache
from order import save_order,view_order
from model import Product

product_blueprint = Blueprint("products",__name__)

data = 'data.json'

@product_blueprint.route('/',methods=['GET'])
def view_products():
    for_payload = verify_token()
    product_cached = product_cache()

    if not for_payload:
        return jsonify({'message':'token not found'}),404
    return jsonify(product_cached),200

@product_blueprint.route('/request_order',methods=['POST'])
def order_request():
    for_payload = verify_token()
    product_cached = product_cache()
    client_request = request.get_json()
    view_ordered = view_order()
    product_id = client_request['product_id']
    quantity = client_request['quantity']

    ordered = [v for v in view_ordered]
    if_match = next((p for p in product_cached if product_id == p['id']),None)
    check_product_id = next((p for p in ordered[0]['items'] if product_id == p['product_id']),None)

    if not for_payload:
        return jsonify({'message':'token not found'}),404
    if not client_request:
        return jsonify({'message':'invalid request'}),400
    if not if_match:
        return jsonify({'message':'product id not found'})
    total_item_price = quantity * if_match['price']

    if len(ordered) == 0:
        new_items = {"product_id": product_id, "item": if_match['items'], "quantity": quantity,"price":if_match['price'],
                     "total": total_item_price}
        new_order = {"order_id":len(view_ordered)+1,"user_id":for_payload['id'],"items":[new_items]}
        ordered.append(new_order)
        save_order(ordered)
        return jsonify({'message':'successfully added'})
    if check_product_id:
        return jsonify({'message':'product already added, go to update'}),400
    new_items = {"product_id":product_id,"item":if_match['items'],"quantity":quantity,"price":if_match['price'],"total":total_item_price}
    ordered[0]['items'].append(new_items)
    save_order(ordered)
    # print(check_product_id)
    return jsonify({'message':'successfully added'})
#ITEMS HAS DUPLICATED



