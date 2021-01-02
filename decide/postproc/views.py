from rest_framework.views import APIView
from rest_framework.response import Response


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

    def borda(self, options):
        resultados = []
        maximo = len(options)

        for opt in options:
            for i in range(maximo):
                valor = opt['votes'][i]*(maximo-i)
                self.actualizar_resultados(opt, resultados, valor)

        self.order(resultados)
        out = {'resultados': resultados}

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

        if t == 'IDENTITY':
            return self.identity(opts)

        elif t == 'BORDA':
            return self.borda(opts)

        return Response({})
