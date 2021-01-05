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
            {'option':'Partido A','number':1,'votes': 100000,'escanos':4},
            {'option':'Partido B', 'number':2,'votes': 80000,'escanos':3},
            {'option':'Partido C', 'number':3,'votes': 30000,'escanos':1},
            {'option':'Partido D', 'number':4,'votes': 20000,'escanos':0}
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
            {'option':'Likud','number':1,'votes': 985408,'escanos':30},
            {'option':'Unión Sionista', 'number':2,'votes': 786313,'escanos':24},
            {'option':'Lista Conjunta', 'number':3,'votes': 446583,'escanos':13},
            {'option':'Yesh Atid', 'number':4,'votes': 371602,'escanos':11},
            {'option':'Kulanu', 'number':5,'votes': 315360,'escanos':9},
            {'option':'La casa Judía', 'number':6,'votes': 283910,'escanos':9},
            {'option':'Shas', 'number':7,'votes': 241613,'escanos':7},
            {'option':'Yesh Atid', 'number':8,'votes': 214906,'escanos':6},
            {'option':'Judaísmo Unido de la Torá', 'number':9,'votes': 210143,'escanos':6},
            {'option':'Meretz', 'number':10,'votes': 165529,'escanos':5}
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
            {'option':'Partido A','number':1,'votes': 100000,'escanos':0},
            {'option':'Partido B', 'number':2,'votes': 80000,'escanos':0},
            {'option':'Partido C', 'number':3,'votes': 30000,'escanos':0},
            {'option':'Partido D', 'number':4,'votes': 20000,'escanos':0}
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
            {'option':'Partido A','number':1,'votes': 0,'escanos':0},
            {'option':'Partido B', 'number':2,'votes': 0,'escanos':0},
            {'option':'Partido C', 'number':3,'votes': 0,'escanos':0},
            {'option':'Partido D', 'number':4,'votes': 0,'escanos':0}
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
            {'option':'Partido A','number':1,'votes': 0,'escanos':0},
            {'option':'Partido B', 'number':2,'votes': 0,'escanos':0},
            {'option':'Partido C', 'number':3,'votes': 0,'escanos':0},
            {'option':'Partido D', 'number':4,'votes': 0,'escanos':0}
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

        #Prueba 6 con votos en negativo
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
            {'option':'Partido A','number':1,'votes': -100000,'escanos':0},
            {'option':'Partido B', 'number':2,'votes': -80000,'escanos':0},
            {'option':'Partido C', 'number':3,'votes': -30000,'escanos':0},
            {'option':'Partido D', 'number':4,'votes': -12000,'escanos':0}
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
            {'option':'Partido A','number':1,'votes': 100000,'escanos':0},
            {'option':'Partido B', 'number':2,'votes': 80000,'escanos':0},
            {'option':'Partido C', 'number':3,'votes': 30000,'escanos':0},
            {'option':'Partido D', 'number':4,'votes': 12000,'escanos':0}
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
            {'option':'OPT1','number':1,'votes': 646556,'escanos': 3},
            {'option':'OPT2','number':2,'votes': 452154,'escanos': 2},
            {'option':'OPT3','number':3,'votes': 481216,'escanos': 2},
            {'option':'OPT4','number':4,'votes': 848654,'escanos': 4},
            {'option':'OPT5','number':5,'votes': 879564,'escanos': 5},
            {'option':'OPT6','number':6,'votes': 648321,'escanos': 3},
            {'option':'OPT7','number':7,'votes': 143210,'escanos': 0},
            {'option':'OPT8','number':8,'votes': 896483,'escanos': 5},
            {'option':'OPT9','number':9,'votes': 874684,'escanos': 5},
            {'option':'OPT10','number':10,'votes': 648545,'escanos': 3}
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
            {'option':'OPT1','number':1,'votes': 32142,'escanos': 0},
            {'option':'OPT2','number':2,'votes': 64315,'escanos': 0},
            {'option':'OPT3','number':3,'votes': 97845,'escanos': 0},
            {'option':'OPT4','number':4,'votes': 31645,'escanos': 0},
            {'option':'OPT5','number':5,'votes': 97645,'escanos': 0}
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
            {'option':'OPT1','number':1,'votes': 34124611,'escanos': 10},
            {'option':'OPT2','number':2,'votes': 34124611,'escanos': 10}
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
            {'option':'OPT1','number':1,'votes': 65155,'escanos': 0},
            {'option':'OPT2','number':2,'votes': 89498,'escanos': 0},
            {'option':'OPT3','number':3,'votes': 8645151,'escanos': 47},
            {'option':'OPT4','number':4,'votes': 65311,'escanos': 0},
            {'option':'OPT5','number':5,'votes': 8784565,'escanos': 48},
            {'option':'OPT6','number':6,'votes': 32151,'escanos': 0},
            {'option':'OPT7','number':7,'votes': 987515,'escanos': 5}
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
            {'option':'OPT1','number':1,'votes': 846245435646644,'escanos': 65},
            {'option':'OPT2','number':2,'votes': 931654454532151,'escanos': 72},
            {'option':'OPT3','number':3,'votes': 821564325158125,'escanos': 63}
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)