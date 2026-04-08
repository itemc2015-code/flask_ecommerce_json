from flask import jsonify
import json

orders = 'order.json'

def view_order():
    try:
        with open(orders,'r') as f:
            view_orders=json.load(f)
            return view_orders
    except FileNotFoundError:
        return jsonify({'message':'json file not found'}),404
    except json.JSONDecodeError:
        return jsonify({'message':'invalid json file'}),500

def save_order(ordered):
    try:
        with open(orders,'w') as f:
            json.dump(ordered,f,indent=4)
    except FileNotFoundError:
        return jsonify({'message':'json file not found'}),404
    except json.JSONDecodeError:
        return jsonify({'message':'invalid json file'}),500


