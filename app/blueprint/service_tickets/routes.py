from flask import jsonify, request
from marshmallow import ValidationError
from sqlalchemy import select

from app.blueprint.service_tickets import service_tickets_bp
from app.blueprint.service_tickets.schemas import (
    service_ticket_schema,
    service_tickets_schema,
)
from app.models import Customer, Inventory, Mechanics, Service_Tickets, Ticket_Inventory, db
from app.utils.util import mechanic_token_required


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
@mechanic_token_required
def assign_mechanic(current_mechanic_id, ticket_id, mechanic_id):
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
@mechanic_token_required
def remove_mechanic(current_mechanic_id, ticket_id, mechanic_id):
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


@service_tickets_bp.route('/<int:ticket_id>/edit', methods=['PUT'])
@mechanic_token_required
def edit_ticket_mechanics(current_mechanic_id, ticket_id):
    ticket = db.session.get(Service_Tickets, ticket_id)
    if not ticket:
        return jsonify({'error': 'Service ticket not found'}), 404

    data = request.json or {}
    add_ids = data.get('add_ids', [])
    remove_ids = data.get('remove_ids', [])

    warnings = []

    for mid in add_ids:
        mechanic = db.session.get(Mechanics, mid)
        if not mechanic:
            warnings.append(f'Mechanic {mid} not found, skipped')
            continue
        if mechanic not in ticket.mechanic:
            ticket.mechanic.append(mechanic)

    for mid in remove_ids:
        mechanic = db.session.get(Mechanics, mid)
        if not mechanic:
            warnings.append(f'Mechanic {mid} not found, skipped')
            continue
        if mechanic in ticket.mechanic:
            ticket.mechanic.remove(mechanic)

    db.session.commit()
    response = service_ticket_schema.dump(ticket)
    if warnings:
        response['warnings'] = warnings
    return jsonify(response), 200


@service_tickets_bp.route('/<int:ticket_id>/add-part/<int:inventory_id>', methods=['POST'])
@mechanic_token_required
def add_part_to_ticket(current_mechanic_id, ticket_id, inventory_id):
    ticket = db.session.get(Service_Tickets, ticket_id)
    if not ticket:
        return jsonify({'error': 'Service ticket not found'}), 404

    part = db.session.get(Inventory, inventory_id)
    if not part:
        return jsonify({'error': 'Part not found'}), 404

    quantity = (request.json or {}).get('quantity', 1)

    existing = db.session.get(Ticket_Inventory, {'ticket_id': ticket_id, 'inventory_id': inventory_id})
    if existing:
        existing.quantity += quantity
    else:
        ticket_part = Ticket_Inventory(ticket_id=ticket_id, inventory_id=inventory_id, quantity=quantity)
        db.session.add(ticket_part)

    db.session.commit()
    return service_ticket_schema.jsonify(ticket), 200


@service_tickets_bp.route('/', methods=['GET'])
def get_service_tickets():
    query = select(Service_Tickets)
    tickets = db.session.execute(query).scalars().all()
    return service_tickets_schema.jsonify(tickets), 200
