from rest_framework import fields, serializers
from .models import *
from ppsus_app.models import MULTIPLE_CHOICES
from django.contrib.auth.hashers import make_password

class PostoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posto
        fields = '__all__'

class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = '__all__'

class SubjetivaSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Subjetiva
        fields = '__all__'
        read_only_fields = ('usuario', 'usuario_edit', 'fragilidade', 'fatores')

class EdmontonSerializer(serializers.ModelSerializer):
    q3_ind_func = fields.MultipleChoiceField(choices=MULTIPLE_CHOICES)

    class Meta:
        model = Edmonton
        fields = '__all__'
        read_only_fields = ('usuario', 'usuario_edit', 'fragilidade', 'fatores')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'posto', 'user_permissions')
        read_only_fields = ('id',)
        #write_only_fields = ('password',)

class AvaliacaoSerializer(serializers.Serializer):
	id = serializers.IntegerField(read_only=True)
	data_inicio = serializers.DateTimeField(read_only=True)
	data_fim = serializers.DateTimeField(read_only=True) 
	tipo = serializers.CharField(read_only=True)


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'
