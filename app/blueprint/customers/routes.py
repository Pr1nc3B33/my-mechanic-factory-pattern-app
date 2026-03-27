from app.blueprint.customers import customers_bp
from .schemas import customer_schema, customers_schema
from app.models import Customer, db
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.extensions import limiter, cache
from app.utils.util import encode_token
from app.utils.util import encode_token, token_required
from app.blueprint.customers.schemas import customer_schema, customers_schema, login_schema



@customers_bp.route("/login", methods = ['POST'])
def login():
    try:
        credentials = request.json
        username = credentials['email']
        password = credentials['password']
    except KeyError:
        return jsonify({'messages':'invalid payload'}), 400    
    query = select(Customer).where(Customer.email == username)
    customer = db.session.execute(query).scalar_one_or_none()
    
    if customer and customer.password == password:
        auth_token = encode_token(customer.id)
        
        response = {
            "status":"success",
            "message":"Login Successfull",
            "auth_token": auth_token
            
        }
        return jsonify(response), 200
    else:
        return jsonify({'message':'Invalid email or password'}), 401    


@customers_bp.route("/", methods = ['GET'])
def get_customers():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    query = select(Customer).limit(per_page).offset((page - 1) * per_page)
    all_customers = db.session.execute(query).scalars().all()
    return customers_schema.jsonify(all_customers), 200


@customers_bp.route("/", methods = ['POST'])
@limiter.limit("5 per minute")
@cache.cached(timeout=60)
def create_customer():
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400   
    query = select(Customer).where(Customer.email == customer_data['email'])
    existing_customer = db.session.execute(query).scalars().all()
    if existing_customer:
        return jsonify({"error": "Customer with this email already exists"}), 400
    new_customer = Customer(**customer_data)
    db.session.add(new_customer)
    db.session.commit()
    return customer_schema.jsonify(new_customer), 201

@customers_bp.route("/<int:id>", methods = ['GET'])
@limiter.limit("10 per minute")
def get_customer(id):
    customer = db.session.get(Customer, id)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404
    return customer_schema.jsonify(customer), 200

@customers_bp.route("/<int:id>", methods = ['PUT'])
def update_customer(id):
    customer = db.session.get(Customer, id)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404
    try:
        customer_data = customer_schema.load(request.json, partial=True)
    except ValidationError as e:
        return jsonify(e.messages), 400
    for key, value in customer_data.items():
        setattr(customer, key, value)
    db.session.commit()
    return customer_schema.jsonify(customer), 200
    

@customers_bp.route("/<int:id>", methods = ['DELETE'])
def delete_customer(id):
    customer = db.session.get(Customer, id)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": "Customer deleted successfully"}), 200
    
    