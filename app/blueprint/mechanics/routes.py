from flask import jsonify, request
from marshmallow import ValidationError
from sqlalchemy import func, select

from app.blueprint.mechanics import mechanics_bp
from app.blueprint.mechanics.schemas import mechanic_schema, mechanics_schema, mechanic_login_schema
from app.models import Mechanics, db, service_mechanic
from app.utils.util import encode_token_mechanic, mechanic_token_required


@mechanics_bp.route('/login', methods=['POST'])
def mechanic_login():
    try:
        credentials = mechanic_login_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    mechanic = db.session.execute(
        select(Mechanics).where(Mechanics.email == credentials['email'])
    ).scalars().first()

    if mechanic and mechanic.password == credentials['password']:
        token = encode_token_mechanic(mechanic.id)
        return jsonify({'status': 'success', 'message': 'Login successful', 'auth_token': token}), 200

    return jsonify({'message': 'Invalid email or password'}), 401


@mechanics_bp.route('/', methods=['POST'])
def create_mechanic():
    try:
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    query = select(Mechanics).where(Mechanics.email == mechanic_data['email'])
    existing_mechanic = db.session.execute(query).scalars().first()
    if existing_mechanic:
        return jsonify({'error': 'Mechanic with this email already exists'}), 400

    new_mechanic = Mechanics(**mechanic_data)
    db.session.add(new_mechanic)
    db.session.commit()
    return mechanic_schema.jsonify(new_mechanic), 201


@mechanics_bp.route('/', methods=['GET'])
def get_mechanics():
    query = select(Mechanics)
    mechanics = db.session.execute(query).scalars().all()
    return mechanics_schema.jsonify(mechanics), 200


@mechanics_bp.route('/most-tickets', methods=['GET'])
def mechanics_most_tickets():
    # Left-join so mechanics with 0 tickets still appear at the bottom
    query = (
        select(Mechanics)
        .outerjoin(service_mechanic, Mechanics.id == service_mechanic.c.mechanic_id)
        .group_by(Mechanics.id)
        .order_by(func.count(service_mechanic.c.ticket_id).desc())
    )
    mechanics = db.session.execute(query).scalars().all()
    return mechanics_schema.jsonify(mechanics), 200


@mechanics_bp.route('/<int:id>', methods=['PUT'])
@mechanic_token_required
def update_mechanic(current_mechanic_id, id):
    mechanic = db.session.get(Mechanics, id)
    if not mechanic:
        return jsonify({'error': 'Mechanic not found'}), 404

    try:
        mechanic_data = mechanic_schema.load(request.json, partial=True)
    except ValidationError as e:
        return jsonify(e.messages), 400

    if 'email' in mechanic_data:
        query = select(Mechanics).where(Mechanics.email == mechanic_data['email'], Mechanics.id != id)
        existing_mechanic = db.session.execute(query).scalars().first()
        if existing_mechanic:
            return jsonify({'error': 'Mechanic with this email already exists'}), 400

    for key, value in mechanic_data.items():
        setattr(mechanic, key, value)

    db.session.commit()
    return mechanic_schema.jsonify(mechanic), 200


@mechanics_bp.route('/<int:id>', methods=['DELETE'])
@mechanic_token_required
def delete_mechanic(current_mechanic_id, id):
    mechanic = db.session.get(Mechanics, id)
    if not mechanic:
        return jsonify({'error': 'Mechanic not found'}), 404

    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({'message': 'Mechanic deleted successfully'}), 200
