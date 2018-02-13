from rest_framework import fields, serializers
from .models import *
from django.contrib.auth.models import User
from ppsus_app.models import MULTIPLE_CHOICES

class PostoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posto
        fields = '__all__'

class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = '__all__'

class SubjetivaSerializer(serializers.ModelSerializer):
    usuario = serializers.ReadOnlyField(source='')
    usuario_edit = serializers.ReadOnlyField(source='')
    fragilidade = serializers.ReadOnlyField(source='')
    fatores = serializers.ReadOnlyField(source='')
    
    class Meta:
        model = Subjetiva
        fields = '__all__'

class EdmontonSerializer(serializers.ModelSerializer):
    usuario = serializers.ReadOnlyField(source='')
    usuario_edit = serializers.ReadOnlyField(source='')
    fragilidade = serializers.ReadOnlyField(source='')
    fatores = serializers.ReadOnlyField(source='')
    
    q3_ind_func = fields.MultipleChoiceField(choices=MULTIPLE_CHOICES)

    class Meta:
        model = Edmonton
        fields = '__all__'

#class UserSerializer(serializers.HyperlinkedModelSerializer):
#    class Meta:
#        model = User
#        fields = '__all__'
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    '''def create(self, validated_data):
        user = self.Meta.model(**validated_data)
        user.set_password(validated_data["password"])
        #user.save()
        return user'''
    

class AvaliacaoSerializer(serializers.Serializer):
	id = serializers.IntegerField(read_only=True)
	data_inicio = serializers.DateTimeField(read_only=True)
	data_fim = serializers.DateTimeField(read_only=True) 
	tipo = serializers.CharField(read_only=True)

    