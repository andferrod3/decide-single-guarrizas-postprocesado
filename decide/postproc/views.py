from rest_framework.views import APIView
from rest_framework.response import Response
import math


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

    def sainteLague(self, listaEscaños, escañosTotales):

        numEscañosRepartidos  = 0
        
        #inicializamos la lista con el num de escaños y cociente por partido a 0
        for x in listaEscaños:
             x.update({ 
                        'cociente' : 0,
                        'escanyos' : 0 })


        #Hacer lo siguiente HASTA que el numero de escaños repartidos y el real sean el mismo
        while(numEscañosRepartidos != escañosTotales):

            #Calculamos en primer lugar los cocientes para cada partido en la iteracion
            for x in listaEscaños:

                    esc = int(x.get('escanyos'))
                    ci = x.get('votes')/(2*esc+1)
                    print(ci)
                    x.update({ 'cociente' : ci})

                
            mayor_cociente = 0 

            #Una vez hecho esto, sacamos el mayor cociente de todos en esta iteracion
            for x in listaEscaños:
               if(x.get('cociente') > mayor_cociente):
                   mayor_cociente = x.get('cociente')

            #Finalmente, vemos a que partido pertenece dicho cociente mayor y, en caso de ser el suyo,
            #se le otorga como ganador 1 escaño mas y ninguno al resto de partidos
            for x in listaEscaños:
               if(x.get('cociente') == mayor_cociente):
                   x.update({'escanyos':x.get('escanyos')+1})
                
               else:
                   x.update({'escanyos':x.get('escanyos')})
                
            numEscañosRepartidos =  numEscañosRepartidos + 1
        
        #Finalmente le damos el formato de la coleccion que recibe el test para hacer la comprobaciones pertinentes
        #y eliminamos el campo cociente
        for x in listaEscaños:
            x.pop('cociente')

        return listaEscaños

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

        if t == 'IDENTITY':
            return self.identity(opts)

        return Response({})

    def metodoSainteLague(self, data):
        t = data.get('type')
        lista = data.get('options')
        escañosTotales = data.get('numEscanyos')
        if(t == 'SAINTELAGUE'):
            return self.sainteLague(lista,escañosTotales)
        else:
            return {}
