from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
# Initialize CORS cleanly for all routes
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/admin/update-token', methods=['POST', 'OPTIONS'])
def update_token():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200

    global current_token
    data = request.json or {}
    new_token = data.get("current_token")
    if new_token is not None:
        try:
            current_token = int(new_token)
            return jsonify({"success": True, "token": current_token})
        except ValueError:
            return jsonify({"success": False, "message": "Invalid token format"}), 400
            
    return jsonify({"success": True, "token": current_token})


@app.after_request
def after_request(response):
    # Set headers directly instead of add() to prevent duplicate CORS header values
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET,PUT,POST,DELETE,OPTIONS'
    return response

# In-memory storage
seats = {"available_seats": 20, "total_seats": 100}
token_counter = 100
current_token = 100
orders = []

menu_data = [
    {"id": 1, "name": "Burger", "price": 120},
    {"id": 2, "name": "Pizza", "price": 250},
    {"id": 3, "name": "Fries", "price": 80},
    {"id": 4, "name": "Egg Noodles", "price": 100},
    {"id": 5, "name": "Water Bottle", "price": 20},
    {"id": 6, "name": "Ice Cream", "price": 50},
    {"id": 7, "name": "Lays", "price": 20},
    {"id": 8, "name": "Dairy Milk", "price": 40},
    {"id": 9, "name": "Thumbs Up", "price": 30},
    {"id": 10, "name": "Biscuits", "price": 25}
]

@app.route('/')
def home():
    return jsonify({"status": "QuickBitezzz Backend Running"})

@app.route('/menu', methods=['GET', 'OPTIONS'])
def get_menu():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200
    return jsonify(menu_data)

@app.route('/seats', methods=['GET', 'POST', 'OPTIONS'])
def manage_seats():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200

    global seats
    if request.method == 'POST':
        data = request.get_json() or {}
        new_avail = data.get('available_seats')
        new_total = data.get('total_seats')
        
        if new_avail is not None:
            seats['available_seats'] = int(new_avail)
        if new_total is not None:
            seats['total_seats'] = int(new_total)
            
        return jsonify(seats)
    return jsonify(seats)

@app.route('/current-token', methods=['GET', 'OPTIONS'])
def get_current_token():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200
    return jsonify({"current_token": current_token})

@app.route('/order', methods=['POST', 'OPTIONS'])
def place_order():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200

    global token_counter, seats, orders
    data = request.get_json() or {}
    
    token_counter += 1
    new_order_id = len(orders) + 1
    
    items = data.get("items") or data.get("item") or []
    total = data.get("total", 0)
    
    order = {
        "order_id": new_order_id,
        "token_number": token_counter,
        "items": items,
        "total_amount": total,
        "payment_status": data.get("payment_status", "Paid"),
        "payment_method": data.get("payment_method", "UPI"),
        "status": "Preparing Your Order"
    }
    
    orders.append(order)
    
    if seats["available_seats"] > 0:
        seats["available_seats"] -= 1
        
    return jsonify({"message": "Order placed successfully", "order": order})

@app.route('/status/<int:order_id>', methods=['GET', 'OPTIONS'])
def get_order_status(order_id):
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200

    order = next((o for o in orders if int(o.get("order_id", 0)) == int(order_id)), None)
    if order:
        return jsonify({
            "order_id": order["order_id"],
            "token_number": order["token_number"],
            "status": order["status"],
            "seats_left": seats["available_seats"],
            "total_amount": order["total_amount"]
        })
    return jsonify({"message": "Order not found"}), 404

@app.route('/admin/orders', methods=['GET', 'OPTIONS'])
def get_admin_orders():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200
    return jsonify(orders)

@app.route('/admin/update-status/<int:order_id>', methods=['POST', 'PUT', 'OPTIONS'])
def update_order_status(order_id):
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200

    global current_token
    data = request.get_json() or {}
    new_status = data.get("status")
    
    order = next((o for o in orders if int(o.get("order_id", 0)) == int(order_id)), None)
    if order:
        order["status"] = new_status
        if new_status in ["Your Order is Ready", "Preparing Your Order"]:
            current_token = order["token_number"]
        return jsonify({"success": True, "order": order})
    return jsonify({"success": False, "message": "Order not found"}), 404

@app.route('/admin/delete-order/<int:order_id>', methods=['POST', 'DELETE', 'OPTIONS'])
def admin_delete_order(order_id):
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200

    global orders
    initial_count = len(orders)
    orders = [o for o in orders if int(o.get("order_id", 0)) != int(order_id)]
    
    if len(orders) < initial_count:
        return jsonify({"success": True, "message": "Order removed successfully"}), 200
    else:
        return jsonify({"success": False, "message": "Order not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
