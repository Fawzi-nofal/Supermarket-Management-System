# app.py - Flask API Server (Flask 3 compatible)
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask.json.provider import DefaultJSONProvider
from datetime import datetime
import json
from bson import ObjectId

# Import your existing modules
from customers import (
    ensure_customers_indexes, create_customer, get_all_customers,
    update_customer, delete_customer, get_customer_by_id
)
from products import (
    ensure_products_indexes, create_product, get_all_products,
    update_product, delete_product, get_product_by_id
)
from orders import (
    ensure_orders_indexes, create_order, get_order_by_id, list_orders,
    update_order, delete_order, total_revenue, top_customers, top_products
)

# ---------------- JSON Provider (replaces app.json_encoder) ----------------
class CustomJSONProvider(DefaultJSONProvider):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, ObjectId):
            return str(obj)
        return super().default(obj)

app = Flask(__name__)
app.json = CustomJSONProvider(app)  # Flask 3 way to customize JSON
CORS(app)  # Enable CORS for frontend communication

# ---------------- Initialize DB Indexes on startup (no before_first_request) ----------------
def initialize_db():
    ensure_customers_indexes()
    ensure_products_indexes()
    ensure_orders_indexes()

# Try to initialize once at startup; don't crash app if DB is down
try:
    initialize_db()
except Exception as e:
    # Avoid hard crash at import time; still report via logs
    print(f"[init warning] Failed to initialize DB indexes: {e}")

# ---------------- Error handler ----------------
@app.errorhandler(Exception)
def handle_error(e):
    return jsonify({"error": str(e)}), 500

# ================= CUSTOMERS API =================

@app.route('/api/customers', methods=['GET'])
def api_get_all_customers():
    """Get all customers"""
    try:
        customers = get_all_customers()
        return jsonify({"success": True, "data": customers})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/customers/<customer_id>', methods=['GET'])
def api_get_customer(customer_id):
    """Get customer by ID"""
    try:
        customer = get_customer_by_id(customer_id)
        if customer:
            return jsonify({"success": True, "data": customer})
        else:
            return jsonify({"success": False, "error": "לקוח לא נמצא"}), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/customers', methods=['POST'])
def api_create_customer():
    """Create new customer"""
    try:
        data = request.json or {}
        customer_id = create_customer(
            customer_id=data['customer_id'],
            name=data['name'],
            phone=data['phone'],
            email=data['email']
        )
        return jsonify({"success": True, "data": {"_id": customer_id}})
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/customers/<customer_id>', methods=['PUT'])
def api_update_customer(customer_id):
    """Update customer"""
    try:
        data = request.json or {}
        updated_customer = update_customer(
            customer_id=customer_id,
            name=data.get('name'),
            phone=data.get('phone'),
            email=data.get('email')
        )
        if updated_customer:
            return jsonify({"success": True, "data": updated_customer})
        else:
            return jsonify({"success": False, "error": "לקוח לא נמצא"}), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/customers/<customer_id>', methods=['DELETE'])
def api_delete_customer(customer_id):
    """Delete customer"""
    try:
        deleted_count = delete_customer(customer_id)
        if deleted_count > 0:
            return jsonify({"success": True, "message": "לקוח נמחק בהצלחה"})
        else:
            return jsonify({"success": False, "error": "לקוח לא נמצא"}), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# ================= PRODUCTS API =================

@app.route('/api/products', methods=['GET'])
def api_get_all_products():
    """Get all products"""
    try:
        products = get_all_products()
        return jsonify({"success": True, "data": products})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/products/<product_id>', methods=['GET'])
def api_get_product(product_id):
    """Get product by ID"""
    try:
        product = get_product_by_id(product_id)
        if product:
            return jsonify({"success": True, "data": product})
        else:
            return jsonify({"success": False, "error": "מוצר לא נמצא"}), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/products', methods=['POST'])
def api_create_product():
    """Create new product"""
    try:
        data = request.json or {}
        product_id = create_product(
            product_id=data['product_id'],
            name=data['name'],
            category=data['category'],
            price=float(data['price'])
        )
        return jsonify({"success": True, "data": {"_id": product_id}})
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/products/<product_id>', methods=['PUT'])
def api_update_product(product_id):
    """Update product"""
    try:
        data = request.json or {}
        price = data.get('price')  # handle 0 correctly
        updated_product = update_product(
            product_id=product_id,
            name=data.get('name'),
            category=data.get('category'),
            price=float(price) if price is not None else None
        )
        if updated_product:
            return jsonify({"success": True, "data": updated_product})
        else:
            return jsonify({"success": False, "error": "מוצר לא נמצא"}), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/products/<product_id>', methods=['DELETE'])
def api_delete_product(product_id):
    """Delete product"""
    try:
        deleted_count = delete_product(product_id)
        if deleted_count > 0:
            return jsonify({"success": True, "message": "מוצר נמחק בהצלחה"})
        else:
            return jsonify({"success": False, "error": "מוצר לא נמצא"}), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# ================= ORDERS API =================

@app.route('/api/orders', methods=['GET'])
def api_get_orders():
    """Get orders, optionally filtered by customer"""
    try:
        customer_id = request.args.get('customer_id')
        limit = int(request.args.get('limit', 100))
        skip = int(request.args.get('skip', 0))

        orders = list_orders(customer_id=customer_id, limit=limit, skip=skip)
        return jsonify({"success": True, "data": orders})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/orders/<order_id>', methods=['GET'])
def api_get_order(order_id):
    """Get order by ID"""
    try:
        order = get_order_by_id(order_id)
        if order:
            return jsonify({"success": True, "data": order})
        else:
            return jsonify({"success": False, "error": "הזמנה לא נמצאה"}), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/orders', methods=['POST'])
def api_create_order():
    """Create new order"""
    try:
        data = request.json or {}
        order_id = create_order(
            order_id=data['order_id'],
            customer_id=data['customer_id'],
            items=data['items']
        )
        return jsonify({"success": True, "data": {"_id": order_id}})
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/orders/<order_id>', methods=['PUT'])
def api_update_order(order_id):
    """Update order"""
    try:
        data = request.json or {}
        updated_order = update_order(
            order_id=order_id,
            status=data.get('status'),
            items=data.get('items')
        )
        if updated_order:
            return jsonify({"success": True, "data": updated_order})
        else:
            return jsonify({"success": False, "error": "הזמנה לא נמצאה"}), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/orders/<order_id>', methods=['DELETE'])
def api_delete_order(order_id):
    """Delete order"""
    try:
        deleted_count = delete_order(order_id)
        if deleted_count > 0:
            return jsonify({"success": True, "message": "הזמנה נמחקה בהצלחה"})
        else:
            return jsonify({"success": False, "error": "הזמנה לא נמצאה"}), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# ================= ANALYTICS API =================

@app.route('/api/analytics/revenue', methods=['GET'])
def api_total_revenue():
    """Get total revenue"""
    try:
        revenue = total_revenue()
        return jsonify({"success": True, "data": {"total_revenue": revenue}})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/analytics/top-customers', methods=['GET'])
def api_top_customers():
    """Get top customers by order count"""
    try:
        limit = int(request.args.get('limit', 5))
        top_customer_list = top_customers(limit=limit)
        return jsonify({"success": True, "data": top_customer_list})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/analytics/top-products', methods=['GET'])
def api_top_products():
    """Get top selling product"""
    try:
        top_product = top_products()
        return jsonify({"success": True, "data": top_product})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/analytics/counts', methods=['GET'])
def api_get_counts():
    """Get counts of customers, products, and orders"""
    try:
        customers_count = len(get_all_customers())
        products_count = len(get_all_products())
        orders_count = len(list_orders())

        return jsonify({
            "success": True,
            "data": {
                "customers": customers_count,
                "products": products_count,
                "orders": orders_count
            }
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "message": "Flask API is running"})

if __name__ == '__main__':
    print("🚀 Starting Flask API Server...")
    print("📊 Endpoints available:")
    print("   - GET  /api/customers")
    print("   - POST /api/customers")
    print("   - GET  /api/products")
    print("   - POST /api/products")
    print("   - GET  /api/orders")
    print("   - POST /api/orders")
    print("   - GET  /api/analytics/revenue")
    print("   - GET  /api/analytics/top-customers")
    print("   - GET  /api/analytics/top-products")
    print("   - GET  /api/health")

    app.run(debug=True, host='0.0.0.0', port=5000)
