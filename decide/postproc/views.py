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

    def sainteLague(self,options,seats,census):
        results = []
        voters = sum(opt['votes'] for opt in options)

        for seat in range(seats):
            opt = self.maximum(options)
            self.update_results(opt, results, 1)
            aux = next((o for o in results if o['option'] == opt['option']), None)
            opt['votes'] = aux['votes']//(2*aux['postproc'] +1)

        part = self.participation(census, voters)
        out = {'results': results, 'participation': part}
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

        elif t == 'SAINTELAGUE':
            return self.sainteLague(opts,seats,census)

        return Response({})
