import unittest

from tests.test_base import BaseAPITestCase


class TestInventoryRoutes(BaseAPITestCase):
    def test_create_part_success(self):
        response = self.client.post(
            '/inventory/',
            json={'name': 'Air Filter', 'price': 19.99},
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()['name'], 'Air Filter')

    def test_create_part_invalid_payload(self):
        response = self.client.post('/inventory/', json={'name': 'No Price'})

        self.assertEqual(response.status_code, 400)

    def test_get_parts(self):
        self.seed_inventory()
        self.seed_inventory()

        response = self.client.get('/inventory/')

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)

    def test_get_part_success(self):
        part = self.seed_inventory()

        response = self.client.get(f'/inventory/{part.id}')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['id'], part.id)

    def test_get_part_not_found(self):
        response = self.client.get('/inventory/9999')

        self.assertEqual(response.status_code, 404)

    def test_update_part_success(self):
        part = self.seed_inventory()

        response = self.client.put(
            f'/inventory/{part.id}',
            json={'name': 'Updated Part', 'price': 29.99},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['name'], 'Updated Part')

    def test_update_part_not_found(self):
        response = self.client.put('/inventory/9999', json={'price': 10.0})

        self.assertEqual(response.status_code, 404)

    def test_delete_part_success(self):
        part = self.seed_inventory()

        response = self.client.delete(f'/inventory/{part.id}')

        self.assertEqual(response.status_code, 200)

    def test_delete_part_not_found(self):
        response = self.client.delete('/inventory/9999')

        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
