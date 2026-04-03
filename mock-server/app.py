from flask import Flask, jsonify, request
import json
import os

app = Flask(__name__)

def load_customers():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(base_dir, 'data', 'customers.json')
    try:
        with open(json_path, 'r') as f:
            return json.load(f) 
    except FileNotFoundError:
        print(f"Json file path not found : {json_path}")

@app.get("/api/health")
def get_health():
    return jsonify({
        "status": "ok",
        "service": "mock-server",
        "port": 5000
    }), 200

@app.get("/api/customers")
def get_customers():
    customer_data = load_customers()

    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)

    start = (page - 1) * limit
    end = start + limit
    pagination = customer_data[start:end]

    return jsonify({
        "data" : pagination,
        "total" : len(customer_data),
        "page" : page,
        "limit" : limit
    }), 200

@app.get("/api/customers/<customer_id>")
def get_customer(customer_id):
    customer_data = load_customers()

    customer = next((c for c in customer_data if c["customer_id"] == customer_id), None)

    if not customer:
        return jsonify({"error": f"Customer {customer_id} not found"}), 404
    
    return jsonify(customer), 200