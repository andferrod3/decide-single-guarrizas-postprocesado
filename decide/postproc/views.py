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

    def saintelague(self,options,escanos):
        results = []
        for opt in options:
            results.append({
                    **opt,
                    'postproc': 0,
                })
        for i in range(escanos):
            maximo = max(options, key=lambda opt: opt['votes'])
            ganador_escano = next((o for o in results if o['option'] == maximo['option']), None)
            ganador_escano['postproc'] = ganador_escano['postproc'] + 1
            ganador_escano = next((o for o in results if o['option'] == maximo['option']), None)
            maximo['votes'] = ganador_escano['votes']//(2*ganador_escano['postproc'] +1)
        
        results.sort(key=lambda x: -x['postproc'])
        out = {'results': results}
        print(results)
        return Response(out)

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
        escanos = request.data.get('escanos')

        if t == 'IDENTITY':
            return self.identity(opts)
        
        elif t == 'SAINTELAGUE':
            return self.saintelague(opts,escanos)

        return Response({})
