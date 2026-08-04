from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    """
    Simple health-check endpoint for testing.
    """
    return jsonify({"message": "Test app is running"}), 200


@app.route("/inventory", methods=["GET"])
def inventory():
    """
    Minimal inventory endpoint for testing.
    """
    sample_inventory = [
        {
            "id": 1,
            "product_name": "Organic Almond Milk",
            "brands": "Silk",
            "ingredients_text": "Filtered water, almonds, cane sugar",
            "price": 3.99,
            "stock": 50,
        }
    ]
    return jsonify(sample_inventory), 200


if __name__ == "__main__":
    app.run(debug=True)
