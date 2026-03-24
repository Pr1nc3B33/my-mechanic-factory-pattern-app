from flask import jsonify, request
from marshmallow import ValidationError
from sqlalchemy import select

from app.blueprint.service_tickets import service_tickets_bp
from app.blueprint.service_tickets.schemas import (
    service_ticket_schema,
    service_tickets_schema,
)
from app.models import Customer, Mechanics, Service_Tickets, db


@service_tickets_bp.route('/', methods=['POST'])
def create_service_ticket():
    try:
        ticket_data = service_ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    customer = db.session.get(Customer, ticket_data['customer_id'])
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404

    new_ticket = Service_Tickets(**ticket_data)
    db.session.add(new_ticket)
    db.session.commit()
    return service_ticket_schema.jsonify(new_ticket), 201


@service_tickets_bp.route('/<int:ticket_id>/assign-mechanic/<int:mechanic_id>', methods=['PUT'])
def assign_mechanic(ticket_id, mechanic_id):
    ticket = db.session.get(Service_Tickets, ticket_id)
    if not ticket:
        return jsonify({'error': 'Service ticket not found'}), 404

    mechanic = db.session.get(Mechanics, mechanic_id)
    if not mechanic:
        return jsonify({'error': 'Mechanic not found'}), 404

    if mechanic in ticket.mechanic:
        return jsonify({'error': 'Mechanic already assigned to this ticket'}), 400

    ticket.mechanic.append(mechanic)
    db.session.commit()
    return service_ticket_schema.jsonify(ticket), 200


@service_tickets_bp.route('/<int:ticket_id>/remove-mechanic/<int:mechanic_id>', methods=['PUT'])
def remove_mechanic(ticket_id, mechanic_id):
    ticket = db.session.get(Service_Tickets, ticket_id)
    if not ticket:
        return jsonify({'error': 'Service ticket not found'}), 404

    mechanic = db.session.get(Mechanics, mechanic_id)
    if not mechanic:
        return jsonify({'error': 'Mechanic not found'}), 404

    if mechanic not in ticket.mechanic:
        return jsonify({'error': 'Mechanic is not assigned to this ticket'}), 400

    ticket.mechanic.remove(mechanic)
    db.session.commit()
    return service_ticket_schema.jsonify(ticket), 200


@service_tickets_bp.route('/', methods=['GET'])
def get_service_tickets():
    query = select(Service_Tickets)
    tickets = db.session.execute(query).scalars().all()
    return service_tickets_schema.jsonify(tickets), 200
