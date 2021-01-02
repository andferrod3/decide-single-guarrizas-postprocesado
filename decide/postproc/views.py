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

    def actualizar_resultados(self, opt, resultados, arg):
        if not any(d.get('option', None) == opt['option'] for d in resultados):
            resultados.append({
                **opt,
                'postproc': arg,
            })
        else:
            aux = next((o for o in resultados if o['option'] == opt['option']), None)
            aux['postproc'] = aux['postproc'] + arg

    def borda(self, options):
        resultados = []
        maximo = len(options)

        for opt in options:
            for i in range(maximo):
                valor = opt['votes'][i]*(maximo-i)
                self.actualizar_resultados(opt, resultados, valor)

        resultados.sort(key=lambda x: -x['postproc'])
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
