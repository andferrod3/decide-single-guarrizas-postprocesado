from django.db import models
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
        #Si no hay opciones, devuelve un array vacío
        if len(options) == 0:
            return []

        hombres = []
        mujeres = []
        for opt in options:
            # si la opcion es un hombre, añadelo a la lista hombres, si no, a mujer.
            if opt['genero']:
                hombres.append(opt)
            else:
                mujeres.append(opt)

        # lista Ordenada de hombres por numero de votos
        hombres.sort(key=lambda x: -x['votes'])
        # lista Ordenada de mujeres por numero de votos
        mujeres.sort(key=lambda x: -x['votes'])

        res = []

        # tendrá el valor de la longitud de la lista más corta (hombres o mujeres)
        r = 0
        # la lista con más candidatos de las dos
        listaSecundaria = []

        if len(hombres) < len(mujeres):
            r = len(hombres)
            listaSecundaria = mujeres
        else:
            r = len(mujeres)
            listaSecundaria = hombres

        # añade a la lista resultado todos los elementos de la que fuera la
        # lista más larga. De este modo, se ordenaran los elementos de las
        # listas aplicando paridad hasta que en una de las dos no haya más
        # elementos. Entonces, completamos la lista resultado con los
        # candidatos de la lista que aún no se ha terminado de recorrer.

        for i in range(r):
            if hombres[i]['votes'] > mujeres[i]['votes']:
                res.append(hombres[i])
                res.append(mujeres[i])
            else:
                res.append(mujeres[i])
                res.append(hombres[i])

        for opt in listaSecundaria:
            if opt not in res:
                res.append(opt)
                opt.pop('genero')

        return res

    def danish(self, listaEscaños, escañosTotales):

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
                    ci = x.get('votes')/(esc+(1/3))
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

    def danish1(self, options, seats):
        #Se añade un campo de escaños (seats) a cada una de las opciones
        for opt in options:
            opt['seats'] = 0

        #Para cada uno de los escaños se calcula a que opción le correspondería el escaño 
        #teniendo en cuenta los ya asignados
        for i in range(seats):
            max(options, 
                key = lambda x : x['votes'] / ( x['seats'] + (1.0 / 3.0)))['seats'] += 1

        #Se ordenan las opciones por el número de escaños
        options.sort(key=lambda x: -x['seats'])
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
        
        if t == 'IDENTITY':
            return self.identity(opts)
        elif t == 'PARIDAD':
            return self.paridad(opts)

        return Response({})

    def metodoDanish(self, data):
        t = data.get('type')
        lista = data.get('options')
        escañosTotales = data.get('numEscanyos')
        if(t == 'DANISH'):
            return self.danish1(lista,escañosTotales)
        else:
            return {}
