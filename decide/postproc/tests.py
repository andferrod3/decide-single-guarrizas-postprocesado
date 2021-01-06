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
    
    #Prueba 1 Imperiali con los datos de la Wikipedia
    def testImperialiFunciona(self):
        
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

    #Prueba 2 Imperiali con numEscanos=0   
    def testImperialiNoEscanos(self):
        
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
            'numEscanos': 0,
            
        }

        expected_result = [
            { 'option': 'A', 'number': 1, 'votes': 391000, 'escanosImp': 0},
            { 'option': 'B', 'number': 2, 'votes': 311000, 'escanosImp': 0},
            { 'option': 'C', 'number': 3, 'votes': 184000, 'escanosImp': 0},
            { 'option': 'D', 'number': 4, 'votes': 73000, 'escanosImp': 0},
            { 'option': 'E', 'number': 5, 'votes': 27000, 'escanosImp': 0},
            { 'option': 'F', 'number': 6, 'votes': 12000, 'escanosImp': 0},
            { 'option': 'G', 'number': 7, 'votes': 2000, 'escanosImp': 0},
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    #Prueba 3 Imperiali sin pasarle el numEscanos
    def testImperialiSinPasarEscanos(self):
        
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
            
            
        }

        expected_result = [
            { 'option': 'A', 'number': 1, 'votes': 391000, 'escanosImp': 0},
            { 'option': 'B', 'number': 2, 'votes': 311000, 'escanosImp': 0},
            { 'option': 'C', 'number': 3, 'votes': 184000, 'escanosImp': 0},
            { 'option': 'D', 'number': 4, 'votes': 73000, 'escanosImp': 0},
            { 'option': 'E', 'number': 5, 'votes': 27000, 'escanosImp': 0},
            { 'option': 'F', 'number': 6, 'votes': 12000, 'escanosImp': 0},
            { 'option': 'G', 'number': 7, 'votes': 2000, 'escanosImp': 0},
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    #Prueba 4 Imperiali sin votos
    def testImperialiCon0Votos(self):
        
        data = {
            'type': 'IMPERIALI',
            'options': [
                { 'option': 'A', 'number': 1, 'votes': 0 },
                { 'option': 'B', 'number': 2, 'votes': 0 },
                { 'option': 'C', 'number': 3, 'votes': 0 },
                { 'option': 'D', 'number': 4, 'votes': 0 },
                { 'option': 'E', 'number': 5, 'votes': 0 },
                { 'option': 'F', 'number': 6, 'votes': 0 },
                { 'option': 'G', 'number': 7, 'votes': 0 },
            ],
            'numEscanos': 21,
            
        }

        expected_result = [
            { 'option': 'A', 'number': 1, 'votes': 0, 'escanosImp': 0},
            { 'option': 'B', 'number': 2, 'votes': 0, 'escanosImp': 0},
            { 'option': 'C', 'number': 3, 'votes': 0, 'escanosImp': 0},
            { 'option': 'D', 'number': 4, 'votes': 0, 'escanosImp': 0},
            { 'option': 'E', 'number': 5, 'votes': 0, 'escanosImp': 0},
            { 'option': 'F', 'number': 6, 'votes': 0, 'escanosImp': 0},
            { 'option': 'G', 'number': 7, 'votes': 0, 'escanosImp': 0},
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    #Prueba 5 Imperiali sin votos sin escanos
    def testImperialiCon0Votos0Escanos(self):
        
        data = {
            'type': 'IMPERIALI',
            'options': [
                { 'option': 'A', 'number': 1, 'votes': 0 },
                { 'option': 'B', 'number': 2, 'votes': 0 },
                { 'option': 'C', 'number': 3, 'votes': 0 },
                { 'option': 'D', 'number': 4, 'votes': 0 },
                { 'option': 'E', 'number': 5, 'votes': 0 },
                { 'option': 'F', 'number': 6, 'votes': 0 },
                { 'option': 'G', 'number': 7, 'votes': 0 },
            ],
            'numEscanos': 0,
            
        }

        expected_result = [
            { 'option': 'A', 'number': 1, 'votes': 0, 'escanosImp': 0},
            { 'option': 'B', 'number': 2, 'votes': 0, 'escanosImp': 0},
            { 'option': 'C', 'number': 3, 'votes': 0, 'escanosImp': 0},
            { 'option': 'D', 'number': 4, 'votes': 0, 'escanosImp': 0},
            { 'option': 'E', 'number': 5, 'votes': 0, 'escanosImp': 0},
            { 'option': 'F', 'number': 6, 'votes': 0, 'escanosImp': 0},
            { 'option': 'G', 'number': 7, 'votes': 0, 'escanosImp': 0},
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    #Prueba 6 Imperiali sin opciones    
    def testImperialiSinOpciones(self):
        
        data = {
            'type': 'IMPERIALI',
            'options': [
            ],
            'numEscanos': 21,
            
        }

        expected_result = [
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

   #Prueba 8 Imperiali mismos votos
    def testImperialiConMismosVotos(self):
        
        data = {
            'type': 'IMPERIALI',
            'options': [
                { 'option': 'A', 'number': 1, 'votes': 1000 },
                { 'option': 'B', 'number': 2, 'votes': 1000 },

            ],
            'numEscanos': 20,
            
        }

        expected_result = [
            { 'option': 'A', 'number': 1, 'votes': 1000, 'escanosImp': 10},
            { 'option': 'B', 'number': 2, 'votes': 1000, 'escanosImp': 10},

        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)
