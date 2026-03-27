# My Mechanic API

A RESTful API for managing an auto mechanic shop — customers, mechanics, service tickets, and parts inventory. Built with Flask using the **factory pattern** and organized with **blueprints** for clean, scalable architecture.

## Features

- **JWT Authentication** with role-based access control (customer vs. mechanic tokens)
- **CRUD operations** for customers, mechanics, service tickets, and inventory
- **Many-to-many relationships** between mechanics and tickets, and between tickets and parts
- **Rate limiting** and **response caching** for performance and abuse prevention
- **Pagination** on list endpoints
- **Input validation** with Marshmallow schemas
- **Batch operations** for assigning/removing multiple mechanics from a ticket

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | Flask 3.x |
| ORM | Flask-SQLAlchemy |
| Validation | Flask-Marshmallow / marshmallow-sqlalchemy |
| Auth | python-jose (JWT) |
| Rate Limiting | Flask-Limiter |
| Caching | Flask-Caching |
| Database | SQLite (default) / MySQL |

## Project Structure

```
my_mechanic/
├── app.py                  # Entry point
├── config.py               # App configuration (Dev / Prod)
├── requirements.txt        # Python dependencies
├── app/
│   ├── __init__.py         # Application factory (create_app)
│   ├── extensions.py       # Marshmallow, Limiter, Cache setup
│   ├── models.py           # SQLAlchemy models
│   ├── utils/
│   │   └── util.py         # JWT encode/decode & auth decorators
│   └── blueprint/
│       ├── customers/      # Customer endpoints & schema
│       ├── mechanics/      # Mechanic endpoints & schema
│       ├── service_tickets/ # Service ticket endpoints & schema
│       └── inventory/      # Inventory endpoints & schema
└── docs/
    └── *.postman_collection.json
```

## Getting Started

### Prerequisites

- Python 3.10+
- pip

### Installation

```bash
# Clone the repo
git clone https://github.com/Pr1nc3B33/my-mechanic-factory-pattern-app.git
cd my-mechanic-factory-pattern-app

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | JWT signing key | *must be set* |
| `DATABASE_URL` | Database connection string | `sqlite:///my_mechanic.db` |
| `APP_CONFIG` | Config class name | `DevelopmentConfig` |
| `PORT` | Server port | `5002` |

```bash
export SECRET_KEY="your-secret-key-here"
export DATABASE_URL="mysql+mysqlconnector://user:pass@localhost/my_mechanic"
```

### Run

```bash
python app.py
```

The API will be available at `http://127.0.0.1:5002`.

## API Endpoints

### Customers `/customers`

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `POST` | `/customers/` | — | Create a customer |
| `POST` | `/customers/login` | — | Login, returns JWT |
| `GET` | `/customers/` | — | List all customers (paginated) |
| `GET` | `/customers/<id>` | — | Get customer by ID |
| `GET` | `/customers/my-tickets` | Customer | Get logged-in customer's tickets |
| `PUT` | `/customers/<id>` | Customer | Update a customer |
| `DELETE` | `/customers/<id>` | Customer | Delete a customer |

### Mechanics `/mechanics`

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `POST` | `/mechanics/` | — | Create a mechanic |
| `POST` | `/mechanics/login` | — | Login, returns JWT |
| `GET` | `/mechanics/` | — | List all mechanics |
| `GET` | `/mechanics/most-tickets` | — | Rank mechanics by ticket count |
| `PUT` | `/mechanics/<id>` | Mechanic | Update a mechanic |
| `DELETE` | `/mechanics/<id>` | Mechanic | Delete a mechanic |

### Service Tickets `/service-tickets`

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `POST` | `/service-tickets/` | — | Create a service ticket |
| `GET` | `/service-tickets/` | — | List all service tickets |
| `PUT` | `/service-tickets/<id>/assign-mechanic/<mid>` | Mechanic | Assign mechanic to ticket |
| `PUT` | `/service-tickets/<id>/remove-mechanic/<mid>` | Mechanic | Remove mechanic from ticket |
| `PUT` | `/service-tickets/<id>/edit` | Mechanic | Batch add/remove mechanics |
| `POST` | `/service-tickets/<id>/add-part/<pid>` | Mechanic | Add inventory part to ticket |

### Inventory `/inventory`

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `POST` | `/inventory/` | — | Create a part |
| `GET` | `/inventory/` | — | List all parts |
| `GET` | `/inventory/<id>` | — | Get part by ID |
| `PUT` | `/inventory/<id>` | — | Update a part |
| `DELETE` | `/inventory/<id>` | — | Delete a part |

## Authentication

Endpoints marked **Customer** or **Mechanic** require a JWT token in the `Authorization` header:

```
Authorization: Bearer <token>
```

Obtain a token by sending a `POST` to the relevant `/login` endpoint with `email` and `password` in the request body.

## Postman Collection

A ready-to-use Postman collection is included at `docs/my_mechanic_factory_pattern_app.postman_collection.json`. Import it into Postman to test all endpoints.
