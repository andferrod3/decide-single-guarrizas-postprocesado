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


    def test_multi_preguntas1(self):
        data = {
            'type': 'MULTIPREGUNTAS',
            'questions': [
                [
                    { 'option': 'Option 1', 'number': 1, 'votes': 7 },
                    { 'option': 'Option 2', 'number': 2, 'votes': 2 },
                    { 'option': 'Option 3', 'number': 3, 'votes': 0 },
                    { 'option': 'Option 4', 'number': 4, 'votes': 9 }
                ],
                [
                    { 'option': 'Option 1', 'number': 1, 'votes': 0 },
                    { 'option': 'Option 2', 'number': 2, 'votes': 4 },
                    { 'option': 'Option 3', 'number': 3, 'votes': 6 },
                    { 'option': 'Option 4', 'number': 4, 'votes': 1 },
                    { 'option': 'Option 5', 'number': 5, 'votes': 7 }
                ],
            ]
        }

        expected_result = [
            [
                    { 'option': 'Option 4', 'number': 4, 'votes': 9, 'postproc': 9 },
                    { 'option': 'Option 1', 'number': 1, 'votes': 7, 'postproc': 7 },
                    { 'option': 'Option 2', 'number': 2, 'votes': 2, 'postproc': 2 },
                    { 'option': 'Option 3', 'number': 3, 'votes': 0, 'postproc': 0 }
                ],
                [
                    { 'option': 'Option 5', 'number': 5, 'votes': 7, 'postproc': 7 },
                    { 'option': 'Option 3', 'number': 3, 'votes': 6, 'postproc': 6 },
                    { 'option': 'Option 2', 'number': 2, 'votes': 4, 'postproc': 4 },
                    { 'option': 'Option 4', 'number': 4, 'votes': 1, 'postproc': 1 },
                    { 'option': 'Option 1', 'number': 1, 'votes': 0, 'postproc': 0 }
                ],
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)
        
    def test_multi_preguntas2(self):
        data = {
            'type': 'MULTIPREGUNTAS',
            'questions': [
                [
                    { 'option': 'Option 1', 'number': 1, 'votes': 2 },
                    { 'option': 'Option 2', 'number': 2, 'votes': 6 },
                    { 'option': 'Option 3', 'number': 3, 'votes': 3 }
                ],
                [
                    { 'option': 'Option 1', 'number': 1, 'votes': 1 },
                    { 'option': 'Option 2', 'number': 2, 'votes': 4 },
                    { 'option': 'Option 3', 'number': 3, 'votes': 3 },
                    { 'option': 'Option 4', 'number': 4, 'votes': 1 },
                    { 'option': 'Option 5', 'number': 5, 'votes': 2 },
                    { 'option': 'Option 6', 'number': 6, 'votes': 0 }
                ],
                [
                    { 'option': 'Option 1', 'number': 1, 'votes': 3 },
                    { 'option': 'Option 2', 'number': 2, 'votes': 8 },
                    { 'option': 'Option 3', 'number': 3, 'votes': 0 },
                    { 'option': 'Option 4', 'number': 4, 'votes': 0 }
                ],
            ]
        }

        expected_result = [
            [
                    { 'option': 'Option 2', 'number': 2, 'votes': 6, 'postproc': 6 },
                    { 'option': 'Option 3', 'number': 3, 'votes': 3, 'postproc': 3 },
                    { 'option': 'Option 1', 'number': 1, 'votes': 2, 'postproc': 2 }
                ],
                [
                    { 'option': 'Option 2', 'number': 2, 'votes': 4, 'postproc': 4 },
                    { 'option': 'Option 3', 'number': 3, 'votes': 3, 'postproc': 3 },
                    { 'option': 'Option 5', 'number': 5, 'votes': 2, 'postproc': 2 },
                    { 'option': 'Option 1', 'number': 1, 'votes': 1, 'postproc': 1 },
                    { 'option': 'Option 4', 'number': 4, 'votes': 1, 'postproc': 1 },
                    { 'option': 'Option 6', 'number': 6, 'votes': 0, 'postproc': 0 }
                ],
                [
                    { 'option': 'Option 2', 'number': 2, 'votes': 8, 'postproc': 8 },
                    { 'option': 'Option 1', 'number': 1, 'votes': 3, 'postproc': 3 },
                    { 'option': 'Option 3', 'number': 3, 'votes': 0, 'postproc': 0 },
                    { 'option': 'Option 4', 'number': 4, 'votes': 0, 'postproc': 0 }
                ],
        ]
          
        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)
        
        #test con preguntas vacías
    def test_multi_preguntas3(self):
        data = {
            'type': 'MULTIPREGUNTAS',
            'questions': [
                [  
                ],
                [  
                ],
            ]
        }

        expected_result = [
            [   
                ],
                [  
                ],
        ]
        
        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)
        
    def test_multi_preguntas4(self):
        data = {
            'type': 'MULTIPREGUNTAS',
            'questions': [
                [
                    { 'option': 'Rojo', 'number': 1, 'votes': 30 },
                    { 'option': 'Verde', 'number': 2, 'votes': 0 },
                    { 'option': 'Amarillo', 'number': 3, 'votes': 0 },
                    { 'option': 'Azul', 'number': 4, 'votes': 0 }
                ],
                [
                    { 'option': 'Sevilla', 'number': 1, 'votes': 20 },
                    { 'option': 'Betis', 'number': 2, 'votes': 0 },
                    { 'option': 'Barcelona', 'number': 3, 'votes': 2 },
                    { 'option': 'Madrid', 'number': 4, 'votes': 1 },
                    { 'option': 'Granada', 'number': 5, 'votes': 7 }
                ],
            ]
        }

        expected_result = [
            [
                    { 'option': 'Rojo', 'number': 1, 'votes': 30, 'postproc': 30 },
                    { 'option': 'Verde', 'number': 2, 'votes': 0, 'postproc': 0 },
                    { 'option': 'Amarillo', 'number': 3, 'votes': 0, 'postproc': 0 },
                    { 'option': 'Azul', 'number': 4, 'votes': 0, 'postproc': 0 }
                ],
                [
                    { 'option': 'Sevilla', 'number': 1, 'votes': 20, 'postproc': 20 },
                    { 'option': 'Granada', 'number': 5, 'votes': 7, 'postproc': 7 },
                    { 'option': 'Barcelona', 'number': 3, 'votes': 2, 'postproc': 2 },
                    { 'option': 'Madrid', 'number': 4, 'votes': 1, 'postproc': 1 },
                    { 'option': 'Betis', 'number': 2, 'votes': 0, 'postproc': 0 }
                ],
        ]
        
        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_multi_preguntas5(self):
        data = {
            'type': 'MULTIPREGUNTAS',
            'questions': [
                [
                    { 'option': 'A', 'number': 1, 'votes': 0 },
                    { 'option': 'B', 'number': 2, 'votes': 0 },
                    { 'option': 'C', 'number': 3, 'votes': 0 }
                ],
                [
                    { 'option': '1', 'number': 1, 'votes': 0 },
                    { 'option': '2', 'number': 2, 'votes': 0 },
                    { 'option': '3', 'number': 3, 'votes': 0 },
                    { 'option': '4', 'number': 4, 'votes': 0 }
                ],
            ]
        }

        expected_result = [
            [
                    { 'option': 'A', 'number': 1, 'votes': 0, 'postproc': 0 },
                    { 'option': 'B', 'number': 2, 'votes': 0, 'postproc': 0 },
                    { 'option': 'C', 'number': 3, 'votes': 0, 'postproc': 0 }
                ],
                [
                    { 'option': '1', 'number': 1, 'votes': 0, 'postproc': 0 },
                    { 'option': '2', 'number': 2, 'votes': 0, 'postproc': 0 },
                    { 'option': '3', 'number': 3, 'votes': 0, 'postproc': 0 },
                    { 'option': '4', 'number': 4, 'votes': 0, 'postproc': 0 }
                ],
        ]
        
        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_multi_preguntas6(self):
        data = {
            'type': 'MULTIPREGUNTAS',
            'questions': [
                [
                    { 'option': 'ALEJANDRO', 'number': 1, 'votes': 40 },
                    { 'option': 'PABLO', 'number': 2, 'votes': 10 }
                ],
                [
                    { 'option': 'CONCHA', 'number': 1, 'votes': 25 },
                    { 'option': 'CUBERO', 'number': 2, 'votes': 25}
                ],
                [
                    { 'option': 'JAVI', 'number': 1, 'votes': 24 },
                    { 'option': 'FERNANDO', 'number': 2, 'votes': 26 }
                ],
                [
                    { 'option': 'MANUEL', 'number': 1, 'votes': 50 },
                    { 'option': 'IKER', 'number': 2, 'votes': 0 }
                ],
            ]
        }

        expected_result = [
            [
                    { 'option': 'ALEJANDRO', 'number': 1, 'votes': 40, 'postproc': 40 },
                    { 'option': 'PABLO', 'number': 2, 'votes': 10, 'postproc': 10 }
                ],
                [
                    { 'option': 'CONCHA', 'number': 1, 'votes': 25, 'postproc': 25 },
                    { 'option': 'CUBERO', 'number': 2, 'votes': 25, 'postproc': 25 }
                ],
                [
                    { 'option': 'FERNANDO', 'number': 2, 'votes': 26, 'postproc': 26 },
                    { 'option': 'JAVI', 'number': 1, 'votes': 24, 'postproc': 24}
                ],
                [
                    { 'option': 'MANUEL', 'number': 1, 'votes': 50, 'postproc': 50 },
                    { 'option': 'IKER', 'number': 2, 'votes': 0, 'postproc': 0 }
                ],
        ]
        
        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

#normal
    def test_weight1(self):
        data = {
            'type': 'PREGUNTASPESO',
            'options': [
                    {'option': 'Option 1', 'number': 1, 'votes': 6, 'peso': 2},
                    {'option': 'Option 2', 'number': 2, 'votes': 15, 'peso': 2},
                    {'option': 'Option 3', 'number': 3, 'votes': 0, 'peso': 2}
                    ],
        }

        expected_result = [
                    {'option': 'Option 2', 'number': 2, 'votes': 15, 'peso': 2, 'postproc': 30},
                    {'option': 'Option 1', 'number': 1, 'votes': 6, 'peso': 2, 'postproc': 12},
                    {'option': 'Option 3', 'number': 3, 'votes': 0, 'peso': 2, 'postproc': 0}
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

#varios pesos
    def test_weight2(self):
        data = {
            'type': 'PREGUNTASPESO',
            'options': [
                    {'option': 'Option 1', 'number': 1, 'votes': 0, 'peso': 30},
                    {'option': 'Option 2', 'number': 2, 'votes': 10, 'peso': 10},
                    {'option': 'Option 3', 'number': 3, 'votes': 8, 'peso': 3},
                    {'option': 'Option 4', 'number': 4, 'votes': 5, 'peso': 1},
                    ],
        }

        expected_result = [
                    {'option': 'Option 2', 'number': 2, 'votes': 10, 'peso': 10, 'postproc': 100},
                    {'option': 'Option 3', 'number': 3, 'votes': 8, 'peso': 3, 'postproc': 24},
                    {'option': 'Option 4', 'number': 4, 'votes': 5, 'peso': 1, 'postproc': 5},
                    {'option': 'Option 1', 'number': 1, 'votes': 0, 'peso': 30, 'postproc': 0}
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    #con pesos negativos    
    def test_weight3(self):
        data = {
            'type': 'PREGUNTASPESO',
            'options': [
                    {'option': 'Option 1', 'number': 1, 'votes': 2, 'peso': -10},
                    {'option': 'Option 2', 'number': 2, 'votes': 60, 'peso': -2},
                    {'option': 'Option 3', 'number': 3, 'votes': 15, 'peso': 5},
                    {'option': 'Option 4', 'number': 4, 'votes': 1, 'peso': 20},
                    ],
        }

        expected_result = [
                    {'option': 'Option 3', 'number': 3, 'votes': 15, 'peso': 5, 'postproc': 75},
                    {'option': 'Option 4', 'number': 4, 'votes': 1, 'peso': 20, 'postproc': 20},
                    {'option': 'Option 1', 'number': 1, 'votes': 2, 'peso': -10, 'postproc': -20},
                    {'option': 'Option 2', 'number': 2, 'votes': 60, 'peso': -2, 'postproc': -120}
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)
    
    #con pesos a 0   
    def test_weight4(self):
        data = {
            'type': 'PREGUNTASPESO',
            'options': [
                    {'option': 'Option 1', 'number': 1, 'votes': 0, 'peso': 0},
                    {'option': 'Option 2', 'number': 2, 'votes': 25, 'peso': 0},
                    {'option': 'Option 3', 'number': 3, 'votes': 11, 'peso': 0}
                    ],
        }

        expected_result = [
                    {'option': 'Option 1', 'number': 1, 'votes': 0, 'peso': 0, 'postproc': 0},
                    {'option': 'Option 2', 'number': 2, 'votes': 25, 'peso': 0, 'postproc': 0},
                    {'option': 'Option 3', 'number': 3, 'votes': 11, 'peso': 0, 'postproc': 0}
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)
            
    #Prueba 1 Imperiali con los datos de la Wikipedia
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
            { 'option': 'A', 'number': 1, 'votes': 391000, 'postproc': 9},
            { 'option': 'B', 'number': 2, 'votes': 311000, 'postproc': 7},
            { 'option': 'C', 'number': 3, 'votes': 184000, 'postproc': 4},
            { 'option': 'D', 'number': 4, 'votes': 73000, 'postproc': 1},
            { 'option': 'E', 'number': 5, 'votes': 27000, 'postproc': 0},
            { 'option': 'F', 'number': 6, 'votes': 12000, 'postproc': 0},
            { 'option': 'G', 'number': 7, 'votes': 2000, 'postproc': 0},
        ]

        response = self.client.post("/postproc/", data, format="json")
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)


    def test_danish1(self):
        data = {
            "type": "DANISH",
            "options": [
                { "option": "Option 1", "number": 1, "votes": 25244},
                { "option": "Option 2", "number": 2, "votes": 45784},
                { "option": "Option 3", "number": 3, "votes": 101366}
            ], 
            'numEscanos': 3

        }

        expected_result = [
            { "option": "Option 1", "number": 1, "votes": 25244, "postproc": 0 },
            { "option": "Option 2", "number": 2, "votes": 45784, "postproc": 1 },
            { "option": "Option 3", "number": 3, "votes": 101366, "postproc": 2 }
        ]

        response = self.client.post("/postproc/", data, format="json")

        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)


    #Prueba 1 con datos de ej de Wikipedia

    def testHuntington(self):
        data = {
            'type': 'HUNTINGTONHILL',
            'options': [
                {'option':'Partido A','number':1,'votes': 100000},
                {'option':'Partido B', 'number':2,'votes': 80000},
                {'option':'Partido C', 'number':3,'votes': 30000},
                {'option':'Partido D', 'number':4,'votes': 20000}
            ],
            'numEscanos': 8
        }

        expected_result = [
            {'option':'Partido A','number':1,'votes': 100000,'postproc':4},
            {'option':'Partido B', 'number':2,'votes': 80000,'postproc':3},
            {'option':'Partido C', 'number':3,'votes': 30000,'postproc':1},
            {'option':'Partido D', 'number':4,'votes': 20000,'postproc':0}
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    #Prueba 2 con datos de otro ej de Wikipedia mas complejo
    def testHuntington2(self):
        data = {
            'type': 'HUNTINGTONHILL',
            'options': [
            {'option':'Likud','number':1,'votes': 985408},
            {'option':'Unión Sionista', 'number':2,'votes': 786313},
            {'option':'Lista Conjunta', 'number':3,'votes': 446583,},
            {'option':'Yesh Atid', 'number':4,'votes': 371602},
            {'option':'Kulanu', 'number':5,'votes': 315360},
            {'option':'La casa Judía', 'number':6,'votes': 283910},
            {'option':'Shas', 'number':7,'votes': 241613},
            {'option':'Yesh Atid', 'number':8,'votes': 214906},
            {'option':'Judaísmo Unido de la Torá', 'number':9,'votes': 210143},
            {'option':'Meretz', 'number':10,'votes': 165529}
            ],
            'numEscanos': 120
        }

        expected_result = [
            {'option':'Likud','number':1,'votes': 985408,'postproc':30},
            {'option':'Unión Sionista', 'number':2,'votes': 786313,'postproc':24},
            {'option':'Lista Conjunta', 'number':3,'votes': 446583,'postproc':13},
            {'option':'Yesh Atid', 'number':4,'votes': 371602,'postproc':11},
            {'option':'Kulanu', 'number':5,'votes': 315360,'postproc':9},
            {'option':'La casa Judía', 'number':6,'votes': 283910,'postproc':9},
            {'option':'Shas', 'number':7,'votes': 241613,'postproc':7},
            {'option':'Yesh Atid', 'number':8,'votes': 214906,'postproc':6},
            {'option':'Judaísmo Unido de la Torá', 'number':9,'votes': 210143,'postproc':6},
            {'option':'Meretz', 'number':10,'votes': 165529,'postproc':5}
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

     #Prueba 3 con muchos votos pero numeros de escanos a 0 
    def testHuntington3(self):
        data = {
            'type': 'HUNTINGTONHILL',
            'options': [
                {'option':'Partido A','number':1,'votes': 100000},
                {'option':'Partido B', 'number':2,'votes': 80000},
                {'option':'Partido C', 'number':3,'votes': 30000},
                {'option':'Partido D', 'number':4,'votes': 20000}
            ],
            'numEscanos': 0
        }

        expected_result = [
            {'option':'Partido A','number':1,'votes': 100000,'postproc':0},
            {'option':'Partido B', 'number':2,'votes': 80000,'postproc':0},
            {'option':'Partido C', 'number':3,'votes': 30000,'postproc':0},
            {'option':'Partido D', 'number':4,'votes': 20000,'postproc':0}

        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)


     #Prueba 4 con ningun voto pero numero de escanos mayor que 0 
    def testHuntington4(self):
        data = {
            'type': 'HUNTINGTONHILL',
            'options': [
                {'option':'Partido A','number':1,'votes': 0},
                {'option':'Partido B', 'number':2,'votes': 0},
                {'option':'Partido C', 'number':3,'votes': 0},
                {'option':'Partido D', 'number':4,'votes': 0}
            ],
            'numEscanos': 30
        }

        expected_result = [
            {'option':'Partido A','number':1,'votes': 0,'postproc':0},
            {'option':'Partido B', 'number':2,'votes': 0,'postproc':0},
            {'option':'Partido C', 'number':3,'votes': 0,'postproc':0},
            {'option':'Partido D', 'number':4,'votes': 0,'postproc':0}

        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)


    #Prueba 5 con votos a 0 y numero de escanos a 0 
    def testHuntington5(self):
        data = {
            'type': 'HUNTINGTONHILL',
            'options': [
                {'option':'Partido A','number':1,'votes': 0},
                {'option':'Partido B', 'number':2,'votes': 0},
                {'option':'Partido C', 'number':3,'votes': 0},
                {'option':'Partido D', 'number':4,'votes': 0}
            ],
            'numEscanos': 0
        }

        expected_result = [
            {'option':'Partido A','number':1,'votes': 0,'postproc':0},
            {'option':'Partido B', 'number':2,'votes': 0,'postproc':0},
            {'option':'Partido C', 'number':3,'votes': 0,'postproc':0},
            {'option':'Partido D', 'number':4,'votes': 0,'postproc':0}

        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def testHuntington6(self):
        data = {
            'type': 'HUNTINGTONHILL',
            'options': [
                {'option':'Partido A','number':1,'votes': -100000},
                {'option':'Partido B', 'number':2,'votes': -80000},
                {'option':'Partido C', 'number':3,'votes': -30000},
                {'option':'Partido D', 'number':4,'votes': -12000}
            ],
            'numEscanos': 20
        }

        expected_result = [
            {'option':'Partido A','number':1,'votes': -100000,'postproc':0},
            {'option':'Partido B', 'number':2,'votes': -80000,'postproc':0},
            {'option':'Partido C', 'number':3,'votes': -30000,'postproc':0},
            {'option':'Partido D', 'number':4,'votes': -12000,'postproc':0}

        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)


    #Prueba 7 con numeros escanos en negativo
    def testHuntington7(self):
        data = {
            'type': 'HUNTINGTONHILL',
            'options': [
                {'option':'Partido A','number':1,'votes': 100000},
                {'option':'Partido B', 'number':2,'votes': 80000},
                {'option':'Partido C', 'number':3,'votes': 30000},
                {'option':'Partido D', 'number':4,'votes': 12000}
            ],
            'numEscanos': -20
        }

        expected_result = [
            {'option':'Partido A','number':1,'votes': 100000,'postproc':0},
            {'option':'Partido B', 'number':2,'votes': 80000,'postproc':0},
            {'option':'Partido C', 'number':3,'votes': 30000,'postproc':0},
            {'option':'Partido D', 'number':4,'votes': 12000,'postproc':0}
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    #Prueba 8 con numEscanos sin pasar
    def testHuntington8(self):
        data = {
            'type': 'HUNTINGTONHILL',
            'options': [
                {'option':'Partido A','number':1,'votes': 100000},
                {'option':'Partido B', 'number':2,'votes': 80000},
                {'option':'Partido C', 'number':3,'votes': 30000},
                {'option':'Partido D', 'number':4,'votes': 12000}
            ],
            #'numEscanos': 200
        }

        expected_result = [
            {'option':'Partido A','number':1,'votes': 100000,'postproc':0},
            {'option':'Partido B', 'number':2,'votes': 80000,'postproc':0},
            {'option':'Partido C', 'number':3,'votes': 30000,'postproc':0},
            {'option':'Partido D', 'number':4,'votes': 12000,'postproc':0}
          
          ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    #Prueba 9 sin opciones
    def testHuntington9(self):
        data = {
            'type': 'HUNTINGTONHILL',
            'options': [
              
            ],
            'numEscanos': 200
        }

        expected_result = [
           
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)  

    #Prueba 10 sin opciones y num escanos
    def testHuntington10(self):
        data = {
            'type': 'HUNTINGTONHILL',
            'options': [
              
            ],
            #'numEscanos': 200
        }

        expected_result = [
           
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)       

    def testDHont1(self): #Número de votos para facilitar la comprobación manual.
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
            {'option':'OPT1','number':1,'votes': 12000, 'postproc': 0},
            {'option':'OPT2','number':2,'votes': 140000, 'postproc': 2},
            {'option':'OPT3','number':3,'votes': 110000, 'postproc': 2},
            {'option':'OPT4','number':4,'votes': 205000, 'postproc': 4},
            {'option':'OPT5','number':5,'votes': 150000, 'postproc': 2},
            {'option':'OPT6','number':6,'votes': 16000, 'postproc': 0}
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result) 
           
    def testDHont2(self): #Número de votos muy repartido.
        data = {
            'type': 'DHONT',
            'options': [
                {'option':'OPT1','number':1,'votes': 646556},
                {'option':'OPT2','number':2,'votes': 452154},
                {'option':'OPT3','number':3,'votes': 481216},
                {'option':'OPT4','number':4,'votes': 848654},
                {'option':'OPT5','number':5,'votes': 879564},
                {'option':'OPT6','number':6,'votes': 648321},
                {'option':'OPT7','number':7,'votes': 143210},
                {'option':'OPT8','number':8,'votes': 896483},
                {'option':'OPT9','number':9,'votes': 874684},
                {'option':'OPT10','number':10,'votes': 648545}
            ],
            'numEscanos': 32
        }

        expected_result = [
            {'option':'OPT1','number':1,'votes': 646556,'postproc': 3},
            {'option':'OPT2','number':2,'votes': 452154,'postproc': 2},
            {'option':'OPT3','number':3,'votes': 481216,'postproc': 2},
            {'option':'OPT4','number':4,'votes': 848654,'postproc': 4},
            {'option':'OPT5','number':5,'votes': 879564,'postproc': 5},
            {'option':'OPT6','number':6,'votes': 648321,'postproc': 3},
            {'option':'OPT7','number':7,'votes': 143210,'postproc': 0},
            {'option':'OPT8','number':8,'votes': 896483,'postproc': 5},
            {'option':'OPT9','number':9,'votes': 874684,'postproc': 5},
            {'option':'OPT10','number':10,'votes': 648545,'postproc': 3}
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def testDHont3(self): #No se le indica el número de escaños a repartir.
        data = {
            'type': 'DHONT',
            'options': [
                {'option':'OPT1','number':1,'votes': 32142},
                {'option':'OPT2','number':2,'votes': 64315},
                {'option':'OPT3','number':3,'votes': 97845},
                {'option':'OPT4','number':4,'votes': 31645},
                {'option':'OPT5','number':5,'votes': 97645}
            ]#,
            #'numEscanos': 50
        }

        expected_result = [
            {'option':'OPT1','number':1,'votes': 32142,'postproc': 0},
            {'option':'OPT2','number':2,'votes': 64315,'postproc': 0},
            {'option':'OPT3','number':3,'votes': 97845,'postproc': 0},
            {'option':'OPT4','number':4,'votes': 31645,'postproc': 0},
            {'option':'OPT5','number':5,'votes': 97645,'postproc': 0}
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def testDHont4(self): #Número de votos iguales.
        data = {
            'type': 'DHONT',
            'options': [
                {'option':'OPT1','number':1,'votes': 34124611},
                {'option':'OPT2','number':2,'votes': 34124611}
            ],
            'numEscanos': 20
        }

        expected_result = [
            {'option':'OPT1','number':1,'votes': 34124611,'postproc': 10},
            {'option':'OPT2','number':2,'votes': 34124611,'postproc': 10}
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)  
           
    def testDHont5(self): #Número de votos muy desigual.
        data = {
            'type': 'DHONT',
            'options': [
                {'option':'OPT1','number':1,'votes': 65155},
                {'option':'OPT2','number':2,'votes': 89498},
                {'option':'OPT3','number':3,'votes': 8645151},
                {'option':'OPT4','number':4,'votes': 65311},
                {'option':'OPT5','number':5,'votes': 8784565},
                {'option':'OPT6','number':6,'votes': 32151},
                {'option':'OPT7','number':7,'votes': 987515}
            ],
            'numEscanos': 100
        }

        expected_result = [
            {'option':'OPT1','number':1,'votes': 65155,'postproc': 0},
            {'option':'OPT2','number':2,'votes': 89498,'postproc': 0},
            {'option':'OPT3','number':3,'votes': 8645151,'postproc': 47},
            {'option':'OPT4','number':4,'votes': 65311,'postproc': 0},
            {'option':'OPT5','number':5,'votes': 8784565,'postproc': 48},
            {'option':'OPT6','number':6,'votes': 32151,'postproc': 0},
            {'option':'OPT7','number':7,'votes': 987515,'postproc': 5}

        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)   
  
    def testDHont6(self): #Número de votos muy grandes.
        data = {
            'type': 'DHONT',
            'options': [
                {'option':'OPT1','number':1,'votes': 846245435646644},
                {'option':'OPT2','number':2,'votes': 931654454532151},
                {'option':'OPT3','number':3,'votes': 821564325158125}
            ],
            'numEscanos': 200
        }

        expected_result = [
            {'option':'OPT1','number':1,'votes': 846245435646644,'postproc': 65},
            {'option':'OPT2','number':2,'votes': 931654454532151,'postproc': 72},
            {'option':'OPT3','number':3,'votes': 821564325158125,'postproc': 63}
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)
    
    def testDHont7(self): #Número de escaños muy grandes.
        data = {
            'type': 'DHONT',
            'options': [
                {'option':'OPT1','number':1,'votes': 3512315312},
                {'option':'OPT2','number':2,'votes': 8746512151},
                {'option':'OPT3','number':3,'votes': 8645313512}
            ],
            'numEscanos': 10000
        }

        expected_result = [
            {'option':'OPT1','number':1,'votes': 3512315312,'postproc': 1680},
            {'option':'OPT2','number':2,'votes': 8746512151,'postproc': 4184},
            {'option':'OPT3','number':3,'votes': 8645313512,'postproc': 4136}
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_danish2(self):
        data = {
            "type": "DANISH",
            "options": [
                { "option": "Option 1", "number": 1, "votes": 25244},
                { "option": "Option 2", "number": 2, "votes": 45784},
                { "option": "Option 3", "number": 3, "votes": 101366}
            ], 
            'numEscanos': 4

        }

        expected_result = [
            { "option": "Option 1", "number": 1, "votes": 25244, "postproc": 1 },
            { "option": "Option 2", "number": 2, "votes": 45784, "postproc": 1 },
            { "option": "Option 3", "number": 3, "votes": 101366, "postproc": 2 },
        ]

        response = self.client.post("/postproc/", data, format="json")
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_danish3(self):
        data = {
            "type": "DANISH",
            "options": [
                { "option": "Option 1", "number": 1, "votes": 72000},
                { "option": "Option 2", "number": 2, "votes": 60000},
                { "option": "Option 3", "number": 3, "votes": 28000},
                { "option": "Option 4", "number": 4, "votes": 24000},
                { "option": "Option 5", "number": 5, "votes": 16000}
            ], 
            'numEscanos': 5

        }

        expected_result = [
                { "option": "Option 1", "number": 1, "votes": 72000, "postproc": 2 },
                { "option": "Option 2", "number": 2, "votes": 60000, "postproc": 1 },
                { "option": "Option 3", "number": 3, "votes": 28000, "postproc": 1 },
                { "option": "Option 4", "number": 4, "votes": 24000, "postproc": 1 },
                { "option": "Option 5", "number": 5, "votes": 16000, "postproc": 0 }
        ]

        response = self.client.post("/postproc/", data, format="json")
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
            { 'option': 'A', 'number': 1, 'votes': 391000, 'postproc': 0},
            { 'option': 'B', 'number': 2, 'votes': 311000, 'postproc': 0},
            { 'option': 'C', 'number': 3, 'votes': 184000, 'postproc': 0},
            { 'option': 'D', 'number': 4, 'votes': 73000, 'postproc': 0},
            { 'option': 'E', 'number': 5, 'votes': 27000, 'postproc': 0},
            { 'option': 'F', 'number': 6, 'votes': 12000, 'postproc': 0},
            { 'option': 'G', 'number': 7, 'votes': 2000, 'postproc': 0},
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
            { 'option': 'A', 'number': 1, 'votes': 391000, 'postproc': 0},
            { 'option': 'B', 'number': 2, 'votes': 311000, 'postproc': 0},
            { 'option': 'C', 'number': 3, 'votes': 184000, 'postproc': 0},
            { 'option': 'D', 'number': 4, 'votes': 73000, 'postproc': 0},
            { 'option': 'E', 'number': 5, 'votes': 27000, 'postproc': 0},
            { 'option': 'F', 'number': 6, 'votes': 12000, 'postproc': 0},
            { 'option': 'G', 'number': 7, 'votes': 2000, 'postproc': 0},
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_danish4(self):
        data = {
            "type": "DANISH",
            "options": [
                { "option": "Option 1", "number": 1, "votes": 296729},
                { "option": "Option 2", "number": 2, "votes": 46573},
                { "option": "Option 3", "number": 3, "votes": 44227},
                { "option": "Option 4", "number": 4, "votes": 25410}
            ], 
            'numEscanos': 8

        }

        expected_result = [
                { "option": "Option 1", "number": 1, "votes": 296729, "postproc": 5 },
                { "option": "Option 2", "number": 2, "votes": 46573, "postproc": 1 },
                { "option": "Option 3", "number": 3, "votes": 44227, "postproc": 1 },
                { "option": "Option 4", "number": 4, "votes": 25410, "postproc": 1 }
        ]

        response = self.client.post("/postproc/", data, format="json")
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
            { 'option': 'A', 'number': 1, 'votes': 0, 'postproc': 0},
            { 'option': 'B', 'number': 2, 'votes': 0, 'postproc': 0},
            { 'option': 'C', 'number': 3, 'votes': 0, 'postproc': 0},
            { 'option': 'D', 'number': 4, 'votes': 0, 'postproc': 0},
            { 'option': 'E', 'number': 5, 'votes': 0, 'postproc': 0},
            { 'option': 'F', 'number': 6, 'votes': 0, 'postproc': 0},
            { 'option': 'G', 'number': 7, 'votes': 0, 'postproc': 0},
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)
    
    def test_danish5(self):
        data = {
            "type": "DANISH",
            "options": [
                { "option": "Option 1", "number": 1, "votes": 296729},
                { "option": "Option 2", "number": 2, "votes": 46573},
                { "option": "Option 3", "number": 3, "votes": 44227},
                { "option": "Option 4", "number": 4, "votes": 25410}
            ], 
            'numEscanos': 5

        }

        expected_result = [
                { "option": "Option 1", "number": 1, "votes": 296729, "postproc": 3 },
                { "option": "Option 2", "number": 2, "votes": 46573, "postproc": 1 },
                { "option": "Option 3", "number": 3, "votes": 44227, "postproc": 1 },
                { "option": "Option 4", "number": 4, "votes": 25410, "postproc": 0 }
        ]

        response = self.client.post("/postproc/", data, format="json")
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
            { 'option': 'A', 'number': 1, 'votes': 0, 'postproc': 0},
            { 'option': 'B', 'number': 2, 'votes': 0, 'postproc': 0},
            { 'option': 'C', 'number': 3, 'votes': 0, 'postproc': 0},
            { 'option': 'D', 'number': 4, 'votes': 0, 'postproc': 0},
            { 'option': 'E', 'number': 5, 'votes': 0, 'postproc': 0},
            { 'option': 'F', 'number': 6, 'votes': 0, 'postproc': 0},
            { 'option': 'G', 'number': 7, 'votes': 0, 'postproc': 0},
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
    
    def test_danish6(self):
        data = {
            "type": "DANISH",
            "options": [
                { "option": "Option 1", "number": 1, "votes": 72000},
                { "option": "Option 2", "number": 2, "votes": 60000},
                { "option": "Option 3", "number": 3, "votes": 28000},
                { "option": "Option 4", "number": 4, "votes": 24000},
                { "option": "Option 5", "number": 5, "votes": 16000}
            ], 
            'numEscanos': 4

        }

        expected_result = [
                { "option": "Option 1", "number": 1, "votes": 72000, "postproc": 1 },
                { "option": "Option 2", "number": 2, "votes": 60000, "postproc": 1 },
                { "option": "Option 3", "number": 3, "votes": 28000, "postproc": 1 },
                { "option": "Option 4", "number": 4, "votes": 24000, "postproc": 1 },
                { "option": "Option 5", "number": 5, "votes": 16000, "postproc": 0 }
        ]

        response = self.client.post("/postproc/", data, format="json")
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)
    
    def test_danish7(self):
        data = {
            "type": "DANISH",
            "options": [
                { "option": "Option 1", "number": 1, "votes": 72000},
                { "option": "Option 2", "number": 2, "votes": 60000},
                { "option": "Option 3", "number": 3, "votes": 0},
                { "option": "Option 4", "number": 4, "votes": 24000},
                { "option": "Option 5", "number": 5, "votes": 16000}
            ], 
            'numEscanos': 4

        }

        expected_result = [
                { "option": "Option 1", "number": 1, "votes": 72000, "postproc": 2 },
                { "option": "Option 2", "number": 2, "votes": 60000, "postproc": 1 },
                { "option": "Option 3", "number": 3, "votes": 0, "postproc": 0 },
                { "option": "Option 4", "number": 4, "votes": 24000, "postproc": 1 },
                { "option": "Option 5", "number": 5, "votes": 16000, "postproc": 0 }
        ]

        response = self.client.post("/postproc/", data, format="json")
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)


   #Prueba 7 Imperiali mismos votos
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
            { 'option': 'A', 'number': 1, 'votes': 1000, 'postproc': 10},
            { 'option': 'B', 'number': 2, 'votes': 1000, 'postproc': 10},

        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    #Prueba 8 Imperiali menos votos que ecanos y numEscanos divisible entre el numero de opciones
    def testImperialiMenosVotosQueEscanosDivisible(self):
        
        data = {
            'type': 'IMPERIALI',
            'options': [
                { 'option': 'A', 'number': 1, 'votes': 4 },
                { 'option': 'B', 'number': 2, 'votes': 1 },

            ],
            'numEscanos': 20,   
        }
        expected_result = [
            { 'option': 'A', 'number': 1, 'votes': 4, 'postproc': 10},
            { 'option': 'B', 'number': 2, 'votes': 1, 'postproc': 10},
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    #Prueba 9 Imperiali menos votos que ecanos y numEscanos NO divisible entre el numero de opciones
    def testImperialiMenosVotosQueEscanosNoDivisible(self):
        
        data = {
            'type': 'IMPERIALI',
            'options': [
                { 'option': 'A', 'number': 1, 'votes': 4 },
                { 'option': 'B', 'number': 2, 'votes': 1 },

            ],
            'numEscanos': 21,   
        }
        expected_result = [
            { 'option': 'A', 'number': 1, 'votes': 4, 'postproc': 11},
            { 'option': 'B', 'number': 2, 'votes': 1, 'postproc': 10},
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)


    #Prueba 10 Imperiali Mismos Votos que escanos
    def testImperialimismosVotosQueEscanos(self):
        
        data = {
            'type': 'IMPERIALI',
            'options': [
                { 'option': 'A', 'number': 1, 'votes': 1 },
                { 'option': 'B', 'number': 2, 'votes': 1 },

            ],
            'numEscanos': 2,   
        }

        expected_result = [
            { 'option': 'A', 'number': 1, 'votes': 1, 'postproc': 1},
            { 'option': 'B', 'number': 2, 'votes': 1, 'postproc': 1},
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_saintelague(self):
        data = {
            'type': 'SAINTELAGUE',
            'numEscanos': 7,
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 340000 },
                { 'option': 'Option 2', 'number': 2, 'votes': 280000 },
                { 'option': 'Option 3', 'number': 3, 'votes': 160000 },
                { 'option': 'Option 4', 'number': 4, 'votes': 60000 },
            ]
        }

        expected_result = [
            { 'option': 'Option 1', 'number': 1, 'votes': 340000, 'postproc': 3 },
            { 'option': 'Option 2', 'number': 2, 'votes': 280000, 'postproc': 2 },
            { 'option': 'Option 3', 'number': 3, 'votes': 160000, 'postproc': 1 },
            { 'option': 'Option 4', 'number': 4, 'votes': 60000, 'postproc': 1 }
        ]
        
        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)    

    def test_saintelague2(self):
        data = {
            'type': 'SAINTELAGUE',
            'numEscanos': 5,
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 20 },
                { 'option': 'Option 2', 'number': 2, 'votes': 60 },
                { 'option': 'Option 3', 'number': 3, 'votes': 10 },
            ]
        }

        expected_result = [
            { 'option': 'Option 2', 'number': 2, 'votes': 60, 'postproc': 3 },
            { 'option': 'Option 1', 'number': 1, 'votes': 20, 'postproc': 1 },
            { 'option': 'Option 3', 'number': 3, 'votes': 10, 'postproc': 1 }

        ]
        
        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_saintelague3(self):
        data = {
            'type': 'SAINTELAGUE',
            'numEscanos': 4,
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 1000 },
                { 'option': 'Option 2', 'number': 2, 'votes': 800 },
                { 'option': 'Option 3', 'number': 3, 'votes': 750 },
                { 'option': 'Option 4', 'number': 4, 'votes': 600 },
                { 'option': 'Option 5', 'number': 5, 'votes': 350 },
            ]
        }

        expected_result = [
            { 'option': 'Option 1', 'number': 1, 'votes': 1000, 'postproc': 1 },
            { 'option': 'Option 2', 'number': 2, 'votes': 800, 'postproc': 1 },
            { 'option': 'Option 3', 'number': 3, 'votes': 750, 'postproc': 1 },
            { 'option': 'Option 4', 'number': 4, 'votes': 600, 'postproc': 1 },
            { 'option': 'Option 5', 'number': 5, 'votes': 350, 'postproc': 0 }
        ]
        
        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_saintelague4(self):
        data = {
            'type': 'SAINTELAGUE',
            'numEscanos': 0,
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 1000 },
                { 'option': 'Option 2', 'number': 2, 'votes': 800 },
                { 'option': 'Option 3', 'number': 3, 'votes': 750 },
                { 'option': 'Option 4', 'number': 4, 'votes': 600 },
                { 'option': 'Option 5', 'number': 5, 'votes': 350 },
            ]
        }

        expected_result = [
            { 'option': 'Option 1', 'number': 1, 'votes': 1000, 'postproc': 0 },
            { 'option': 'Option 2', 'number': 2, 'votes': 800, 'postproc': 0 },
            { 'option': 'Option 3', 'number': 3, 'votes': 750, 'postproc': 0 },
            { 'option': 'Option 4', 'number': 4, 'votes': 600, 'postproc': 0 },
            { 'option': 'Option 5', 'number': 5, 'votes': 350, 'postproc': 0 }
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_saintelague5(self):
        data = {
            'type': 'SAINTELAGUE',
            'numEscanos': 4,
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 0 },
                { 'option': 'Option 2', 'number': 2, 'votes': 0 },
                { 'option': 'Option 3', 'number': 3, 'votes': 0 },
                { 'option': 'Option 4', 'number': 4, 'votes': 0 },
                { 'option': 'Option 5', 'number': 5, 'votes': 0 },
            ]
        }

        expected_result = [
            { 'option': 'Option 1', 'number': 1, 'votes': 0, 'postproc': 0 },
            { 'option': 'Option 2', 'number': 2, 'votes': 0, 'postproc': 0 },
            { 'option': 'Option 3', 'number': 3, 'votes': 0, 'postproc': 0 },
            { 'option': 'Option 4', 'number': 4, 'votes': 0, 'postproc': 0 },
            { 'option': 'Option 5', 'number': 5, 'votes': 0, 'postproc': 0 }
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_saintelague6(self):
        data = {
            'type': 'SAINTELAGUE',
            'numEscanos': -4,
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 1000 },
                { 'option': 'Option 2', 'number': 2, 'votes': 800 },
                { 'option': 'Option 3', 'number': 3, 'votes': 750 },
                { 'option': 'Option 4', 'number': 4, 'votes': 600 },
                { 'option': 'Option 5', 'number': 5, 'votes': 350 },
            ]
        }

        expected_result = [
            { 'option': 'Option 1', 'number': 1, 'votes': 1000, 'postproc': 0 },
            { 'option': 'Option 2', 'number': 2, 'votes': 800, 'postproc': 0 },
            { 'option': 'Option 3', 'number': 3, 'votes': 750, 'postproc': 0 },
            { 'option': 'Option 4', 'number': 4, 'votes': 600, 'postproc': 0 },
            { 'option': 'Option 5', 'number': 5, 'votes': 350, 'postproc': 0 }
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_saintelague7(self):
        data = {
            'type': 'SAINTELAGUE',
            'numEscanos': 8,
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 4 },
                { 'option': 'Option 2', 'number': 2, 'votes': 2 }
            ]
        }

        expected_result = [
            { 'option': 'Option 1', 'number': 1, 'votes': 4, 'postproc': 5 },
            { 'option': 'Option 2', 'number': 2, 'votes': 2, 'postproc': 3 }
        ]
        
        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def testHb(self):
        data = {
            'type': 'HB',
            'options': [
                {'option':'Partido A','number':1,'votes': 100000},
                {'option':'Partido B', 'number':2,'votes': 80000},
                {'option':'Partido C', 'number':3,'votes': 30000},
                {'option':'Partido D', 'number':4,'votes': 20000}
            ],
            'numEscanos': 8     #cociente = 25555,56
        }

        expected_result = [
            {'option':'Partido A','number':1,'votes': 100000,'postproc':4},
            {'option':'Partido B', 'number':2,'votes': 80000,'postproc':3},
            {'option':'Partido C', 'number':3,'votes': 30000,'postproc':1},
            {'option':'Partido D', 'number':4,'votes': 20000,'postproc':0}
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)




   
