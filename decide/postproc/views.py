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
    
    def participation(self, census, voters):
        out = 0

        if census != 0:
            out = (voters/census)*100
            out = round(out,2)

        return out
    
    def maximum(self, options):
        return max(options, key=lambda opt: opt['votes'])

    def update_results(self, opt, results, arg):
        if not any(d.get('option', None) == opt['option'] for d in results):
            results.append({
                **opt,
                'postproc': arg,
            })
        else:
            aux = next((o for o in results if o['option'] == opt['option']), None)
            aux['postproc'] = aux['postproc'] + arg

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
