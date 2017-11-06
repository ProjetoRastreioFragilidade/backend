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

class Paciente(models.Model):
	nome = models.CharField(max_length=100)
	nro_sus = models.CharField(max_length=15)	
	data_nascimento = models.DateField()

class Subjetiva(models.Model):
	fk_paciente_sub = models.ForeignKey(Paciente, on_delete=models.CASCADE)
	fk_usuario_sub = models.ForeignKey(Usuario, on_delete=models.CASCADE)
	data_inicio = models.DateTimeField()	
	data_fim = models.DateTimeField()
	q1_perdeu_peso = models.IntegerField(blank=True)
	q1_perdeu_peso_kg = models.FloatField(blank=True)
	q2_ativ_fisica = models.IntegerField(blank=True)
	q3_red_forca = models.IntegerField(blank=True)
	q4_red_caminhada = models.IntegerField(blank=True)
	q4_tempo_caminhada = models.TimeField(blank=True)
	q5_fadiga = models.IntegerField(blank=True)
	q6_desanimo = models.IntegerField(blank=True)

class Edmonton(models.Model):
	fk_paciente_ed = models.ForeignKey(Paciente, on_delete=models.CASCADE)
	fk_usuario_ed = models.ForeignKey(Usuario, on_delete=models.CASCADE)
	fk_usuario_edit = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='usuario_edit_set', blank=True)
	data_inicio = models.DateTimeField()	
	data_fim = models.DateTimeField()
	q1_cognicao = models.IntegerField(blank=True)
	q1_cognicao_edit = models.IntegerField(blank=True)
	q1_foto_relogio = models.ImageField(upload_to='fotos_relogio/', blank=True)
	q2_estado_saude_A = models.IntegerField(blank=True)
	q2_estado_saude_B = models.IntegerField(blank=True)
	q3_ind_func = models.IntegerField(blank=True)
	q4_sup_social = models.IntegerField(blank=True)
	q5_medicamento_A = models.IntegerField(blank=True)
	q6_nutricao = models.IntegerField(blank=True)
	q7_humor = models.IntegerField(blank=True)
	q8_continencia = models.IntegerField(blank=True)
	q9_desemp_func = models.IntegerField(blank=True)