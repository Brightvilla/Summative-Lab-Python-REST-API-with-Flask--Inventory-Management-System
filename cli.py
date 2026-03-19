import requests

BASE = "http://127.0.0.1:5000"

def list_items():
    res = requests.get(f"{BASE}/inventory")
    items = res.json()
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
    price = float(input("Price: ").strip())
    stock = int(input("Stock: ").strip())
    res = requests.post(f"{BASE}/inventory", json={"product_name": name, "brands": brand, "price": price, "stock": stock})
    if res.status_code == 201:
        print(f"✓ Item added with ID {res.json()['id']}")
    else:
        print(f"Error: {res.json().get('error')}")

def update_item(item_id):
    price = input("New price (leave blank to skip): ").strip()
    stock = input("New stock (leave blank to skip): ").strip()
    payload = {}
    if price:
        payload["price"] = float(price)
    if stock:
        payload["stock"] = int(stock)
    if not payload:
        print("Nothing to update.")
        return
    res = requests.patch(f"{BASE}/inventory/{item_id}", json=payload)
    if res.status_code == 200:
        print("✓ Item updated.")
    else:
        print(f"Error: {res.json().get('error')}")

def delete_item(item_id):
    res = requests.delete(f"{BASE}/inventory/{item_id}")
    if res.status_code == 200:
        print(f"✓ Item {item_id} deleted.")
    else:
        print(f"Error: {res.json().get('error')}")

def fetch_product(barcode):
    res = requests.get(f"{BASE}/fetch", params={"barcode": barcode})
    if res.status_code == 200:
        p = res.json()
        print(f"Name: {p['product_name']}\nBrand: {p['brands']}\nIngredients: {p['ingredients_text']}")
        add = input("Add to inventory? (y/n): ").strip().lower()
        if add == "y":
            price = float(input("Price: ").strip())
            stock = int(input("Stock: ").strip())
            requests.post(f"{BASE}/inventory", json={**p, "price": price, "stock": stock})
            print("✓ Added to inventory.")
    else:
        print(f"Error: {res.json().get('error')}")

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
            update_item(cmd[1])
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
