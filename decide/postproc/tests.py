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
    
    def testImperialiFunciona(self):
        #Test de ejemplo
        data = {
            'type': 'IMPERIALI',
            'options': [
                { 'option': 'A', 'number': 1, 'votes': 391000 },
                { 'option': 'B', 'number': 2, 'votes': 311000 },
                { 'option': 'C', 'number': 3, 'votes': 184000 },
                { 'option': 'D', 'number': 4, 'votes': 73000 },
                { 'option': 'E', 'number': 5, 'votes': 27000 },
                { 'option': 'F', 'number': 6, 'votes': 12000 },
                { 'option': 'G', 'number': 7, 'votes': 2000 },
            ],
            'numEscanos': 21,
        }

        expected_result = [
            { 'option': 'A', 'number': 1, 'votes': 391000, 'escanosImp': 9},
            { 'option': 'B', 'number': 2, 'votes': 311000, 'escanosImp': 7},
            { 'option': 'C', 'number': 3, 'votes': 184000, 'escanosImp': 4},
            { 'option': 'D', 'number': 4, 'votes': 73000, 'escanosImp': 1},
            { 'option': 'E', 'number': 5, 'votes': 27000, 'escanosImp': 0},
            { 'option': 'F', 'number': 6, 'votes': 12000, 'escanosImp': 0},
            { 'option': 'G', 'number': 7, 'votes': 2000, 'escanosImp': 0},
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)


    def testHuntington(self):
        data = {
            'type': 'HUNTINGTONHILL',
            'options': [
                {'option':'PP','number':1,'votes': 100000},
                {'option':'PSOE', 'number':2,'votes': 80000},
                {'option':'Podemos', 'number':3,'votes': 30000},
                {'option':'Cs', 'number':4,'votes': 20000}
            ],
            'numEscanos': 8
        }

        expected_result = [
            {'option':'PP','number':1,'votes': 100000,'escanos':4},
            {'option':'PSOE', 'number':2,'votes': 80000,'escanos':3},
            {'option':'Podemos', 'number':3,'votes': 30000,'escanos':1},
            {'option':'Cs', 'number':4,'votes': 20000,'escanos':0}
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def testDHont(self):
        data = {
            'type': 'DHONT',
            'options': [
                {'option':'OPT1','number':1,'votes': 12000},
                {'option':'OPT2','number':2,'votes': 140000},
                {'option':'OPT3','number':3,'votes': 110000},
                {'option':'OPT4','number':4,'votes': 205000},
                {'option':'OPT5','number':5,'votes': 150000},
                {'option':'OPT6','number':6,'votes': 16000}
            ],
            'numEscanos': 10
        }

        expected_result = [
            {'option':'OPT1','number':1,'votes': 12000, 'escanos': 0},
            {'option':'OPT2','number':2,'votes': 140000, 'escanos': 2},
            {'option':'OPT3','number':3,'votes': 110000, 'escanos': 2},
            {'option':'OPT4','number':4,'votes': 205000, 'escanos': 4},
            {'option':'OPT5','number':5,'votes': 150000, 'escanos': 2},
            {'option':'OPT6','number':6,'votes': 16000, 'escanos': 0}
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)