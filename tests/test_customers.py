import unittest

from tests.test_base import BaseAPITestCase


class TestCustomersRoutes(BaseAPITestCase):
    def test_login_success(self):
        customer = self.seed_customer(email='login-success@example.com')

        response = self.client.post(
            '/customers/login',
            json={'email': customer.email, 'password': 'password123'},
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn('auth_token', response.get_json())

    def test_login_invalid_credentials(self):
        self.seed_customer(email='login-fail@example.com')

        response = self.client.post(
            '/customers/login',
            json={'email': 'login-fail@example.com', 'password': 'bad-password'},
        )

        self.assertEqual(response.status_code, 401)

    def test_get_customers(self):
        self.seed_customer()
        self.seed_customer()

        response = self.client.get('/customers/?page=1&per_page=10')

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)

    def test_create_customer_success(self):
        payload = {
            'name': 'New Customer',
            'phone': '555-333-4444',
            'email': 'create-customer@example.com',
            'password': 'password123',
        }

        response = self.client.post('/customers/', json=payload)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()['email'], payload['email'])

    def test_create_customer_duplicate_email(self):
        self.seed_customer(email='duplicate-customer@example.com')

        response = self.client.post(
            '/customers/',
            json={
                'name': 'Duplicate Customer',
                'phone': '555-123-1234',
                'email': 'duplicate-customer@example.com',
                'password': 'password123',
            },
        )

        self.assertEqual(response.status_code, 400)

    def test_get_customer_success(self):
        customer = self.seed_customer()

        response = self.client.get(f'/customers/{customer.id}')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['id'], customer.id)

    def test_get_customer_not_found(self):
        response = self.client.get('/customers/9999')

        self.assertEqual(response.status_code, 404)

    def test_get_my_tickets_with_token(self):
        customer = self.seed_customer(email='ticket-owner@example.com')
        self.seed_ticket(customer_id=customer.id)
        token = self.customer_token(customer.email)

        response = self.client.get(
            '/customers/my-tickets',
            headers=self.auth_header(token),
        )

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)

    def test_get_my_tickets_missing_token(self):
        response = self.client.get('/customers/my-tickets')

        self.assertEqual(response.status_code, 401)

    def test_update_customer_success(self):
        customer = self.seed_customer(email='update-customer@example.com')
        token = self.customer_token(customer.email)

        response = self.client.put(
            f'/customers/{customer.id}',
            json={'name': 'Updated Customer'},
            headers=self.auth_header(token),
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['name'], 'Updated Customer')

    def test_update_customer_missing_token(self):
        customer = self.seed_customer()

        response = self.client.put(
            f'/customers/{customer.id}',
            json={'name': 'Should Fail'},
        )

        self.assertEqual(response.status_code, 401)

    def test_delete_customer_success(self):
        customer = self.seed_customer(email='delete-customer@example.com')
        token = self.customer_token(customer.email)

        response = self.client.delete(
            f'/customers/{customer.id}',
            headers=self.auth_header(token),
        )

        self.assertEqual(response.status_code, 200)

    def test_delete_customer_not_found(self):
        customer = self.seed_customer(email='delete-customer-notfound@example.com')
        token = self.customer_token(customer.email)

        response = self.client.delete(
            '/customers/9999',
            headers=self.auth_header(token),
        )

        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
