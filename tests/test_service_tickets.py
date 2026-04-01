import unittest

from app.models import Ticket_Inventory, db
from tests.test_base import BaseAPITestCase


class TestServiceTicketRoutes(BaseAPITestCase):
    def test_create_service_ticket_success(self):
        customer = self.seed_customer()

        response = self.client.post(
            '/service-tickets/',
            json={
                'customer_id': customer.id,
                'service_date': '2026-04-01',
                'service_type': 'Transmission Check',
                'vin': '1HGCM82633A004352',
            },
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()['customer_id'], customer.id)

    def test_create_service_ticket_customer_not_found(self):
        response = self.client.post(
            '/service-tickets/',
            json={
                'customer_id': 9999,
                'service_date': '2026-04-01',
                'service_type': 'Transmission Check',
                'vin': '1HGCM82633A004352',
            },
        )

        self.assertEqual(response.status_code, 404)

    def test_get_service_tickets(self):
        customer = self.seed_customer()
        self.seed_ticket(customer_id=customer.id)

        response = self.client.get('/service-tickets/')

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)

    def test_assign_mechanic_success(self):
        customer = self.seed_customer()
        ticket = self.seed_ticket(customer_id=customer.id)
        mechanic = self.seed_mechanic(email='assign-mech@example.com')
        token = self.mechanic_token(mechanic.email)

        response = self.client.put(
            f'/service-tickets/{ticket.id}/assign-mechanic/{mechanic.id}',
            headers=self.auth_header(token),
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(mechanic.id, response.get_json().get('mechanic_ids', []))

    def test_assign_mechanic_missing_token(self):
        customer = self.seed_customer()
        ticket = self.seed_ticket(customer_id=customer.id)
        mechanic = self.seed_mechanic()

        response = self.client.put(
            f'/service-tickets/{ticket.id}/assign-mechanic/{mechanic.id}',
        )

        self.assertEqual(response.status_code, 401)

    def test_remove_mechanic_success(self):
        customer = self.seed_customer()
        ticket = self.seed_ticket(customer_id=customer.id)
        mechanic = self.seed_mechanic(email='remove-mech@example.com')
        ticket.mechanic.append(mechanic)
        db.session.commit()
        token = self.mechanic_token(mechanic.email)

        response = self.client.put(
            f'/service-tickets/{ticket.id}/remove-mechanic/{mechanic.id}',
            headers=self.auth_header(token),
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotIn(mechanic.id, response.get_json().get('mechanic_ids', []))

    def test_remove_mechanic_not_assigned(self):
        customer = self.seed_customer()
        ticket = self.seed_ticket(customer_id=customer.id)
        mechanic = self.seed_mechanic(email='not-assigned@example.com')
        token = self.mechanic_token(mechanic.email)

        response = self.client.put(
            f'/service-tickets/{ticket.id}/remove-mechanic/{mechanic.id}',
            headers=self.auth_header(token),
        )

        self.assertEqual(response.status_code, 400)

    def test_edit_ticket_mechanics_success_with_warning(self):
        customer = self.seed_customer()
        ticket = self.seed_ticket(customer_id=customer.id)
        mech_a = self.seed_mechanic(email='batch-a@example.com')
        mech_b = self.seed_mechanic(email='batch-b@example.com')
        ticket.mechanic.append(mech_a)
        db.session.commit()
        token = self.mechanic_token(mech_a.email)

        response = self.client.put(
            f'/service-tickets/{ticket.id}/edit',
            json={'add_ids': [mech_b.id, 9999], 'remove_ids': [mech_a.id]},
            headers=self.auth_header(token),
        )

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn(mech_b.id, data.get('mechanic_ids', []))
        self.assertIn('warnings', data)

    def test_edit_ticket_mechanics_missing_token(self):
        customer = self.seed_customer()
        ticket = self.seed_ticket(customer_id=customer.id)

        response = self.client.put(
            f'/service-tickets/{ticket.id}/edit',
            json={'add_ids': [], 'remove_ids': []},
        )

        self.assertEqual(response.status_code, 401)

    def test_add_part_to_ticket_success(self):
        customer = self.seed_customer()
        ticket = self.seed_ticket(customer_id=customer.id)
        mechanic = self.seed_mechanic(email='part-mech@example.com')
        part = self.seed_inventory()
        token = self.mechanic_token(mechanic.email)

        response = self.client.post(
            f'/service-tickets/{ticket.id}/add-part/{part.id}',
            json={'quantity': 2},
            headers=self.auth_header(token),
        )

        self.assertEqual(response.status_code, 200)
        link = db.session.get(Ticket_Inventory, {'ticket_id': ticket.id, 'inventory_id': part.id})
        self.assertIsNotNone(link)
        self.assertEqual(link.quantity, 2)

    def test_add_part_to_ticket_part_not_found(self):
        customer = self.seed_customer()
        ticket = self.seed_ticket(customer_id=customer.id)
        mechanic = self.seed_mechanic(email='part-missing@example.com')
        token = self.mechanic_token(mechanic.email)

        response = self.client.post(
            f'/service-tickets/{ticket.id}/add-part/9999',
            json={'quantity': 1},
            headers=self.auth_header(token),
        )

        self.assertEqual(response.status_code, 404)

    def test_add_part_to_ticket_missing_token(self):
        customer = self.seed_customer()
        ticket = self.seed_ticket(customer_id=customer.id)
        part = self.seed_inventory()

        response = self.client.post(
            f'/service-tickets/{ticket.id}/add-part/{part.id}',
            json={'quantity': 1},
        )

        self.assertEqual(response.status_code, 401)


if __name__ == '__main__':
    unittest.main()
