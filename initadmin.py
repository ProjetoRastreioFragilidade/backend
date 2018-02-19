import django
django.setup()

from ppsus_app.models import User, Posto

admins = {
	#Aracy I
	1: [['Aline', 'Cristina dos Santos', 'alinearacy1'],
		['Andreá', 'Daisy dos Santos', 'andreaaracy1'],
		['Andréia', 'Inácio de Oliveira', 'andreiaaracy1'],
		['Lucinete', 'Alves Gomes', 'lucinetearacy1'],
		['Priscila', 'Ribeiro Costa', 'priscilaaracy1']
	],
	#Aracy II
	2: [['Ana', 'Adelaide Pereira', 'anaaracy2'],
		['Eloana', 'Silva Teixeira', 'eloanaaracy2'],
		['Harlem', 'Rogério Furquim', 'harlemaracy2'],
		['Marileide', 'Cristina Pine', 'marileidearacy2'],
		['Marli', 'de Fátima Oliveira Luiz', 'marliaracy2'],
		['Solange', 'Volten Gobbo', 'solangearacy2']],
	#Petrilli
	3: [['Aparecida', 'Romualda da Cunha', 'aparecidapetrilli'],
		['Jaquesceli', 'Carneiro de Almeida Oliveira', 'jaquescelipetrilli'],
		['Josiane', 'Alves Pereira dos Santos', 'josianepetrilli'],
		['Karoline', 'do Nascimento Polacci Jordão', 'karolinepetrilli'],
		['Kelly', 'Oliveira Santos', 'kellypetrilli']],
	#UFSCar
	4: [['Andresa', 'Paixão', 'andresa1'],
		['Angélica', 'Sartório', 'angelica2'],
		['Claudete', 'de Oliveira', 'claudete3'],
		['Fernanda', 'Karoline Generoso', 'fernanda4'],
		['Gabriela', 'Mazzo', 'gabriela5'],
		['Gabriella', 'Cavallaro', 'gabriella6'],
		['Isabela', 'Machado', 'isabela7'],
		['Juliane', 'Dias', 'juliane8'],
		['Larissa', 'Cesário', 'larissa9'],
		['Leticia', 'Didone', 'leticia10'],
		['Luiz', 'Eduardo Santos', 'luizeduardo11'],
		['Marisa', 'Silvana Zazzetta', 'marisa12'],
		['Mirely', 'Oliveira Ghinelli', 'mirely13'],
		['Patrícia', 'Bet', 'patricia14'],
		['Rosângela', 'Custódio', 'rosangela15'],
		['Ruana', 'Danieli', 'ruanadanieli16'],
		['Tainá', 'dos Santos', 'tainasantos17'],
		['Thainá', 'C. Duarte de Mello', 'thaina18']]}

if Posto.objects.count() == 0:
	for np in ['Aracy I', 'Aracy II', 'Petrilli', 'UFSCar']:
		posto = Posto.objects.create(nome=np)
		print("Posto "+np+" criado com sucesso!")	
else:
	print('Já existem postos cadastrados nesse banco de dados')

if User.objects.count() == 0:
	admin = User.objects.create_superuser(username='admin', password='ppsus2018', email='')
	admin.is_active = True
	admin.is_admin = True
	admin.save()

	for posto in admins:
		for first_name, last_name, login in admins[posto]:
			admin = User.objects.create_superuser(
				username=login, 
				password=login,
				email='',
				first_name=first_name, 
				last_name=last_name, 
				posto_id=posto)
			admin.is_active = True
			admin.is_admin = True
			admin.save()

			print("User "+login+" criado com sucesso!")	
else:
	print('Já existem usuários cadastrados nesse banco de dados')