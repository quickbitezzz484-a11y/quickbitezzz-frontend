from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)

# Enable CORS globally for all routes
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# Add CORS headers to all responses (including 404/405 errors)
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

# Global preflight handler returning 200 OK for OPTIONS
@app.before_request
def handle_options():
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200
