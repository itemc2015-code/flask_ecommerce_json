from flask import jsonify
import json

orders = 'order.json'

def view_order():
    try:
        with open(orders,'r') as f:
            view_orders=json.load(f)
            if  len(view_orders) == 0:
                return []
            return view_orders
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

def save_order(ordered):
    try:
        with open(orders,'w') as f:
            json.dump(ordered,f,indent=4)
    except FileNotFoundError:
        return jsonify({'message':'json file not found'}),404
    except json.JSONDecodeError:
        return jsonify({'message':'invalid json file'}),500

def get_grandtotal():
    try:
        with open(orders,'r') as f:
            view_ordered = json.load(f)
        if not view_ordered:
            return jsonify({'message':'empty order'})
        ordered_list = [v for v in view_ordered]
        get_gtotal = sum(ordered_list['grand_total'])
        return get_gtotal
    except FileNotFoundError:
        return jsonify({'message':'json file not found'}),404
    except json.JSONDecodeError:
        return jsonify({'message':'invalid json file'}),500


