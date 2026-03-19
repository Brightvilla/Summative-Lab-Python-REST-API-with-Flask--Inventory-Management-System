# Inventory Management System — Flask REST API

A Flask-based REST API for managing inventory, with OpenFoodFacts API integration and a CLI interface.

---
Run this in your terminal to install for the correct Python:

~/.pyenv/versions/3.8.13/bin/pip install flask flask-cors requests

Copy
bash
Then run tests with:

~/.pyenv/versions/3.8.13/bin/pytest tests/ -v

Copy
## Setup & Installation

**Prerequisites:** Python 3.8+

```bash
# Clone the repo
git clone <your-repo-url>
cd <repo-folder>

# Install dependencies
pip install flask flask-cors requests pytest
```

---

## Running the API

```bash
python app.py
```

Server runs at `http://127.0.0.1:5000`

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/inventory` | Fetch all inventory items |
| GET | `/inventory/<id>` | Fetch a single item by ID |
| POST | `/inventory` | Add a new item |
| PATCH | `/inventory/<id>` | Update an item |
| DELETE | `/inventory/<id>` | Remove an item |
| GET | `/fetch` | Fetch product from OpenFoodFacts |

### Example Requests

**GET all items**
```bash
curl http://127.0.0.1:5000/inventory
```

**GET single item**
```bash
curl http://127.0.0.1:5000/inventory/1
```

**POST new item**
```bash
curl -X POST http://127.0.0.1:5000/inventory \
  -H "Content-Type: application/json" \
  -d '{"product_name": "Organic Almond Milk", "brands": "Silk", "price": 3.99, "stock": 50}'
```

**PATCH update item**
```bash
curl -X PATCH http://127.0.0.1:5000/inventory/1 \
  -H "Content-Type: application/json" \
  -d '{"price": 4.49, "stock": 45}'
```

**DELETE item**
```bash
curl -X DELETE http://127.0.0.1:5000/inventory/1
```

---

## OpenFoodFacts Integration

Fetch product details by barcode or name:

```bash
# By barcode
curl http://127.0.0.1:5000/fetch?barcode=0012000161155

# By name
curl http://127.0.0.1:5000/fetch?name=almond+milk
```

---

## CLI Usage

```bash
python cli.py
```

Available commands:

```
list                  View all inventory items
add                   Add a new inventory item
update <id>           Update price or stock of an item
delete <id>           Delete an item
fetch <barcode>       Look up a product on OpenFoodFacts
help                  Show available commands
quit / exit           Exit the CLI
```

**Example CLI session:**
```
> add
Product name: Organic Almond Milk
Brand: Silk
Price: 3.99
Stock: 50
✓ Item added with ID 1

> list
ID    Name                      Brand           Price    Stock
-----------------------------------------------------------------
1     Organic Almond Milk       Silk            $3.99    50
```

---

## Running Tests

```bash
pytest tests/
```

Tests cover:
- All CRUD API endpoints
- CLI commands
- OpenFoodFacts API interactions (mocked with `unittest.mock`)

---

## Project Structure

```
├── app.py           # Main Flask app
├── cli.py           # CLI interface
├── tests/
│   ├── test_api.py
│   └── test_cli.py
└── README.md
```

---

## Data Model

Each inventory item follows this structure (inspired by OpenFoodFacts):

```json
{
  "id": 1,
  "product_name": "Organic Almond Milk",
  "brands": "Silk",
  "ingredients_text": "Filtered water, almonds, cane sugar...",
  "price": 3.99,
  "stock": 50
}
```

---

## Lab Criteria & Scenario

### Scenario

You have been hired by a small retail company to develop an inventory management system. This system will allow employees to add, edit, view, and delete inventory items. Additionally, the system will fetch real-time product data from an external API (e.g., OpenFoodFacts API) to supplement product details.

You are tasked with creating an administrator portal for an e-commerce website which will include:

- A Flask-based REST API with CRUD operations for managing inventory.
- An external API integration to fetch product details by barcode or name.
- A CLI-based interface to interact with the API.
- Unit tests to validate functionality and interactions.

---

### Define the Problem

- Analyze and plan each necessary route.
- Build a user interface to interact with each route.
- Build Flask endpoints to trigger upon user action.
- Connect to OpenFoodFacts API to get specific data from the database.
- Update simulated data storage by updating an array.

---

### Determine the Design

For each planned route determine the necessary route inputs as well as the output of each route.

- Determine what it will change in regards to the data given.
- Determine when each route will be triggered within the CLI application.
- Utilizing the OpenFoodFacts database, build a mock database in an array.

The data should resemble what the OpenFoodFacts API may contain:

```json
{
  "status": 1,
  "product": {
    "product_name": "Organic Almond Milk",
    "brands": "Silk",
    "ingredients_text": "Filtered water, almonds, cane sugar, ..."
  }
}
```

Ensure each item in your database array contains an ID.

---

### Development Steps

**Step 1 — File Setup**
- Initialize or clone a new Python project.
- Install necessary packages like Flask.
- Use GitHub.

**Step 2 — API Design**
- Define API endpoints following RESTful conventions:
  - `GET /inventory` → Fetch all items
  - `GET /inventory/<id>` → Fetch a single item
  - `POST /inventory` → Add a new item
  - `PATCH /inventory/<id>` → Update an item
  - `DELETE /inventory/<id>` → Remove an item
- Implement Flask routing and request handling.
- Update temporary array to simulate storage.

**Step 3 — Fetch Data**
- Use the OpenFoodFacts API to fetch product details.
- Implement a function that queries the external API using a barcode or product name.
- Enhance stored inventory data with additional details from the API.

**Step 4 — CLI Frontend**
- Develop a CLI tool to interact with the API.
- Allow users to: add items, view inventory, update price/stock, delete products, find items on the API.
- Ensure error handling for invalid inputs and API failures.

**Step 5 — Test and Debug**
- Write unit tests for API endpoints, CLI commands, and external API interactions.
- Use `pytest` and `unittest.mock` to simulate API responses.
- Debug with Flask Debug Mode and Postman for API validation.

**Step 6 — Document and Maintain**
- Write a `README.md` with installation instructions, API endpoint details, and CLI usage examples.
- Ensure clear code comments and maintainability.
- Push the project to GitHub with a structured repository.

---

### Criteria

| Criteria | Description |
|----------|-------------|
| Flask Routing | Routes for CRUD actions and helper routes built with Flask |
| CRUD | Read, create, update (PATCH), and delete requests completed |
| External API | Interface built to fetch from OpenFoodFacts and add to the database array |
| Git Management | Git utilized, branches used, pull requests merged, branches cleared |
| Testing | Testing suite built for each feature created |
