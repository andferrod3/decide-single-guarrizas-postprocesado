from django.db import models
from rest_framework.views import APIView
from rest_framework.response import Response


import math
import numpy as np


class PostProcView(APIView):

    def identity(self, options):
        out = []

        for opt in options:
            out.append({
                **opt,
                'postproc': opt['votes'],
            });

        out.sort(key=lambda x: -x['postproc'])
        return Response(out)


    def danish(self, options, escañosTotales):

        #Creamos una lista de tamaño igual al numero de escaños. 
        #Es la secuencia usada para cada opcion, dividir el numero de votos entre cada una de los valores de la lista
        #para asi sacar los cocientes. 
        #La secuencia comienza en 1 y continua sumandole 3 al anterior. pj: para 4 escaños = (1,3,7,10)
        serie=[]
        serie.append(1)
        for i in range(1, escañosTotales):
            serie.append(serie[i-1]+3)
        
        #le asignamos un campo para el recuento de escanyos a cada opcion inicializandola a 0
        for option in options:
            option['escanyos']=0

        #creamos una matriz de el num de opciones como filas, y el num de escanyos totales como columnas
        matriz=np.zeros((len(options), escañosTotales))
    
        #para cada una de las opciones dividimos el num de votos por cada uno de los valos de la lista serie
        #y lo añadimos a la matriz en la posición que le corresponde
        for i in range(0, len(options)):
            option = options[i]
            for j in range(0, escañosTotales):
                s = serie[j]
                cociente = option['votes']/s
                matriz[i][j]= cociente

        #Para cada posible escanyo a asignar, obtenemos la posicion del mayor valor de la matriz,
        # incrementando en 1 el numero de escaños de la opción a la que corresponde el maximo valor.
        #Modificamos el mayor valor por 0 para que deje de serlo
        for escanyo in range(0, escañosTotales):
            maximo = np.amax(matriz)
            posicion = np.where(matriz==maximo)
            opt=options[posicion[0][0]]
            opt['escanyos']+=1
            matriz[posicion[0][0]][posicion[1][0]] = 0
            
        
        return Response(options)
       

    def post(self, request):
        """
         * type: IDENTITY | EQUALITY | WEIGHT
         * options: [
            {
             option: str,
             number: int,
             votes: int,
             ...extraparams
            }
           ]
        """

        t = request.data.get('type', 'IDENTITY')
        opts = request.data.get('options', [])
        numEscanos = request.data.get('numEscanos', 0)
        
        if t == 'IDENTITY':
            return self.identity(opts)
        elif t== 'DANISH':
            return self.danish(opts, numEscanos)


        return Response({})
