from django.shortcuts import render
from rest_framework import viewsets
from ppsus_app.models import *
from django.db.models import Value
from ppsus_app.serializers import *
from django.db.models.fields import CharField

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework import permissions
from ppsus_app.permissions import IsOwnerOrReadOnly
from ppsus_app.src import functions


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

class PostoViewSet(viewsets.ModelViewSet):
    queryset = Posto.objects.all()
    serializer_class = PostoSerializer

class PacienteViewSet(viewsets.ModelViewSet):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer

class SubjetivaViewSet(viewsets.ModelViewSet):
    queryset = Subjetiva.objects.all()
    serializer_class = SubjetivaSerializer
    
    def perform_create(self, serializer):
        fragilidade, vet_answ = functions.getFragilidadeSubjetiva(self.request.data)
        score = sum(vet_answ)
        fatores = functions.getFatores('subjetiva', fragilidade, vet_answ)
        # questão 5 e 6 juntas podem pontuar no máximo 1
        if vet_answ[4] == 1 and vet_answ[5] == 1:
            score -= 1

        serializer.save(
            usuario=self.request.user, 
            fragilidade=fragilidade,
            score=score,
            fatores=fatores)

    def perform_update(self, serializer):
        fragilidade, vet_answ = functions.getFragilidadeSubjetiva(self.request.data)
        score = sum(vet_answ)
        fatores = functions.getFatores('subjetiva', fragilidade, vet_answ)
        # questão 5 e 6 juntas podem pontuar no máximo 1
        if vet_answ[4] == 1 and vet_answ[5] == 1:
            score -= 1

        serializer.save(
            usuario_edit=self.request.user, 
            fragilidade=fragilidade,
            score=score,
            fatores=fatores)

class EdmontonViewSet(viewsets.ModelViewSet):    
    queryset = Edmonton.objects.all()
    serializer_class = EdmontonSerializer

    def perform_create(self, serializer):
        fragilidade, vet_answ = functions.getFragilidadeEdmonton(self.request.data)
        score = sum(vet_answ)
        fatores = functions.getFatores('edmonton', fragilidade, vet_answ)
        
        serializer.save(
            usuario=self.request.user, 
            fragilidade=fragilidade,
            score=score,
            fatores=fatores)

    def perform_update(self, serializer):
        fragilidade, vet_answ = functions.getFragilidadeEdmonton(self.request.data)
        score = sum(vet_answ)
        fatores = functions.getFatores('edmonton', fragilidade, vet_answ)

        serializer.save(
            usuario_edit=self.request.user, 
            fragilidade=fragilidade,
            score=score,
            fatores=fatores)            

#class UserViewSet(viewsets.ReadOnlyModelViewSet):
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        instance = serializer.save(is_active=True, is_staff=True)
        instance.set_password(instance.password)
        instance.save()

    def perform_update(self, serializer):
        instance = serializer.save()
        instance.set_password(instance.password)
        instance.save()


class AvaliacaoView(APIView):
    queryset = Subjetiva.objects.all()

    def get(self, request, id_paciente, format=None):
        from itertools import chain

        # filtra
        subjetiva = Subjetiva.objects.filter(paciente=id_paciente)
        edmonton = Edmonton.objects.filter(paciente=id_paciente)

        # adiciona campo tipo da avaliação
        subjetiva = subjetiva.annotate(tipo=Value('s', output_field=CharField()))
        edmonton = edmonton.annotate(tipo=Value('e', output_field=CharField()))

        # une as avaliações
        avaliacoes = list(chain(subjetiva, edmonton))        
        serializer = AvaliacaoSerializer(avaliacoes, many=True) 
        return Response(serializer.data)

class GetPacienteView(APIView):
    queryset = Paciente.objects.all()

    def get_object(self, n_sus):
        try:
            return Paciente.objects.get(nro_sus=n_sus)
        except Paciente.DoesNotExist:
            raise Http404

    def get(self, request, n_sus, format=None):
        paciente = self.get_object(n_sus)
        serializer = PacienteSerializer(paciente)
        return Response(serializer.data)

# resgata a quantidade de idosos por fragilidade, sexo e faixa etária
class RelatorioView(APIView):
    queryset = Paciente.objects.all()

    def get(self, request):
        # listas auxiliares
        avals  = ['subjetiva', 'edmonton']
        f_edm  = ['N', 'V', 'L', 'M', 'S']
        f_sub  = ['N', 'P', 'F']
        sexos  = ['M', 'F']
        idades = ['00-69', '70-79', '80+']
        dicts  = [{f : 0 for f in f_sub}, {f : 0 for f in f_edm}]
        
        # construindo dicionário de retorno
        ret = {}
        ret['geral'] = {aval : dict(dic) for aval, dic in zip(avals, dicts)}
        ret['sexo'] = {aval : {sexo : dict(dicts[i]) for sexo in sexos} for i, aval in enumerate(avals)}
        ret['idade'] = {aval : {idade : dict(dicts[i]) for idade in idades} for i, aval in enumerate(avals)}

        ## GERAL
        query_geral_sub = "SELECT ppsus_app_paciente.id FROM ppsus_app_paciente INNER JOIN ppsus_app_subjetiva ON ppsus_app_paciente.id = ppsus_app_subjetiva.paciente_id WHERE ppsus_app_subjetiva.fragilidade = {} AND ppsus_app_subjetiva.data_inicio = (SELECT max(ppsus_app_subjetiva.data_inicio) FROM ppsus_app_subjetiva WHERE ppsus_app_subjetiva.paciente_id = ppsus_app_paciente.id)"
        query_geral_edm = "SELECT ppsus_app_paciente.id FROM ppsus_app_paciente INNER JOIN ppsus_app_edmonton ON ppsus_app_paciente.id = ppsus_app_edmonton.paciente_id WHERE ppsus_app_edmonton.fragilidade = {} AND ppsus_app_edmonton.data_inicio = (SELECT max(ppsus_app_edmonton.data_inicio) FROM ppsus_app_edmonton WHERE ppsus_app_edmonton.paciente_id = ppsus_app_paciente.id)"
        soma = 0
        for f in f_sub:
            qtd = len(list(Paciente.objects.raw(query_geral_sub.format("\'"+f+"\'"))))
            ret['geral']['subjetiva'][f] = qtd
            soma += qtd
        for f in f_sub:
            ret['geral']['subjetiva'][f] = ret['geral']['subjetiva'][f] * (100/soma)
        
        soma = 0
        for f in f_edm:
            qtd = len(list(Paciente.objects.raw(query_geral_edm.format("\'"+f+"\'"))))
            ret['geral']['edmonton'][f] = qtd
            soma += qtd
        for f in f_edm:
            ret['geral']['edmonton'][f] = ret['geral']['edmonton'][f] * (100/soma)
        

        ## POR SEXO
        query_sexo_sub = "SELECT ppsus_app_paciente.id FROM ppsus_app_paciente INNER JOIN ppsus_app_subjetiva ON ppsus_app_paciente.id = ppsus_app_subjetiva.paciente_id WHERE ppsus_app_subjetiva.fragilidade = {} AND ppsus_app_paciente.sexo = {} AND ppsus_app_subjetiva.data_inicio = (SELECT max(ppsus_app_subjetiva.data_inicio) FROM ppsus_app_subjetiva WHERE ppsus_app_subjetiva.paciente_id = ppsus_app_paciente.id)"
        query_sexo_edm = "SELECT ppsus_app_paciente.id FROM ppsus_app_paciente INNER JOIN ppsus_app_edmonton ON ppsus_app_paciente.id = ppsus_app_edmonton.paciente_id WHERE ppsus_app_edmonton.fragilidade = {} AND ppsus_app_paciente.sexo = {} AND ppsus_app_edmonton.data_inicio = (SELECT max(ppsus_app_edmonton.data_inicio) FROM ppsus_app_edmonton WHERE ppsus_app_edmonton.paciente_id = ppsus_app_paciente.id)"
            
        for s in sexos:
            s_ = {'M' : 0, 'F' : 1}[s]
            soma = 0
            for f in f_sub:
                qtd = len(list(Paciente.objects.raw(query_sexo_sub.format("\'"+f+"\'", s_))))
                ret['sexo']['subjetiva'][s][f] = qtd
                soma += qtd
            if soma > 0:
                for f in f_sub:
                    ret['sexo']['subjetiva'][s][f] = ret['sexo']['subjetiva'][s][f] * (100/soma)

            soma = 0
            for f in f_edm:
                qtd = len(list(Paciente.objects.raw(query_sexo_edm.format("\'"+f+"\'", s_))))
                ret['sexo']['edmonton'][s][f] = qtd
                soma += qtd
            if soma > 0:
                for f in f_edm:
                    ret['sexo']['edmonton'][s][f] = ret['sexo']['edmonton'][s][f] * (100/soma)

        ## POR IDADE
        query_idade_sub = "SELECT ppsus_app_paciente.id FROM ppsus_app_paciente INNER JOIN ppsus_app_subjetiva ON ppsus_app_paciente.id = ppsus_app_subjetiva.paciente_id WHERE ppsus_app_subjetiva.fragilidade = {} AND ppsus_app_paciente.data_nascimento BETWEEN {} AND {} AND ppsus_app_subjetiva.data_inicio = (SELECT max(ppsus_app_subjetiva.data_inicio) FROM ppsus_app_subjetiva WHERE ppsus_app_subjetiva.paciente_id = ppsus_app_paciente.id)"
        query_idade_edm = "SELECT ppsus_app_paciente.id FROM ppsus_app_paciente INNER JOIN ppsus_app_edmonton ON ppsus_app_paciente.id = ppsus_app_edmonton.paciente_id WHERE ppsus_app_edmonton.fragilidade = {} AND ppsus_app_paciente.data_nascimento BETWEEN {} AND {} AND ppsus_app_edmonton.data_inicio = (SELECT max(ppsus_app_edmonton.data_inicio) FROM ppsus_app_edmonton WHERE ppsus_app_edmonton.paciente_id = ppsus_app_paciente.id)"
        
        from datetime import datetime, timedelta
        from .src.utils import sub_years, sub_days
        
        for i in idades:
            di, df = {'00-69' : (sub_years(datetime.now().date(), 69), datetime.now().date()), 
                      '70-79' : (sub_years(datetime.now().date(), 79), sub_days(sub_years(datetime.now().date(), 69), 1)),
                      '80+'   : (sub_years(datetime.now().date(), 200), sub_days(sub_years(datetime.now().date(), 79), 1))}[i]
            
            print("##############")
            print("{} até {}".format("\'"+str(di)+"\'", "\'"+str(df)+"\'"))
            print("##############")
            
            soma = 0
            for f in f_sub:
                qtd = len(list(Paciente.objects.raw(query_idade_sub.format("\'"+f+"\'", "\'"+str(di)+"\'", "\'"+str(df)+"\'"))))
                ret['idade']['subjetiva'][i][f] = qtd
                soma += qtd
            if soma > 0:
                for f in f_sub:
                    ret['idade']['subjetiva'][i][f] = ret['idade']['subjetiva'][i][f] * (100/soma)

            soma = 0
            for f in f_edm:
                qtd = len(list(Paciente.objects.raw(query_idade_edm.format("\'"+f+"\'", "\'"+str(di)+"\'", "\'"+str(df)+"\'"))))
                ret['idade']['edmonton'][i][f] = qtd
                soma += qtd
            if soma > 0:
                for f in f_edm:
                    ret['idade']['edmonton'][i][f] = ret['idade']['edmonton'][i][f] * (100/soma)

        return Response(ret)