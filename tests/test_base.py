import unittest
from datetime import date

from app import create_app
from app.models import Customer, Inventory, Mechanics, Service_Tickets, db


class BaseAPITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('TestingConfig')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()
        self.counter = 0

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        db.engine.dispose()
        self.app_context.pop()

    def _unique(self, prefix='user'):
        self.counter += 1
        return f"{prefix}{self.counter}"

    def seed_customer(self, email=None):
        token = self._unique('cust')
        customer = Customer(
            name=f"Customer {token}",
            phone='555-000-0000',
            email=email or f"{token}@example.com",
            password='password123',
        )
        db.session.add(customer)
        db.session.commit()
        return customer

    def seed_mechanic(self, email=None):
        token = self._unique('mech')
        mechanic = Mechanics(
            name=f"Mechanic {token}",
            email=email or f"{token}@example.com",
            phone='555-111-1111',
            salary=65000.0,
            password='password123',
        )
        db.session.add(mechanic)
        db.session.commit()
        return mechanic

    def seed_inventory(self):
        token = self._unique('part')
        part = Inventory(name=f"Part {token}", price=24.99)
        db.session.add(part)
        db.session.commit()
        return part

    def seed_ticket(self, customer_id=None):
        if customer_id is None:
            customer = self.seed_customer()
            customer_id = customer.id

        ticket = Service_Tickets(
            customer_id=customer_id,
            service_date=date(2026, 4, 1),
            service_type='Oil Change',
            vin='1HGCM82633A004352',
        )
        db.session.add(ticket)
        db.session.commit()
        return ticket

    def customer_token(self, email, password='password123'):
        response = self.client.post(
            '/customers/login',
            json={'email': email, 'password': password},
        )
        data = response.get_json()
        return data.get('auth_token') if data else None

    def mechanic_token(self, email, password='password123'):
        response = self.client.post(
            '/mechanics/login',
            json={'email': email, 'password': password},
        )
        data = response.get_json()
        return data.get('auth_token') if data else None

    @staticmethod
    def auth_header(token):
        return {'Authorization': f'Bearer {token}'}
