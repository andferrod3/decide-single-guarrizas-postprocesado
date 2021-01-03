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
        elif t == 'IMPERIALI':
            return self.imperialiYResiduo(numEscanos, opts)

        return Response({})
