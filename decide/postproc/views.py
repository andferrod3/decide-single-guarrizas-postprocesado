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

    def multiPreguntas(self, questions):
        for question in questions:
            for opt in question:
                opt['postproc'] = opt['votes'];

            question.sort(key=lambda x: -x['postproc'])

        return Response(questions)

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
        #groups = request.data.get('groups', False)
        opts = request.data.get('options', [])

        if t == 'IDENTITY':
            return self.identity(opts)

        elif t == 'MULTIPREGUNTAS':
            questions = request.data.get('questions', [])
            return self.multiPreguntas(questions)

        return Response({})
