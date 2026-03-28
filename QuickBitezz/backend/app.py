from flask import Flask, request, jsonify
from flask_cors import CORS
import threading
import time


app = Flask(__name__)
CORS(app)


current_serving_token = 100

valid_students = [
    {"name": "Jaideep", "roll_no": "25K91A66P9"},
    {"name": "Rahul", "roll_no": "25K91A66P8"},
    {"name": "Ananya", "roll_no": "25K91A66P7"}
]





orders = []
TOTAL_SEATS = 20
available_seats = TOTAL_SEATS



@app.route('/')
def home():
    return "QuickBitezzz Backend Running 🚀"

@app.route('/menu', methods=['GET'])
def menu():
    food_menu = [
        {"id": 1, "name": "Burger", "price": 100},
        {"id": 2, "name": "Pizza", "price": 150},
        {"id": 3, "name": "Fries", "price": 70}
    ]
    return jsonify(food_menu)

def update_status(order):
    print("Started status thread for order", order["order_id"])
    
    order["status"] = "Ready Avuthundhi Chill macha"
    print("Order", order["order_id"], "-> Out for Delivery")

    
    order["status"] = "Ochi Tini Poo"
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
        "items": data.get("item"),
        "total_amount": data.get("total"),
        "payment_status": data.get("payment_status", "Pending"),
        "status": "Preparing",
        "seats_left": available_seats - 1
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


valid_students = [
    {"name": "Jaideep", "roll_no": "25K91A66P9"},
    {"name": "Rahul", "roll_no": "25K91A66P8"},
    {"name": "Ananya", "roll_no": "25K91A66P7"}
]

@app.route('/login', methods=['POST'])
def login():
    data = request.json

    name = data.get("name", "").strip()
    roll_no = data.get("roll_no", "").strip()

    if not name or not roll_no:
        return jsonify({
            "success": False,
            "message": "Name and Roll Number are required."
        }), 400

    for student in valid_students:
        if student["name"].lower() == name.lower() and student["roll_no"] == roll_no:
            return jsonify({
                "success": True,
                "message": "Login successful",
                "user": student
            })

    return jsonify({
        "success": False,
        "message": "Invalid college details."
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

if __name__ == '__main__':
    app.run(debug=False)
