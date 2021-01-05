from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from base import mods


class PostProcTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        mods.mock_query(self.client)

    def tearDown(self):
        self.client = None

    def test_identity(self):
        data = {
            'type': 'IDENTITY',
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 5 },
                { 'option': 'Option 2', 'number': 2, 'votes': 0 },
                { 'option': 'Option 3', 'number': 3, 'votes': 3 },
                { 'option': 'Option 4', 'number': 4, 'votes': 2 },
                { 'option': 'Option 5', 'number': 5, 'votes': 5 },
                { 'option': 'Option 6', 'number': 6, 'votes': 1 },
            ]
        }

        expected_result = [
            { 'option': 'Option 1', 'number': 1, 'votes': 5, 'postproc': 5 },
            { 'option': 'Option 5', 'number': 5, 'votes': 5, 'postproc': 5 },
            { 'option': 'Option 3', 'number': 3, 'votes': 3, 'postproc': 3 },
            { 'option': 'Option 4', 'number': 4, 'votes': 2, 'postproc': 2 },
            { 'option': 'Option 6', 'number': 6, 'votes': 1, 'postproc': 1 },
            { 'option': 'Option 2', 'number': 2, 'votes': 0, 'postproc': 0 },
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    
    def test_saintelague(self):
        data = {
            'type': 'SAINTELAGUE',
            'escanos': 7,
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 340000 },
                { 'option': 'Option 2', 'number': 2, 'votes': 280000 },
                { 'option': 'Option 3', 'number': 3, 'votes': 160000 },
                { 'option': 'Option 4', 'number': 4, 'votes': 60000 },
            ]
        }

        expected_result = {
            'results': [
            { 'option': 'Option 1', 'number': 1, 'votes': 340000, 'postproc': 3 },
            { 'option': 'Option 2', 'number': 2, 'votes': 280000, 'postproc': 2 },
            { 'option': 'Option 3', 'number': 3, 'votes': 160000, 'postproc': 1 },
            { 'option': 'Option 4', 'number': 4, 'votes': 60000, 'postproc': 1 },
            ]
        }
        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_saintelague2(self):
        data = {
            'type': 'SAINTELAGUE',
            'escanos': 5,
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 20 },
                { 'option': 'Option 2', 'number': 2, 'votes': 60 },
                { 'option': 'Option 3', 'number': 3, 'votes': 10 },
            ]
        }

        expected_result = {
            'results': [
            { 'option': 'Option 2', 'number': 2, 'votes': 60, 'postproc': 3 },
            { 'option': 'Option 1', 'number': 1, 'votes': 20, 'postproc': 1 },
            { 'option': 'Option 3', 'number': 3, 'votes': 10, 'postproc': 1 },
            ]
        }
        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_saintelague3(self):
        data = {
            'type': 'SAINTELAGUE',
            'escanos': 4,
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 1000 },
                { 'option': 'Option 2', 'number': 2, 'votes': 800 },
                { 'option': 'Option 3', 'number': 3, 'votes': 750 },
                { 'option': 'Option 4', 'number': 4, 'votes': 600 },
                { 'option': 'Option 5', 'number': 5, 'votes': 350 },
            ]
        }

        expected_result = {
            'results': [
            { 'option': 'Option 1', 'number': 1, 'votes': 1000, 'postproc': 1 },
            { 'option': 'Option 2', 'number': 2, 'votes': 800, 'postproc': 1 },
            { 'option': 'Option 3', 'number': 3, 'votes': 750, 'postproc': 1 },
            { 'option': 'Option 4', 'number': 4, 'votes': 600, 'postproc': 1 },
            { 'option': 'Option 5', 'number': 5, 'votes': 350, 'postproc': 0 },
            ]
        }
        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)
