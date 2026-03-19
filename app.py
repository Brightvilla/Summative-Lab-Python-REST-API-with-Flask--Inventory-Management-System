from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

inventory = [
    {"id": 1, "product_name": "Organic Almond Milk", "brands": "Silk", "ingredients_text": "Filtered water, almonds, cane sugar", "price": 3.99, "stock": 50},
    {"id": 2, "product_name": "Whole Grain Bread", "brands": "Nature's Own", "ingredients_text": "Whole wheat flour, water, yeast", "price": 2.49, "stock": 30},
]

def find_item(item_id):
    return next((item for item in inventory if item["id"] == item_id), None)

# CRUD Routes
@app.route("/inventory", methods=["GET"])
def get_inventory():
    return jsonify(inventory)

@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_item(item_id):
    item = find_item(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(item)

@app.route("/inventory", methods=["POST"])
def add_item():
    data = request.get_json()
    if not data or "product_name" not in data:
        return jsonify({"error": "product_name is required"}), 400
    new_item = {
        "id": max((i["id"] for i in inventory), default=0) + 1,
        "product_name": data.get("product_name"),
        "brands": data.get("brands", ""),
        "ingredients_text": data.get("ingredients_text", ""),
        "price": data.get("price", 0.0),
        "stock": data.get("stock", 0),
    }
    inventory.append(new_item)
    return jsonify(new_item), 201

@app.route("/inventory/<int:item_id>", methods=["PATCH"])
def update_item(item_id):
    item = find_item(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    data = request.get_json()
    for field in ("product_name", "brands", "ingredients_text", "price", "stock"):
        if field in data:
            item[field] = data[field]
    return jsonify(item)

@app.route("/inventory/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    item = find_item(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    inventory.remove(item)
    return jsonify({"message": f"Item {item_id} deleted"})

# External API Route
@app.route("/fetch", methods=["GET"])
def fetch_product():
    barcode = request.args.get("barcode")
    name = request.args.get("name")

    if barcode:
        url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
        res = requests.get(url)
        data = res.json()
        if data.get("status") != 1:
            return jsonify({"error": "Product not found"}), 404
        product = data["product"]
    elif name:
        url = f"https://world.openfoodfacts.org/cgi/search.pl?search_terms={name}&json=1"
        res = requests.get(url)
        products = res.json().get("products", [])
        if not products:
            return jsonify({"error": "No products found"}), 404
        product = products[0]
    else:
        return jsonify({"error": "Provide barcode or name query param"}), 400

    result = {
        "product_name": product.get("product_name", ""),
        "brands": product.get("brands", ""),
        "ingredients_text": product.get("ingredients_text", ""),
    }
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
