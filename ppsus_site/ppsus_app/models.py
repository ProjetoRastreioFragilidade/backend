from django.db import models


class Posto(models.Model):
	nome = models.CharField(max_length=100)
	numero = models.IntegerField(blank=True)
	endereco = models.CharField(max_length=100, blank=True)
	bairro = models.CharField(max_length=100, blank=True)
	cep = models.CharField(max_length=8, blank=True)
	telefone = models.CharField(max_length=9, blank=True)

class Usuario(models.Model):
	fk_post = models.ForeignKey(Posto, on_delete=models.CASCADE, blank=True)
	nome = models.CharField(max_length=100)
	login = models.CharField(max_length=50)	
	senha = models.CharField(max_length=20)
	tipo = models.CharField(max_length=1)
	permissao = models.IntegerField()