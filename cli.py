import requests

BASE = "http://127.0.0.1:5001"

def list_items():
    try:
        res = requests.get(f"{BASE}/inventory")
        res.raise_for_status()
        items = res.json()
    except requests.exceptions.RequestException as e:
        print(f"Error contacting API: {e}")
        return
    except ValueError:
        print("Error: API did not return valid JSON.")
        return

    if not items:
        print("No items in inventory.")
        return
    print(f"{'ID':<5} {'Name':<25} {'Brand':<15} {'Price':<8} {'Stock'}")
    print("-" * 65)
    for item in items:
        print(f"{item['id']:<5} {item['product_name']:<25} {item['brands']:<15} ${item['price']:<7} {item['stock']}")

def add_item():
    name = input("Product name: ").strip()
    brand = input("Brand: ").strip()

    raw_price = input("Price: ").strip()
    # Remove common non-numeric characters
    for ch in ["$", "Price:", "price:", ","]:
        raw_price = raw_price.replace(ch, "")
    raw_price = raw_price.strip()
    try:
        price = float(raw_price)
    except ValueError:
        print("Invalid price. Please enter a number like 3.99 (optionally with '$').")
        return

    try:
        stock = int(input("Stock: ").strip())
    except ValueError:
        print("Invalid stock. Please enter an integer like 50.")
        return

    res = requests.post(
        f"{BASE}/inventory",
        json={"product_name": name, "brands": brand, "price": price, "stock": stock},
    )
    if res.status_code == 201:
        print(f"✓ Item added with ID {res.json()['id']}")
    else:
        print(f"Error: {res.json().get('error')}")
def update_item(item_id):
    price_input = input("New price (leave blank to skip): ").strip()
    stock_input = input("New stock (leave blank to skip): ").strip()

    payload = {}

    if price_input:
        raw_price = price_input
        # Remove common non-numeric characters
        for ch in ["$", "Price:", "price:", ","]:
            raw_price = raw_price.replace(ch, "")
        raw_price = raw_price.strip().rstrip(".")  # handle "3.99." case
        try:
            payload["price"] = float(raw_price)
        except ValueError:
            print("Invalid price. Please enter a number like 3.99 (optionally with '$').")
            return

    if stock_input:
        try:
            payload["stock"] = int(stock_input.strip())
        except ValueError:
            print("Invalid stock. Please enter an integer like 50.")
            return

    if not payload:
        print("Nothing to update.")
        return

    try:
        res = requests.patch(f"{BASE}/inventory/{item_id}", json=payload)
        res.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error contacting API: {e}")
        return

    try:
        data = res.json()
    except ValueError:
        print("Error: API did not return valid JSON.")
        return

    if res.status_code == 200:
        print("✓ Item updated.")
    else:
        print(f"Error: {data.get('error')}")
def delete_item(item_id):
    res = requests.delete(f"{BASE}/inventory/{item_id}")
    if res.status_code == 200:
        print(f"✓ Item {item_id} deleted.")
    else:
        print(f"Error: {res.json().get('error')}")

def fetch_product(barcode):
    try:
        res = requests.get(f"{BASE}/fetch", params={"barcode": barcode})
        res.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error contacting API: {e}")
        return

    try:
        p = res.json()
    except ValueError:
        print("Error: API did not return valid JSON for fetch.")
        return

    # Basic validation that expected keys exist
    if not p.get("product_name"):
        print("Error: Product not found or missing 'product_name'.")
        return

    print(f"Name: {p.get('product_name')}\nBrand: {p.get('brands')}\nIngredients: {p.get('ingredients_text')}")
    add = input("Add to inventory? (y/n): ").strip().lower()
    if add == "y":
        try:
            price = float(input("Price: ").strip())
            stock = int(input("Stock: ").strip())
        except ValueError:
            print("Invalid price or stock. Please enter numeric values.")
            return

        try:
            add_res = requests.post(
                f"{BASE}/inventory",
                json={**p, "price": price, "stock": stock},
            )
            add_res.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error adding product to inventory: {e}")
            return

        print("✓ Added to inventory.")
def main():
    print("Inventory CLI — type 'help' for commands")
    while True:
        cmd = input("\n> ").strip().split()
        if not cmd:
            continue
        action = cmd[0].lower()
        if action == "list":
            list_items()
        elif action == "add":
            add_item()
        elif action == "update" and len(cmd) == 2:
            try:
                item_id = int(cmd[1])
            except ValueError:
                print("Invalid ID. Usage: update <id>")
                continue
            update_item(item_id)
        elif action == "delete" and len(cmd) == 2:
            delete_item(cmd[1])
        elif action == "fetch" and len(cmd) == 2:
            fetch_product(cmd[1])
        elif action == "help":
            print("list | add | update <id> | delete <id> | fetch <barcode> | quit")
        elif action in ("quit", "exit"):
            break
        else:
            print("Unknown command. Type 'help' for options.")

if __name__ == "__main__":
    main()
