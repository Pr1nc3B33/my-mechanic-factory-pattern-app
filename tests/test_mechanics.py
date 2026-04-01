import unittest

from app.models import db
from tests.test_base import BaseAPITestCase


class TestMechanicsRoutes(BaseAPITestCase):
    def test_login_success(self):
        mechanic = self.seed_mechanic(email='mech-login@example.com')

        response = self.client.post(
            '/mechanics/login',
            json={'email': mechanic.email, 'password': 'password123'},
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn('auth_token', response.get_json())

    def test_login_invalid_credentials(self):
        self.seed_mechanic(email='mech-login-fail@example.com')

        response = self.client.post(
            '/mechanics/login',
            json={'email': 'mech-login-fail@example.com', 'password': 'wrong'},
        )

        self.assertEqual(response.status_code, 401)

    def test_create_mechanic_success(self):
        payload = {
            'name': 'Mechanic New',
            'email': 'new-mech@example.com',
            'phone': '555-777-8888',
            'salary': 75000,
            'password': 'password123',
        }

        response = self.client.post('/mechanics/', json=payload)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()['email'], payload['email'])

    def test_create_mechanic_duplicate_email(self):
        self.seed_mechanic(email='duplicate-mech@example.com')

        response = self.client.post(
            '/mechanics/',
            json={
                'name': 'Duplicate',
                'email': 'duplicate-mech@example.com',
                'phone': '555-111-2222',
                'salary': 70000,
                'password': 'password123',
            },
        )

        self.assertEqual(response.status_code, 400)

    def test_get_mechanics(self):
        self.seed_mechanic()
        self.seed_mechanic()

        response = self.client.get('/mechanics/')

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)

    def test_mechanics_most_tickets(self):
        customer = self.seed_customer()
        mechanic_a = self.seed_mechanic(email='rank-a@example.com')
        mechanic_b = self.seed_mechanic(email='rank-b@example.com')

        ticket1 = self.seed_ticket(customer_id=customer.id)
        ticket2 = self.seed_ticket(customer_id=customer.id)
        ticket1.mechanic.append(mechanic_a)
        ticket2.mechanic.append(mechanic_a)
        ticket2.mechanic.append(mechanic_b)
        db.session.commit()

        response = self.client.get('/mechanics/most-tickets')

        self.assertEqual(response.status_code, 200)
        ranked = response.get_json()
        self.assertGreaterEqual(len(ranked), 2)

    def test_update_mechanic_success(self):
        mechanic = self.seed_mechanic(email='update-mech@example.com')
        token = self.mechanic_token(mechanic.email)

        response = self.client.put(
            f'/mechanics/{mechanic.id}',
            json={'salary': 90000},
            headers=self.auth_header(token),
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['salary'], 90000.0)

    def test_update_mechanic_missing_token(self):
        mechanic = self.seed_mechanic()

        response = self.client.put(
            f'/mechanics/{mechanic.id}',
            json={'salary': 88000},
        )

        self.assertEqual(response.status_code, 401)

    def test_delete_mechanic_success(self):
        mechanic = self.seed_mechanic(email='delete-mech@example.com')
        token = self.mechanic_token(mechanic.email)

        response = self.client.delete(
            f'/mechanics/{mechanic.id}',
            headers=self.auth_header(token),
        )

        self.assertEqual(response.status_code, 200)

    def test_delete_mechanic_not_found(self):
        mechanic = self.seed_mechanic(email='delete-mech-notfound@example.com')
        token = self.mechanic_token(mechanic.email)

        response = self.client.delete(
            '/mechanics/9999',
            headers=self.auth_header(token),
        )

        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
