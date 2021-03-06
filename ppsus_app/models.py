from django.db import models
from multiselectfield import MultiSelectField
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import AbstractUser

CHOICES_SIM_NAO_2 = (
    (1, 'Sim'),
    (2, 'Não'),
)
CHOICES_SIM_NAO_4 = (
    (1, 'Sim'),
    (2, 'Não'),
    (3, 'Não sabe'),
    (4, 'Não respondeu'),
)
CHOICES_FREQ = (
    (1, 'Nunca ou raramente'),
    (2, 'Às vezes'),
    (3, 'Frequentemente'),
    (4, 'Sempre'),
)
MULTIPLE_CHOICES = (
	('1', 'Preparar refeição (cozinhar)'),
	('2', 'Usar o telefone'),
	('3', 'Transporte (se locomover)'),
	('4', 'Lavar a roupa'),
	('5', 'Cuidar da casa (limpar / arrumar)'),
	('6', 'Cuidar do dinheiro'),
	('7', 'Fazer compras'),
	('8', 'Tomar remédios')
)


class Posto(models.Model):
	nome = models.CharField(max_length=100)
	end_bairro = models.CharField(max_length=100, null=True, blank=True)
	end_rua = models.CharField(max_length=100, null=True, blank=True)
	end_numero = models.IntegerField(null=True, blank=True)
	cep = models.CharField(max_length=8, null=True, blank=True)
	telefone = models.CharField(max_length=11, null=True, blank=True)

class User(AbstractUser):
	posto = models.ForeignKey(Posto, on_delete=models.CASCADE, related_name='user', null=True, blank=True)

class Paciente(models.Model):
	posto = models.ForeignKey(Posto, on_delete=models.CASCADE, related_name='paciente')

	nome = models.CharField(max_length=100)
	sexo = models.PositiveSmallIntegerField(choices=((0, "Masculino"), 
													 (1, "Feminino")), null=True, blank=True)
	nro_sus = models.CharField(max_length=15, unique=True)
	data_nascimento = models.DateField()
	end_bairro = models.CharField(max_length=100, null=True, blank=True)
	end_rua = models.CharField(max_length=100, null=True, blank=True)
	end_numero = models.CharField(max_length=100, null=True, blank=True)
	cep = models.CharField(max_length=8, null=True, blank=True)

class Subjetiva(models.Model):
	paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='subjetiva')
	usuario = models.ForeignKey('ppsus_app.User', on_delete=models.CASCADE, related_name='subjetiva')
	usuario_edit = models.ForeignKey('ppsus_app.User', on_delete=models.CASCADE, null=True, blank=True, related_name='subjetiva_edit')

	data_inicio = models.DateTimeField()
	data_fim = models.DateTimeField(auto_now=True)

	fragilidade = models.CharField(max_length=1, null=True, blank=True)
	score = models.PositiveSmallIntegerField(null=True)
	fatores = models.CharField(max_length=300, null=True, blank=True)
	
	q1_perdeu_peso = models.PositiveSmallIntegerField(choices=CHOICES_SIM_NAO_4)
	q1_perdeu_peso_kg = models.FloatField(null=True, blank=True)
	q2_ativ_fisica = models.PositiveSmallIntegerField(choices=CHOICES_SIM_NAO_4)
	q3_red_forca = models.PositiveSmallIntegerField(choices=CHOICES_SIM_NAO_4)
	q4_red_caminhada = models.PositiveSmallIntegerField(choices=CHOICES_SIM_NAO_4)
	q5_fadiga = models.PositiveSmallIntegerField(choices=CHOICES_FREQ)
	q6_desanimo = models.PositiveSmallIntegerField(choices=CHOICES_FREQ)

class Document(models.Model):
	image = models.ImageField(upload_to='%Y/%m/%d/')
	@property
	
	def image_url(self):
		return self.image.url


class Edmonton(models.Model):
	paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='edmonton')
	usuario = models.ForeignKey('ppsus_app.User', on_delete=models.CASCADE, related_name='edmonton')
	usuario_edit = models.ForeignKey('ppsus_app.User', on_delete=models.CASCADE, null=True, blank=True, related_name='edmonton_edit')
	q1_foto_relogio = models.CharField(max_length=200)

	data_inicio = models.DateTimeField()
	data_fim = models.DateTimeField(auto_now=True)

	fragilidade = models.CharField(max_length=1, null=True, blank=True)
	score = models.PositiveSmallIntegerField(null=True)
	fatores = models.CharField(max_length=300, null=True, blank=True)
	
	q1_cognicao = models.PositiveSmallIntegerField(
		choices=((1, 'Aprovado'),
				 (2, 'Reprovado com erros mínimos'),
				 (3, 'Reprovado com erros significantes'),)
	)
	q2_estado_saude_A = models.PositiveSmallIntegerField(
		choices=((1, '0'),
				 (2, '1 ou 2'),
				 (3, '3 ou +'),)
	)
	q2_estado_saude_B = models.PositiveSmallIntegerField(
		choices=((1, 'Excelente'),
				 (2, 'Muito boa'),
				 (3, 'Boa'),
				 (4, 'Razoável'),
				 (5, 'Ruim'),)
	)
	q3_ind_func = MultiSelectField(choices=MULTIPLE_CHOICES, null=True, blank=True)
	q4_sup_social = models.PositiveSmallIntegerField(
		choices=((1, 'Sempre'),
				 (2, 'As vezes'),
				 (3, 'Nunca'),)
	)
	q5_medicamento_A = models.PositiveSmallIntegerField(choices=CHOICES_SIM_NAO_2)
	q5_medicamento_B = models.PositiveSmallIntegerField(choices=CHOICES_SIM_NAO_2)
	q6_nutricao = models.PositiveSmallIntegerField(choices=CHOICES_SIM_NAO_2)
	q7_humor = models.PositiveSmallIntegerField(choices=CHOICES_SIM_NAO_2)
	q8_continencia = models.PositiveSmallIntegerField(choices=CHOICES_SIM_NAO_2)
	q9_desemp_func = models.PositiveSmallIntegerField(
		choices=((1, '0-10 segundos'),
				 (2, '11-20 segundos'),
				 (3, '21 segundos ou mais'),)
	)
	q9_desemp_func_tempo = models.FloatField()
		
# This receiver handles token creation immediately a new user is created.
@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)