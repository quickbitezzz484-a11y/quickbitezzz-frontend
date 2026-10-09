import random
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)

# Full CORS configuration for all routes and preflight checks
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

# Global OPTIONS preflight handler
@app.before_request
def handle_options():
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200

# Application In-Memory State
TOTAL_SEATS = 50
occupied_seats = 0
current_token = 1
token_counter = 100

menu_items = [
    {"id": 1, "name": "Burger", "price": 80},
    {"id": 2, "name": "Pizza", "price": 150},
    {"id": 3, "name": "Fries", "price": 60},
    {"id": 4, "name": "Egg Noodles", "price": 90},
    {"id": 5, "name": "Water Bottle", "price": 20},
    {"id": 6, "name": "Ice Cream", "price": 40},
    {"id": 7, "name": "Lays", "price": 20},
    {"id": 8, "name": "Dairy Milk", "price": 50},
    {"id": 9, "name": "Thumbs Up", "price": 30},
    {"id": 10, "name": "Biscuits", "price": 25}
]

orders = {}

@app.route('/')
def home():
    return jsonify({"message": "QuickBitezzz Backend Active API"})

# --- SEATS ENDPOINTS ---
@app.route('/seats', methods=['GET', 'POST', 'OPTIONS'])
def handle_seats():
    global occupied_seats, TOTAL_SEATS
    if request.method == 'POST':
        data = request.json or {}
        if 'available_seats' in data:
            occupied_seats = max(0, TOTAL_SEATS - int(data['available_seats']))
        if 'total_seats' in data:
            TOTAL_SEATS = int(data['total_seats'])
        return jsonify({"success": True, "available_seats": max(0, TOTAL_SEATS - occupied_seats), "total_seats": TOTAL_SEATS})
    
    available = max(0, TOTAL_SEATS - occupied_seats)
    return jsonify({
        "total_seats": TOTAL_SEATS,
        "occupied_seats": occupied_seats,
        "available_seats": available
    })

# --- TOKEN ENDPOINTS ---
@app.route('/current-token', methods=['GET'])
def get_current_token():
    return jsonify({"current_token": current_token})

@app.route('/admin/next-token', methods=['POST', 'OPTIONS'])
def next_token():
    global current_token
    current_token += 1
    return jsonify({"message": "Token incremented", "current_token": current_token})

@app.route('/admin/set-token', methods=['POST', 'OPTIONS'])
def set_token():
    global current_token
    data = request.json or {}
    token_val = data.get("token") or data.get("current_token")
    
    if token_val is not None:
        try:
            current_token = int(token_val)
            return jsonify({"message": "Token set", "current_token": current_token})
        except ValueError:
            return jsonify({"message": "Invalid token value"}), 400
            
    return jsonify({"message": "Token value required"}), 400

# --- MENU ENDPOINT ---
@app.route('/menu', methods=['GET'])
def get_menu():
    return jsonify(menu_items)

# --- ORDER ENDPOINTS ---
@app.route('/order', methods=['POST', 'OPTIONS'])
def place_order():
    global occupied_seats, token_counter
    data = request.json or {}

    order_id = f"ORD{random.randint(1000, 9999)}"
    token_counter += 1
    assigned_token = token_counter

    if occupied_seats < TOTAL_SEATS:
        occupied_seats += 1

    order_items = data.get("items") or data.get("item") or []

    new_order = {
        "order_id": order_id,
        "token_number": assigned_token,
        "items": order_items,
        "total_amount": data.get("total", 0),
        "payment_status": data.get("payment_status", "Paid"),
        "payment_method": data.get("payment_method", "UPI"),
        "roll_no": data.get("roll_no", ""),
        "student_name": data.get("student_name", ""),
        "status": "Preparing Your Order",
        "seats_left": max(0, TOTAL_SEATS - occupied_seats)
    }

    orders[order_id] = new_order
    return jsonify({"message": "Order placed successfully", "order": new_order}), 201

@app.route('/status/<order_id>', methods=['GET'])
def get_status(order_id):
    order_info = None
    for k, v in orders.items():
        if str(k) == str(order_id):
            order_info = v
            break
            
    if not order_info:
        return jsonify({"message": "Order not found"}), 404
    
    order_info["seats_left"] = max(0, TOTAL_SEATS - occupied_seats)
    return jsonify(order_info)

# --- ADMIN ENDPOINTS ---
@app.route('/admin/orders', methods=['GET'])
def get_admin_orders():
    return jsonify(list(orders.values()))

@app.route('/admin/update-status/<order_id>', methods=['POST', 'PUT', 'OPTIONS'])
def update_status(order_id):
    global occupied_seats
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200

    data = request.json or {}
    new_status = data.get("status")

    matched_key = None
    for k in orders.keys():
        if str(k) == str(order_id):
            matched_key = k
            break

    if matched_key:
        orders[matched_key]["status"] = new_status
        if new_status and "ready" in new_status.lower() and occupied_seats > 0:
            occupied_seats -= 1
        return jsonify({"message": "Status updated", "order": orders[matched_key]})
    
    return jsonify({"message": "Order not found"}), 404

@app.route('/admin/delete-order/<order_id>', methods=['DELETE', 'POST', 'OPTIONS'])
def delete_order(order_id):
    global orders
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200

    matched_key = None
    for k in orders.keys():
        if str(k) == str(order_id):
            matched_key = k
            break

    if matched_key:
        del orders[matched_key]
        return jsonify({"message": "Order deleted"})
    return jsonify({"message": "Order not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
