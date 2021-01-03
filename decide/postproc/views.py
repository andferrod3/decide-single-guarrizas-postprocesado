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

    
    def paridad(self, options):

        BOOL_CHOICES = ((True, 'Male'), (False, 'Female'))
        genero = BOOL_CHOICES

        if len(options)==0:
            return []
        
        listamujer=[]
        listahombre=[]

        for opt in options:
            if opt['genero']:
                listamujer.append(opt)
            else:
                listahombre.append(opt)

        listamujer.sort(key=lambda x: -x['votes']);
        listahombre.sort(key=lambda x: -x['votes']);


        listaAux=[]

        i=0
        res =[]

        if len(listamujer) < len(listahombre):
            i = len(listamujer)
            listaAux = listahombre
        else:
            i = len(listahombre)
            listaAux = listamujer

        
        for j in range(i):
            if listamujer[j]['votes'] > listahombre[i]['votes']:
                res.append(listamujer[j])
                res.append(listahombre[j])
            else:
                res.append(listahombre[j])
                res.append(listamujer[j])

        for opt in listaAux:
            if opt not in res:
                res.append(opt)

        return res



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
        elif t == 'PARIDAD':
            return self.paridad(opts)

        return Response({})
