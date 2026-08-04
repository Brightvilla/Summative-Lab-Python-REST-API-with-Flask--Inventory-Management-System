# Inventory Management System — Flask REST API

A Flask-based REST API for managing inventory, with OpenFoodFacts API integration and a CLI interface.
```text
Summative-Lab-Python-REST-API-with-Flask--Inventory-Management-System/
├── [app.py](VALID_FILE)      # Entry point, imports `app` from api.py and runs the server
├── [api.py](VALID_FILE)      # Flask REST API (routes + inventory logic)
├── [cli.py](VALID_FILE)      # CLI interface that talks to the API using `requests`
├── tests/
│   ├── test_api.py
│   └── test_cli.py
│   └── test_app.py * added.
└── [README.md](VALID_FILE)
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
Running the API
python [app.py](VALID_FILE)
Server runs at http://127.0.0.1:5000

API Endpoints
| Method | Endpoint | Description | |--------|----------|-------------| | GET | /inventory | Fetch all inventory items | | GET | /inventory/<id> | Fetch a single item by ID | | POST | /inventory | Add a new item | | PATCH | /inventory/<id> | Update an item | | DELETE | /inventory/<id> | Remove an item | | GET | /fetch | Fetch product from OpenFoodFacts |

Example Requests
GET all items

curl http://127.0.0.1:5000/inventory
GET single item

curl http://127.0.0.1:5000/inventory/1
POST new item

curl -X POST http://127.0.0.1:5000/inventory \
  -H "Content-Type: application/json" \
  -d '{"product_name": "Organic Almond Milk", "brands": "Silk", "price": 3.99, "stock": 50}'
PATCH update item

curl -X PATCH http://127.0.0.1:5000/inventory/1 \
  -H "Content-Type: application/json" \
  -d '{"price": 4.49, "stock": 45}'
DELETE item

curl -X DELETE http://127.0.0.1:5000/inventory/1
OpenFoodFacts Integration
Fetch product details by barcode or name:

# By barcode
curl http://127.0.0.1:5000/fetch?barcode=0012000161155

# By name
curl http://127.0.0.1:5000/fetch?name=almond+milk
CLI Usage
python [cli.py](VALID_FILE)
Available commands:

list                  View all inventory items
add                   Add a new inventory item
update <id>           Update price or stock of an item
delete <id>           Delete an item
fetch <barcode>       Look up a product on OpenFoodFacts
help                  Show available commands
quit / exit           Exit the CLI
Example CLI session:

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
Running Tests
pytest tests/
Tests cover:

All CRUD API endpoints
CLI commands
OpenFoodFacts API interactions (mocked with unittest.mock)
Project Structure
├── [app.py](VALID_FILE)           # Main Flask app
├── [cli.py](VALID_FILE)           # CLI interface
├── tests/
│   ├── test_api.py
│   └── test_cli.py
└── [README.md](VALID_FILE)
Data Model
Each inventory item follows this structure (inspired by OpenFoodFacts):

{
  "id": 1,
  "product_name": "Organic Almond Milk",
  "brands": "Silk",
  "ingredients_text": "Filtered water, almonds, cane sugar...",
  "price": 3.99,
  "stock": 50
}
Lab Criteria & Scenario
Scenario
You have been hired by a small retail company to develop an inventory management system. This system will allow employees to add, edit, view, and delete inventory items. Additionally, the system will fetch real-time product data from an external API (e.g., OpenFoodFacts API) to supplement product details.

You are tasked with creating an administrator portal for an e-commerce website which will include:

A Flask-based REST API with CRUD operations for managing inventory.
An external API integration to fetch product details by barcode or name.
A CLI-based interface to interact with the API.
Unit tests to validate functionality and interactions.
Define the Problem
Analyze and plan each necessary route.
Build a user interface to interact with each route.
Build Flask endpoints to trigger upon user action.
Connect to OpenFoodFacts API to get specific data from the database.
Update simulated data storage by updating an array.
Determine the Design
For each planned route determine the necessary route inputs as well as the output of each route.

Determine what it will change in regards to the data given.
Determine when each route will be triggered within the CLI application.
Utilizing the OpenFoodFacts database, build a mock database in an array.
The data should resemble what the OpenFoodFacts API may contain:

{
  "status": 1,
  "product": {
    "product_name": "Organic Almond Milk",
    "brands": "Silk",
    "ingredients_text": "Filtered water, almonds, cane sugar, ..."
  }
}
Ensure each item in your database array contains an ID.

Development Steps
Step 1 — File Setup

Initialize or clone a new Python project.
Install necessary packages like Flask.
Use GitHub.
Step 2 — API Design

Define API endpoints following RESTful conventions:
GET /inventory → Fetch all items
GET /inventory/<id> → Fetch a single item
POST /inventory → Add a new item
PATCH /inventory/<id> → Update an item
DELETE /inventory/<id> → Remove an item
Implement Flask routing and request handling.
Update temporary array to simulate storage.
Step 3 — Fetch Data

Use the OpenFoodFacts API to fetch product details.
Implement a function that queries the external API using a barcode or product name.
Enhance stored inventory data with additional details from the API.
Step 4 — CLI Frontend

Develop a CLI tool to interact with the API.
Allow users to: add items, view inventory, update price/stock, delete products, find items on the API.
Ensure error handling for invalid inputs and API failures.
Step 5 — Test and Debug

Write unit tests for API endpoints, CLI commands, and external API interactions.
Use pytest and unittest.mock to simulate API responses.
Debug with Flask Debug Mode and Postman for API validation.
Step 6 — Document and Maintain

Write a README.md with installation instructions, API endpoint details, and CLI usage examples.
Ensure clear code comments and maintainability.
Push the project to GitHub with a structured repository.
Criteria
| Criteria | Description | |----------|-------------| | Flask Routing | Routes for CRUD actions and helper routes built with Flask | | CRUD | Read, create, update (PATCH), and delete requests completed | | External API | Interface built to fetch from OpenFoodFacts and add to the database array | | Git Management | Git utilized, branches used, pull requests merged, branches cleared | | Testing | Testing suite built for each feature created |
Inventory Management System — Flask REST API
A Flask-based REST API for managing inventory, with OpenFoodFacts integration and a CLI interface.

1. Project Structure
Summative-Lab-Python-REST-API-with-Flask--Inventory-Management-System/
├── [app.py](VALID_FILE)              # Entry point, imports `app` from api.py and runs the server
├── [api.py](VALID_FILE)              # Flask REST API (routes + inventory logic)
├── [cli.py](VALID_FILE)              # CLI interface that talks to the API using `requests`
├── tests/
│   ├── test_api.py     # Tests for CRUD endpoints and /fetch
│   └── test_cli.py     # Tests for CLI behavior
└── [README.md](VALID_FILE)
2. Dependencies
This project only needs:

Flask
Flask-Cors
requests
pytest
Install them with pip (use the right Python for your environment).

Option A: Using the lab’s suggested Python (pyenv)
~/.pyenv/versions/3.8.13/bin/pip install Flask Flask-Cors requests pytest
Option B: Using your local Python
From the project root:

pip install Flask Flask-Cors requests pytest
(If you use a virtual environment, activate it first.)

3. How to Run the Web API (“website”)
The actual Flask app is defined in api.py, but you always start it via app.py.

Step-by-step
Open a terminal in the project folder:

cd Summative-Lab-Python-REST-API-with-Flask--Inventory-Management-System
Install dependencies (if not already installed):

pip install Flask Flask-Cors requests pytest
Start the Flask API:

python [app.py](VALID_FILE)
The server will run at:

URL: http://127.0.0.1:5000
You can now hit endpoints with curl, Postman, or from a browser (for simple GETs).
4. API Endpoints
| Method | Endpoint | Description | |--------|-------------------|----------------------------------| | GET | /inventory | Fetch all inventory items | | GET | /inventory/<id> | Fetch a single item by ID | | POST | /inventory | Add a new item | | PATCH | /inventory/<id> | Update an item | | DELETE | /inventory/<id> | Remove an item | | GET | /fetch | Fetch product from OpenFoodFacts |

Example Requests
Run these in a separate terminal while python app.py is running.

GET all items

curl http://127.0.0.1:5000/inventory
GET single item

curl http://127.0.0.1:5000/inventory/1
POST new item

curl -X POST http://127.0.0.1:5000/inventory \
  -H "Content-Type: application/json" \
  -d '{
        "product_name": "Organic Almond Milk",
        "brands": "Silk",
        "ingredients_text": "Filtered water, almonds, cane sugar",
        "price": 3.99,
        "stock": 50
      }'
PATCH update item

curl -X PATCH http://127.0.0.1:5000/inventory/1 \
  -H "Content-Type: application/json" \
  -d '{"price": 4.49, "stock": 45}'
DELETE item

curl -X DELETE http://127.0.0.1:5000/inventory/1
5. OpenFoodFacts Integration
You can fetch product details via /fetch using either a barcode or a name.

# By barcode
curl "http://127.0.0.1:5000/fetch?barcode=0012000161155"

# By name
curl "http://127.0.0.1:5000/fetch?name=almond+milk"
Response (shape will resemble):

{
  "product_name": "Organic Almond Milk",
  "brands": "Silk",
  "ingredients_text": "Filtered water, almonds, cane sugar..."
}
6. Running the CLI Application
The CLI (cli.py) is a separate program that uses the API over HTTP.

Steps
Make sure the API is running:

python [app.py](VALID_FILE)
In another terminal, run the CLI:

python [cli.py](VALID_FILE)
Use available commands (examples, depending on your cli.py implementation):

list                  # View all inventory items
add                   # Add a new inventory item
update <id>           # Update price or stock of an item
delete <id>           # Delete an item
fetch <barcode>       # Look up a product on OpenFoodFacts
help                  # Show available commands
quit / exit           # Exit the CLI
The CLI will send HTTP requests to http://127.0.0.1:5000 and show the results.

7. Running Tests (pytest)
Tests ensure your API and CLI work as expected. They assume:

The Flask app object is imported from app.py (which now re-exports app from api.py).
The CLI knows how to talk to the running API.
Step-by-step
Install test dependencies (if not already):

pip install pytest
From the project root, run:

pytest tests/ -v
or using the lab’s suggested Python:

~/.pyenv/versions/3.8.13/bin/pytest tests/ -v
You should see output similar to:

========================= test session starts =========================
collected X items

[tests/test_api.py](VALID_FILE)  .....
[tests/test_cli.py](VALID_FILE)  ....

========================== X passed in Ys ============================
If any tests fail, read the error message; it usually tells you which endpoint or behavior does not match expectations (status code, JSON keys, etc.).

8. Data Model
Each inventory item follows this structure:

{
  "id": 1,
  "product_name": "Organic Almond Milk",
  "brands": "Silk",
  "ingredients_text": "Filtered water, almonds, cane sugar...",
  "price": 3.99,
  "stock": 50
}
The data is stored in an in-memory Python list in api.py, so it resets each time you restart the server.

9. Quick Summary: From Zero to Passing Tests
Clone/open the project.

Install dependencies:

pip install Flask Flask-Cors requests pytest
(Optional) manually verify the API:

python [app.py](VALID_FILE)    # run server
curl http://127.0.0.1:5000/inventory
Run tests:

pytest tests/ -v
Use cli.py to interact with the API if desired:

python [app.py](VALID_FILE)    # terminal 1
python [cli.py](VALID_FILE)    # terminal 2
This flow takes you from installation to a running web API and a passing pytest suite.