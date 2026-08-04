from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# In-memory inventory "database"
inventory = []
next_id = 1  # auto-incrementing ID


def get_next_id():
    global next_id
    current = next_id
    next_id += 1
    return current


def find_item(item_id):
    return next((item for item in inventory if item["id"] == item_id), None)


@app.route("/inventory", methods=["GET"])
def get_inventory():
    """Fetch all inventory items."""
    return jsonify(inventory), 200


@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_inventory_item(item_id):
    """Fetch a single inventory item by ID."""
    item = find_item(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(item), 200


@app.route("/inventory", methods=["POST"])
def add_inventory_item():
    """Add a new inventory item."""
    data = request.get_json() or {}

    required_fields = ["product_name", "brands", "price", "stock"]
    missing = [f for f in required_fields if f not in data]
    if missing:
        return jsonify({"error": f"Missing field(s): {', '.join(missing)}"}), 400

    item = {
        "id": get_next_id(),
        "product_name": data["product_name"],
        "brands": data["brands"],
        "ingredients_text": data.get("ingredients_text", ""),
        "price": data["price"],
        "stock": data["stock"],
    }
    inventory.append(item)
    return jsonify(item), 201


@app.route("/inventory/<int:item_id>", methods=["PATCH"])
def update_inventory_item(item_id):
    """Update an existing inventory item (partial update)."""
    item = find_item(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404

    data = request.get_json() or {}
    for field in ["product_name", "brands", "ingredients_text", "price", "stock"]:
        if field in data:
            item[field] = data[field]
    return jsonify(item), 200


@app.route("/inventory/<int:item_id>", methods=["DELETE"])
def delete_inventory_item(item_id):
    """Delete an inventory item by ID."""
    item = find_item(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    inventory.remove(item)
    return jsonify(item), 200


@app.route("/fetch", methods=["GET"])
def fetch_product():
    """
    Fetch product from OpenFoodFacts by barcode or name (real API call).
    """
    barcode = request.args.get("barcode")
    name = request.args.get("name")

    if not barcode and not name:
        return jsonify({"error": "barcode or name query parameter required"}), 400

    try:
        if barcode:
            url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
            resp = requests.get(url, timeout=5)
            data = resp.json()

            if data.get("status") != 1:
                return jsonify({"error": "Product not found"}), 404

            product = data.get("product", {})
        else:
            url = "https://world.openfoodfacts.org/cgi/search.pl"
            params = {
                "search_terms": name,
                "search_simple": 1,
                "action": "process",
                "json": 1,
            }
            resp = requests.get(url, params=params, timeout=5)
            data = resp.json()
            products = data.get("products", [])
            if not products:
                return jsonify({"error": "Product not found"}), 404
            product = products[0]

        result = {
            "product_name": product.get("product_name"),
            "brands": product.get("brands"),
            "ingredients_text": product.get("ingredients_text"),
        }
        return jsonify(result), 200

    except requests.RequestException as exc:
        return jsonify({"error": "Failed to fetch from OpenFoodFacts", "detail": str(exc)}), 502


if __name__ == "__main__":
    app.run(debug=True, port=5002)