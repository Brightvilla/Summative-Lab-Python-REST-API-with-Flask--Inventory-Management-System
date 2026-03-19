import pytest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import app as flask_app


@pytest.fixture
def client():
    flask_app.app.config["TESTING"] = True
    flask_app.inventory.clear()
    flask_app.inventory.extend([
        {"id": 1, "product_name": "Almond Milk", "brands": "Silk", "ingredients_text": "Water, almonds", "price": 3.99, "stock": 50},
        {"id": 2, "product_name": "Whole Grain Bread", "brands": "Nature's Own", "ingredients_text": "Wheat flour", "price": 2.49, "stock": 30},
    ])
    with flask_app.app.test_client() as client:
        yield client


# GET /inventory
def test_get_inventory(client):
    res = client.get("/inventory")
    assert res.status_code == 200
    assert len(res.get_json()) == 2


# GET /inventory/<id>
def test_get_item(client):
    res = client.get("/inventory/1")
    assert res.status_code == 200
    assert res.get_json()["product_name"] == "Almond Milk"


def test_get_item_not_found(client):
    res = client.get("/inventory/99")
    assert res.status_code == 404


# POST /inventory
def test_add_item(client):
    res = client.post("/inventory", json={"product_name": "Oat Milk", "brands": "Oatly", "price": 4.99, "stock": 20})
    assert res.status_code == 201
    assert res.get_json()["product_name"] == "Oat Milk"


def test_add_item_missing_name(client):
    res = client.post("/inventory", json={"brands": "Oatly"})
    assert res.status_code == 400


# PATCH /inventory/<id>
def test_update_item(client):
    res = client.patch("/inventory/1", json={"price": 5.99, "stock": 10})
    assert res.status_code == 200
    data = res.get_json()
    assert data["price"] == 5.99
    assert data["stock"] == 10


def test_update_item_not_found(client):
    res = client.patch("/inventory/99", json={"price": 1.00})
    assert res.status_code == 404


# DELETE /inventory/<id>
def test_delete_item(client):
    res = client.delete("/inventory/1")
    assert res.status_code == 200
    assert client.get("/inventory/1").status_code == 404


def test_delete_item_not_found(client):
    res = client.delete("/inventory/99")
    assert res.status_code == 404


# GET /fetch — barcode
def test_fetch_by_barcode(client):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "status": 1,
        "product": {"product_name": "Pepsi", "brands": "PepsiCo", "ingredients_text": "Water, sugar"}
    }
    with patch("app.requests.get", return_value=mock_response):
        res = client.get("/fetch?barcode=0012000161155")
    assert res.status_code == 200
    assert res.get_json()["product_name"] == "Pepsi"


def test_fetch_by_barcode_not_found(client):
    mock_response = MagicMock()
    mock_response.json.return_value = {"status": 0}
    with patch("app.requests.get", return_value=mock_response):
        res = client.get("/fetch?barcode=0000000000000")
    assert res.status_code == 404


# GET /fetch — name
def test_fetch_by_name(client):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "products": [{"product_name": "Almond Milk", "brands": "Silk", "ingredients_text": "Water, almonds"}]
    }
    with patch("app.requests.get", return_value=mock_response):
        res = client.get("/fetch?name=almond+milk")
    assert res.status_code == 200
    assert res.get_json()["brands"] == "Silk"


def test_fetch_no_params(client):
    res = client.get("/fetch")
    assert res.status_code == 400
