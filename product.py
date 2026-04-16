from flask import abort,Blueprint,jsonify,request
from verify import verify_token
import json
from cache import product_cache
from order import save_order,view_order,get_grandtotal
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
    if not for_payload:
        return jsonify({'message':'token not found'}),404

    client_request = request.get_json()
    product_id = client_request['product_id']
    quantity = client_request['quantity']
    if not client_request:
        return jsonify({'message':'invalid request'}),400

    product_cached = product_cache()
    if_match = next((p for p in product_cached if product_id == p['id']),None)
    if not if_match:
        return jsonify({'message':'product id not found'})

    # grand_total = get_grandtotal()

    view_ordered = view_order()
    total_item_price = quantity * if_match['price']
    if not view_ordered:
        new_items = {"product_id": product_id, "item": if_match['items'], "quantity": quantity,
                     "price": if_match['price'],
                     "total": total_item_price}
        new_order = {"order_id": len(view_ordered) + 1, "user_id": for_payload['id'], "items": [new_items],
                     "grand_total": total_item_price}
        view_ordered.append(new_order)
        save_order(view_ordered)
        return jsonify({'message':'successfully added'})
    get_ordered = next((v for v in view_ordered if for_payload['id'] == v['user_id']),None)
    if not get_ordered:
        return jsonify({'message':'user id not found'})
    get_item = next((g for g in get_ordered['items'] if product_id == g['product_id']),None)
    get_item2 = [g['total'] for g in get_ordered['items']]
    new_items = {"product_id":product_id,"item":if_match['items'],"quantity":quantity,"price":if_match['price'],"total":total_item_price}
    get_ordered['items'].append(new_items)
    grand_total = sum(get_item2) + total_item_price
    get_ordered['grand_total'] = grand_total
    # print(grand_total)
    # print(sum(get_item2) + total_item_price)
    save_order(view_ordered)
    return jsonify({'message':'successfully added'})
    #grand total not exact, last total order not counted - FIXED
@product_blueprint.route('/view_order',methods=['GET'])
def view_orders():
    view_ordered = view_order()
    if not view_ordered:
        return jsonify({'message':'no order'})
    return jsonify(view_ordered)

@product_blueprint.route('/update_order',methods=['POST'])
def update_orders():
    get_payload = verify_token()
    if not get_payload:
        return jsonify({'message':'token not found'}),401
    client_request = request.get_json()
    product_id = client_request['product_id']
    quantity = client_request['quantity']
    if not client_request:
        return jsonify({'message':'invalid request'}),400
    ordered = view_order()
    order_querry = next((o for o in ordered if o['user_id'] == get_payload['id']),None)
    item_querry = next((o for o in order_querry['items'] if product_id == o['product_id']),None)
    if not order_querry:
        return jsonify({'message':'order id not found'})
    if not item_querry:
        return jsonify({'message':'product id not found'}),404
    item_querry['quantity'] = quantity
    new_total = quantity * item_querry['price']
    item_querry['total'] = new_total

    save_order(ordered)
    return jsonify({'message':'successfully updated'})

#TO BE CONTINUE: FIX [0] LIST QUERRY, NO GRANDTOTAL YET ON ORDER.PY





