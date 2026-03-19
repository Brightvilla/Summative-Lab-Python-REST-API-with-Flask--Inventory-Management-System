from unittest.mock import patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import cli


ITEMS = [
    {"id": 1, "product_name": "Almond Milk", "brands": "Silk", "ingredients_text": "Water, almonds", "price": 3.99, "stock": 50}
]


# list_items
def test_list_items(capsys):
    mock_res = MagicMock()
    mock_res.json.return_value = ITEMS
    with patch("cli.requests.get", return_value=mock_res):
        cli.list_items()
    out = capsys.readouterr().out
    assert "Almond Milk" in out


def test_list_items_empty(capsys):
    mock_res = MagicMock()
    mock_res.json.return_value = []
    with patch("cli.requests.get", return_value=mock_res):
        cli.list_items()
    assert "No items" in capsys.readouterr().out


# add_item
def test_add_item(capsys):
    mock_res = MagicMock()
    mock_res.status_code = 201
    mock_res.json.return_value = {"id": 3}
    with patch("cli.requests.post", return_value=mock_res), \
         patch("builtins.input", side_effect=["Oat Milk", "Oatly", "4.99", "20"]):
        cli.add_item()
    assert "ID 3" in capsys.readouterr().out


def test_add_item_error(capsys):
    mock_res = MagicMock()
    mock_res.status_code = 400
    mock_res.json.return_value = {"error": "product_name is required"}
    with patch("cli.requests.post", return_value=mock_res), \
         patch("builtins.input", side_effect=["", "Oatly", "4.99", "20"]):
        cli.add_item()
    assert "Error" in capsys.readouterr().out


# update_item
def test_update_item(capsys):
    mock_res = MagicMock()
    mock_res.status_code = 200
    with patch("cli.requests.patch", return_value=mock_res), \
         patch("builtins.input", side_effect=["5.99", "10"]):
        cli.update_item("1")
    assert "updated" in capsys.readouterr().out


def test_update_item_nothing(capsys):
    with patch("builtins.input", side_effect=["", ""]):
        cli.update_item("1")
    assert "Nothing" in capsys.readouterr().out


# delete_item
def test_delete_item(capsys):
    mock_res = MagicMock()
    mock_res.status_code = 200
    with patch("cli.requests.delete", return_value=mock_res):
        cli.delete_item("1")
    assert "deleted" in capsys.readouterr().out


def test_delete_item_error(capsys):
    mock_res = MagicMock()
    mock_res.status_code = 404
    mock_res.json.return_value = {"error": "Item not found"}
    with patch("cli.requests.delete", return_value=mock_res):
        cli.delete_item("99")
    assert "Error" in capsys.readouterr().out


# fetch_product
def test_fetch_product(capsys):
    mock_res = MagicMock()
    mock_res.status_code = 200
    mock_res.json.return_value = {"product_name": "Pepsi", "brands": "PepsiCo", "ingredients_text": "Water, sugar"}
    with patch("cli.requests.get", return_value=mock_res), \
         patch("builtins.input", return_value="n"):
        cli.fetch_product("0012000161155")
    assert "Pepsi" in capsys.readouterr().out


def test_fetch_product_add_to_inventory(capsys):
    mock_get = MagicMock()
    mock_get.status_code = 200
    mock_get.json.return_value = {"product_name": "Pepsi", "brands": "PepsiCo", "ingredients_text": "Water, sugar"}
    mock_post = MagicMock()
    with patch("cli.requests.get", return_value=mock_get), \
         patch("cli.requests.post", return_value=mock_post), \
         patch("builtins.input", side_effect=["y", "1.99", "100"]):
        cli.fetch_product("0012000161155")
    assert "Added" in capsys.readouterr().out


def test_fetch_product_not_found(capsys):
    mock_res = MagicMock()
    mock_res.status_code = 404
    mock_res.json.return_value = {"error": "Product not found"}
    with patch("cli.requests.get", return_value=mock_res):
        cli.fetch_product("0000000000000")
    assert "Error" in capsys.readouterr().out


# main loop
def test_main_quit(capsys):
    with patch("builtins.input", side_effect=["quit"]):
        cli.main()


def test_main_unknown_command(capsys):
    with patch("builtins.input", side_effect=["badcmd", "quit"]):
        cli.main()
    assert "Unknown" in capsys.readouterr().out
