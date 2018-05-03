from ppsus_app.src import utils 

#------------#
# Distância  #
#------------#
# Parâmetros:
# * aval:     <str>      Tipo de avaliação. Ex: 'subjetiva'
# * classe:   <str>      Classificação do sujeito (frágil, pré-frágil, não frágil). Ex: 'F'
# * vet_answ: <list int> Lista de inteiro que correponde a pontuação obtida em cada questão da avaliação
# Retorno:
# * Retorna a lista de 
def getFatores(aval, classe, vet_answ):	

	df_answ = utils.df_coleta.loc[:,'subjetiva':'edmonton_q9']
	df_feat =  utils.df_coleta[['meem', 'ativ_fis', 'temp_sent', 'gds', 'fes', 'man', 'fraq_musc_media', 'fraq_musc_max', 'lawton', 'katz', 'aavd', 'tug', 'caminhada', 'mos', 'circ_cint', 'circ_quad', 'circ_pant', 'berg', 'relogio', 'quedas']]
	df_feat_cat = utils.df_coleta[['meem_cat', 'gds_cat2', 'katz_cat2', 'aavd_cat', 'tug_cat', 'berg_cat2']]

	if aval == 'subjetiva':
		dist_max = 2
	else:
		dist_max = 4

	# Definindo data set de indivíduos próximos #
	exemplos = utils.getIdsByMaxDistance(aval, dist_max, vet_answ, df_answ)
	        
	
	if len(exemplos) >= 0.1*df_answ.shape[0]:
	    df_prox = df_feat.loc[exemplos]
	else:
	    exemplos = df_answ[df_answ[aval] == classe].index
	    df_prox = df_feat.loc[exemplos]

	# definindo data set de indivíduos distantes #
	# usa o complementar, ou seja, todo mundo que não está no data set próximos
	exemplos_dist = [i for i in range(df_answ.shape[0]) if i not in df_prox.index]
	df_dist = df_feat.loc[exemplos_dist]

	return utils.getFinalRank(df_prox, df_dist, df_feat_cat)


def getFragilidadeSubjetiva(data):
	vet_answ = utils.getVetAnswer('subjetiva', data)
	score = sum(vet_answ)
	
	# questão 5 e 6 juntas podem pontuar no máximo 1
	if vet_answ[4] == 1 and vet_answ[5] == 1:
		score -= 1

	if score == 0:
		return 'N', vet_answ
	elif score < 3:
		return 'P', vet_answ
	else:
		return 'F', vet_answ

def getFragilidadeEdmonton(data):
	vet_answ = utils.getVetAnswer('edmonton', data)
	score = sum(vet_answ)
	
	# Não apresenta fragilidade
	if score <= 4:
		return 'N', vet_answ
	# Aparentemente vulnerável
	elif score <= 6:
		return 'V', vet_answ
	# Fragilidade leve
	elif score <= 8:
		return 'L', vet_answ
	# Fragilidade moderada
	elif score <= 10:
		return 'M', vet_answ
	# Fragilidade severa
	else:
		return 'S', vet_answ