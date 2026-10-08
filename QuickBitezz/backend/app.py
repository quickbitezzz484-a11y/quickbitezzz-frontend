from flask import Flask, request, jsonify
from flask_cors import CORS
import threading
import time

app = Flask(__name__)
CORS(app)

current_serving_token = 100

valid_students = [
    {"name": "Jaideep", "roll_no": "25K91A66P9", "password": "JaideepP9"},
    {"name": "Rahul", "roll_no": "25K91A66P8", "password": "RahulP8"},
    {"name": "Ananya", "roll_no": "25K91A66P7", "password": "AnanyaP7"}
]

orders = []
TOTAL_SEATS = 150
available_seats = TOTAL_SEATS

@app.route('/')
def home():
    return "QuickBitezzz Backend Running 🚀"


@app.route('/menu', methods=['GET'])
def menu():
    food_menu = [
        {"id": 1, "name": "Burger", "price": 99},
        {"id": 2, "name": "Pizza", "price": 149},
        {"id": 3, "name": "Fries", "price": 49},
        {"id": 4, "name": "Egg Noodles", "price": 60},
        {"id": 5, "name": "Lays", "price": 20},
        {"id": 6, "name": "Water Bottle", "price": 20},
        {"id": 7, "name": "Ice Cream", "price": 50},
        {"id": 8, "name": "Biscuits", "price": 20},
        {"id": 9, "name": "Dairy Milk", "price": 20},
        {"id": 10, "name": "Thumbs Up", "price": 20}
    ]
    return jsonify(food_menu)

def update_status(order):
    print("Started status thread for order", order["order_id"])

    
    order["status"] = "Almost Ready!!!"
    print("Order", order["order_id"], "-> Ready")

    
    order["status"] = "Your Order is Ready"
    print("Order", order["order_id"], "-> Delivered")

@app.route('/order', methods=['POST'])
def place_order():
    global available_seats

    data = request.json

    if available_seats <= 0:
        return jsonify({
            "message": "No seats available",
            "error": True
        }), 400

    order = {
        "order_id": len(orders) + 1,
        "token_number": len(orders) + 101,
        "items": data.get("item", []),
        "total_amount": data.get("total", 0),
        "payment_status": data.get("payment_status", "Pending"),
        "payment_method": data.get("payment_method", "N/A"),
        "status": "Preparing",
        "seats_left": available_seats -1
    }

    orders.append(order)
    available_seats -= 1

    threading.Thread(target=update_status, args=(order,), daemon=True).start()

    return jsonify({
        "message": "Order placed successfully!",
        "order": order,
        "available_seats": available_seats
    })

@app.route('/status/<int:order_id>', methods=['GET'])
def check_status(order_id):
    for order in orders:
        if order["order_id"] == order_id:
            return jsonify(order)
    return jsonify({"error": "Order not found"}), 404

@app.route('/orders', methods=['GET'])
def get_orders():
    return jsonify(orders)

@app.route('/seats', methods=['GET'])
def get_seats():
    return jsonify({
        "total_seats": TOTAL_SEATS,
        "available_seats": available_seats
    })

@app.route('/login', methods=['POST'])
def login():
    data = request.json

    name = data.get("name", "").strip()
    roll_no = data.get("roll_no", "").strip()
    password = data.get("password", "").strip()

    if not name or not roll_no or not password:
        return jsonify({
            "success": False,
            "message": "Name, Roll Number and Password are required."
        }), 400

    for student in valid_students:
    
     if (
        student["name"].lower() == name.lower() and
        student["roll_no"] == roll_no and
        student["password"] == password
    ):
        return jsonify({
            "success": True,
            "message": "Login successful",
            "user": {
                "name": student["name"],
                "roll_no": student["roll_no"]
            }
        })

    return jsonify({
        "success": False,
        "message": "Invalid login details."
    }), 401

@app.route('/admin/update-status/<int:order_id>', methods=['PUT'])
def admin_update_status(order_id):
    data = request.json
    new_status = data.get("status", "").strip()

    for order in orders:
        if order["order_id"] == order_id:
            order["status"] = new_status
            return jsonify({
                "success": True,
                "message": "Status updated successfully",
                "order": order
            })

    return jsonify({
        "success": False,
        "message": "Order not found"
    }), 404

@app.route('/current-token', methods=['GET'])
def get_current_token():
    return jsonify({
        "current_token": current_serving_token
    })

@app.route('/admin/update-token/<int:token>', methods=['PUT'])
def update_token(token):
    global current_serving_token
    current_serving_token = token

    return jsonify({
        "success": True,
        "message": "Current token updated",
        "current_token": current_serving_token
    })

@app.route('/admin/update-seats/<int:seats>', methods=['PUT'])
def update_seats(seats):
    global available_seats
    available_seats = seats

    return jsonify({
        "success": True,
        "message": "Available seats updated",
        "available_seats": available_seats,
        "total_seats": TOTAL_SEATS
    })

@app.route('/admin/increase-seats', methods=['PUT'])
def increase_seats():
    global available_seats, TOTAL_SEATS

    if available_seats < TOTAL_SEATS:
        available_seats += 1

    return jsonify({
        "success": True,
        "available_seats": available_seats,
        "total_seats": TOTAL_SEATS
    })

@app.route('/admin/decrease-seats', methods=['PUT'])
def decrease_seats():
    global available_seats

    if available_seats > 0:
        available_seats -= 1

    return jsonify({
        "success": True,
        "available_seats": available_seats,
        "total_seats": TOTAL_SEATS
    })



if __name__ == '__main__':
    app.run(debug=False)
