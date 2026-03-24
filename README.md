# My Mechanic Factory Pattern App

Flask REST API for managing customers in a mechanic shop application using the Flask application factory pattern.

## Stack

- Flask
- Flask-SQLAlchemy
- Flask-Marshmallow
- Marshmallow-SQLAlchemy
- SQLAlchemy
- MySQL Connector/Python

## Project Structure

```text
my_mechanic/
├── app/
│   ├── __init__.py
│   ├── extensions.py
│   ├── models.py
│   └── blueprint/
│       └── customers/
│           ├── __init__.py
│           ├── routes.py
│           └── schemas.py
├── app.py
├── config.py
└── requirements.txt
```

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Optionally set environment variables:

```bash
export DATABASE_URL="mysql+mysqlconnector://username:password@localhost/library_db"
export APP_CONFIG="DevelopmentConfig"
export PORT=5002
```

If `DATABASE_URL` is not set, the app defaults to a local SQLite database at `sqlite:///my_mechanic.db`.

## Run

```bash
python app.py
```

Default URL:

```text
http://127.0.0.1:5002
```

## Customer Endpoints

- `POST /customers/`
- `GET /customers/<id>`
- `PUT /customers/<id>`
- `DELETE /customers/<id>`

## Example Request

```bash
curl -X POST http://127.0.0.1:5002/customers/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Doe",
    "phone": "555-123-4567",
    "email": "jane@example.com"
  }'
```