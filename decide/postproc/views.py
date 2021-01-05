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
        elif t == 'IMPERIALI':
            return self.imperialiYResiduo(numEscanos, opts)
        elif t == 'HUNTINGTONHILL':
            return self.HuntingtonHill(numEscanos, opts)

        return Response({})
