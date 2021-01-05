from django.db import models
from rest_framework.views import APIView
from rest_framework.response import Response
import math


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

<<<<<<< HEAD
    def imperialiYResiduo(self, numEscanos, options):

        votosTotales = 0
        for x in options:
            votosTotales += x['votes']

        if votosTotales > 0 and numEscanos > 0:

            q = round(votosTotales / (numEscanos+2), 0)
            
            escanosAsignados = 0
            for x in options:
                escanosSuelo = math.trunc(x['votes']/q)
                x.update({'escanosImp' : escanosSuelo})
                escanosAsignados += x['escanosImp']               

            #Si quedan escaños libres
            while(escanosAsignados < numEscanos):
                for x in options:
                    x.update({ 
                        'escanosRes' : x['votes'] - (q * x['escanosImp'])})

                options.sort(key=lambda x : -x['escanosRes'])

                opcionMasVotosResiduo = options[0]
                opcionMasVotosResiduo.update({
                'escanosImp' : opcionMasVotosResiduo['escanosImp'] + 1})
                escanosAsignados += 1

                #Lo borramos para que no este como atributo
                for i in options:
                    i.pop('escanosRes')
            options.sort(key=lambda x : -x['escanosImp'])
            
            return Response(options)
        else:
            for x in options:
                x.update({'escanosImp' : 0})
            return Response(options)

    def HuntingtonHill(self,numEscanos,options):

        votosTotales = 0
        for x in options:
            votosTotales += x['votes']
        
        if votosTotales > 0 and numEscanos > 0:

            limite = votosTotales/numEscanos

            #Crear parametros para metodo rounding rule
            rounding = limite*0.001
            lower = limite-rounding
            upper = limite+rounding

            numEscanosAsig = 0

            while(numEscanosAsig != numEscanos):

                #si llegamos a aplicar rounding rule y no llegamos al numero igual de escanos, 
                #reseteamos de nuevo el numero de escanos asig y empezamos de nuevo
                numEscanosAsig = 0

                for x in options:

                    if(x['votes']<limite):
                        x['escanos']=0
                    else:
                        cuota = x['votes']/limite
                        
                        if(isinstance(cuota,int)):
                            x['escanos']=cuota
                        else:
                            #Calculamos las cotas superior e inferior de la cuota y despues la media geometrica
                            lQ = int(cuota)
                            mediaG = math.sqrt(lQ*(lQ+1))

                            if(cuota > mediaG):
                                x['escanos']=(lQ+1)
                            else:
                                x['escanos']=lQ
                
                    numEscanosAsig += x['escanos']

                #Huntington-Hill Rounding Rule
                #For a quota q, let L denote its lower quota, U its upper quota, and G the
                #geometric mean of L and U. If then round q down to L, otherwise
                #round q up to U.

                if(numEscanosAsig < numEscanos):
                    limite = lower
                    lower = limite-rounding
                    upper = limite+rounding

                else:
                    limite = upper
                    lower = limite-rounding
                    upper = limite+rounding
        else:
            for x in options:
                x.update({'escanos' : 0})
            return Response(options)
        
        return Response(options)
=======

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
       
>>>>>>> conmarred

    def dHont(self, options, numEscanos):

        #Añadimos un campo para el contador de escaños asignados a cada opción.
        for option in options:
            option['escanos'] = 0
        
        #Para cada escaño, vamos a recorrer todas las opciones, usando la fórmula de d'Hont: número de votos a esa opción / (número de escaños asignados a esa opción + 1)
        for escano in range(0, numEscanos):
             #Lista de tamaño igual al número de opciones. Representa el recuento al aplicar la fórmula de cada opción, ordenados en la misma forma.
            recuento = []
            for option in options:
                r = option['votes'] / (option['escanos']+1)
                recuento.append(r)
            
            #Obtenemos el índice del máximo valor en la lista de recuento de votos, es decir, el índice del ganador del escaño
            ganador = recuento.index(max(recuento))
            #Al estar ordenadas de la misma forma, en la posicion del ganador le sumamos 1 escaño
            options[ganador]['escanos'] += 1

        return Response(options)


    def post(self, request):
        """
         * type: IDENTITY | IMPERIALI | HUNTINGTONHILL | 
         * options: [
            {
             option: str,
             number: int,
             votes: int,
             escanos: int
            }
        
           ]
        """

        t = request.data.get('type', 'IDENTITY')
        opts = request.data.get('options', [])
        numEscanos = request.data.get('numEscanos', 0)
        
        if t == 'IDENTITY':
            return self.identity(opts)
<<<<<<< HEAD
        elif t == 'IMPERIALI':
            return self.imperialiYResiduo(numEscanos=numEscanos, options=opts)
        elif t == 'HUNTINGTONHILL':
<<<<<<< HEAD
            return self.HuntingtonHill(opts,numEscanos)
=======
        elif t== 'DANISH':
            return self.danish(opts, numEscanos)

>>>>>>> conmarred
=======
            return self.HuntingtonHill(options=opts, numEscanos=numEscanos)
        elif t == 'DHONT':
            return self.dHont(options=opts, numEscanos=numEscanos)
>>>>>>> 5563cb7c06fcf8e6c580d58b23d8f8a66dd9257e

        return Response({})
