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

        fatores = functions.getFatores('subjetiva', fragilidade, vet_answ)

        serializer.save(
            usuario=self.request.user, 
            fragilidade=fragilidade,
            fatores=fatores)

    def perform_update(self, serializer):
        fragilidade, vet_answ = functions.getFragilidadeSubjetiva(self.request.data)
        fatores = functions.getFatores('subjetiva', fragilidade, vet_answ)

        serializer.save(
            usuario_edit=self.request.user, 
            fragilidade=fragilidade,
            fatores=fatores)

class EdmontonViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    
    queryset = Edmonton.objects.all()
    serializer_class = EdmontonSerializer

    def perform_create(self, serializer):
        fragilidade, vet_answ = functions.getFragilidadeEdmonton(self.request.data)
        fatores = functions.getFatores('edmonton', fragilidade, vet_answ)

        serializer.save(
            usuario=self.request.user, 
            fragilidade=fragilidade,
            fatores=fatores)

    def perform_update(self, serializer):
        fragilidade, vet_answ = functions.getFragilidadeEdmonton(self.request.data)
        fatores = functions.getFatores('edmonton', fragilidade, vet_answ)

        serializer.save(
            usuario_edit=self.request.user, 
            fragilidade=fragilidade,
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
    def get_object(self, n_sus):
        try:
            return Paciente.objects.get(nro_sus=n_sus)
        except Paciente.DoesNotExist:
            raise Http404

    def get(self, request, n_sus, format=None):
        paciente = self.get_object(n_sus)
        serializer = PacienteSerializer(paciente)
        return Response(serializer.data)