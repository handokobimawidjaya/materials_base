import unittest
import json
from odoo.tests.common import HttpCase

class TestMasterMaterialsAPI(HttpCase):
    def test_get_master_materials(self):
        response = self.url_open('/api/get_master_materials?type=fabric')

        # Check if response status code is 200
        self.assertEqual(response.status_code, 200)

        # Decode response content
        content = response.read().decode('utf-8')
        data = json.loads(content)

        # Check if response contains status, message, and data keys
        self.assertIn('status', data)
        self.assertIn('message', data)
        self.assertIn('data', data)

        # Check if status is 1 (success)
        self.assertEqual(data['status'], 1)

        # Check if message is 'success'
        self.assertEqual(data['message'], 'success')

        # Check if data is a non-empty list
        self.assertIsInstance(data['data'], list)
        self.assertTrue(data['data'])

        # Check if each item in data has the required keys
        for item in data['data']:
            self.assertIn('name', item)
            self.assertIn('code', item)
            self.assertIn('type', item)
            self.assertIn('price', item)
            self.assertIn('supplier_id', item)
            self.assertIn('supplier_code', item)
            self.assertIn('supplier_name', item)

    def test_create_master_materials(self):
        request_data = {
            'data': [
                {
                    'type': 'fabric',
                    'code': 'M001',
                    'name': 'Fabric Material',
                    'price': 150,
                    'supplier_code': 'SUP001'
                },
                {
                    'type': 'jeans',
                    'code': 'M002',
                    'name': 'Jeans Material',
                    'price': 200,
                    'supplier_code': 'SUP002'
                }
            ]
        }

        # Simulate a POST request to the API endpoint
        response = self.url_open('/api/create_master_materials', data=json.dumps(request_data), method='POST')

        # Check if response status code is 200
        self.assertEqual(response.status_code, 200)

        # Decode response content
        content = response.read().decode('utf-8')
        data = json.loads(content)

        # Check if response contains status, message, and data keys
        self.assertIn('status', data)
        self.assertIn('message', data)
        self.assertIn('data', data)

        # Check if status is 1 (success)
        self.assertEqual(data['status'], 1)

        # Check if message is 'Success When Create Materials'
        self.assertEqual(data['message'], 'Success When Create Materials')

        # Check if data is a non-empty list
        self.assertIsInstance(data['data'], list)
        self.assertTrue(data['data'])

        # Check if each item in data has the required keys
        for item in data['data']:
            self.assertIn('transaction_id', item)
            self.assertIn('code', item)
            self.assertIn('name', item)

    def test_update_master_materials(self):
        request_data = {
            'transaction_code': 'M001',
            'name': 'Updated Fabric Material',
            'price': 200,
            'supplier_code': 'SUP002'
        }

        # Simulate a POST request to the API endpoint
        response = self.url_open('/api/update_master_materials', data=json.dumps(request_data), method='POST')

        # Check if response status code is 200
        self.assertEqual(response.status_code, 200)

        # Decode response content
        content = response.read().decode('utf-8')
        data = json.loads(content)

        # Check if response contains status, message, and data keys
        self.assertIn('status', data)
        self.assertIn('message', data)
        self.assertIn('data', data)

        # Check if status is 1 (success)
        self.assertEqual(data['status'], 1)

        # Check if message is 'Success Update Transaction'
        self.assertEqual(data['message'], 'Success Update Transaction')

        # Check if data contains transaction_code key
        self.assertIn('transaction_code', data['data'])

        # Check if transaction_code matches the one sent in the request
        self.assertEqual(data['data']['transaction_code'], 'M001')

    def test_delete_master_materials(self):
        request_data = {
            'transaction_code': 'M002'
        }

        # Simulate a POST request to the API endpoint
        response = self.url_open('/api/delete_master_materials', data=json.dumps(request_data), method='POST')

        # Check if response status code is 200
        self.assertEqual(response.status_code, 200)

        # Decode response content
        content = response.read().decode('utf-8')
        data = json.loads(content)

        # Check if response contains status, message, and data keys
        self.assertIn('status', data)
        self.assertIn('message', data)
        self.assertIn('data', data)

        # Check if status is 1 (success)
        self.assertEqual(data['status'], 1)

        # Check if message is 'Success Delete Transaction'
        self.assertEqual(data['message'], 'Success Delete Transaction')

        # Check if data is a non-empty list
        self.assertIsInstance(data['data'], list)
        self.assertTrue(data['data'])

        # Check if each item in data has the required keys
        for item in data['data']:
            self.assertIn('transaction_code', item)

        # Check if transaction_code matches the one sent in the request
        self.assertEqual(data['data'][0]['transaction_code'], 'M002')

if __name__ == '__main__':
    unittest.main()