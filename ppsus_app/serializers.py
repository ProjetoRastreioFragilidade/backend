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

    #posto = serializers.PrimaryKeyRelatedField(many=True, queryset='profile')

    class Meta:
        model = User
        fields = '__all__'
'''
    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.password = validated_data.get('password', instance.password)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.is_staff = validated_data.get('is_staff', instance.is_staff)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.profile.posto = validated_data.get('profile.posto', instance.profile.posto)
        instance.save()
        return instance

    def create(self, validated_data):
        return User.objects.create(**validated_data)'''

class AvaliacaoSerializer(serializers.Serializer):
	id = serializers.IntegerField(read_only=True)
	data_inicio = serializers.DateTimeField(read_only=True)
	data_fim = serializers.DateTimeField(read_only=True) 
	tipo = serializers.CharField(read_only=True)

    