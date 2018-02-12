#-----------------#
# Vetor respostas #
#-----------------#
def getVetAnswer(aval, data):

    if aval == 'subjetiva':
        vet_answ = [0, 0, 0, 0, 0, 0]

        if data['q1_perdeu_peso'] == '1' and float(data['q1_perdeu_peso_kg']) >= 4.5:
            vet_answ[0] = 1
        if data['q2_ativ_fisica'] == '1':
            vet_answ[1] = 1
        if data['q3_red_forca'] == '1':
            vet_answ[2] = 1
        if data['q4_red_caminhada'] == '1':
            vet_answ[3] = 1
        if data['q5_fadiga'] in ('4', '3', '2'):
            vet_answ[4] = 1
        if data['q6_desanimo'] in ('4', '3', '2'):
            vet_answ[5] = 1
    else:
        vet_answ = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        # questão 1
        vet_answ[0] = int(data['q1_cognicao']) - 1

        # questão 2 A
        vet_answ[1] = int(data['q2_estado_saude_A']) - 1

        # questão 2 B
        if int(data['q2_estado_saude_B']) >= 4:
            vet_answ[2] = int(data['q2_estado_saude_B']) - 3

        # questão 3
        qtd = len(data['q3_ind_func'].split(','))
        if qtd > 3:
            vet_answ[3] += 2
        elif qtd > 0:
            vet_answ[3] += 1

        # questão 4
        if data['q4_sup_social'] == '3':
            vet_answ[4] += 2
        else:
            vet_answ[4] += 1

        # qustão 5 A
        if data['q5_medicamento_A'] == '1':
            vet_answ[5] += 1

        # qustão 5 B
        if data['q5_medicamento_B'] == '1':
            vet_answ[6] += 1

        # qustão 6
        if data['q6_nutricao'] == '1':
            vet_answ[7] += 1

        # qustão 7
        if data['q7_humor'] == '1':
            vet_answ[8] += 1

        # qustão 8
        if data['q8_continencia'] == '1':
            vet_answ[9] += 1

        # questão 9
        vet_answ[10] += int(data['q9_desemp_func']) - 1

    return vet_answ


#------------#
# Distância  #
#------------#
# Parâmetros:
# * aval:     <str>      Tipo de avaliação. Ex: 'subjetiva'
# * dist_max: <int>      Distância máxima para busca dos indices
# * vet_answ: <list int> Lista de inteiro que correponde a pontuação obtida em cada questão da avaliação
# Retorno:
# * Retorna a lista de indice de todos os exemplos com distância menor ou igual a dist_max
def getIdsByMaxDistance(aval, dist_max, vet_answ, df):
    
    cols_aval = {'subjetiva' : ['subjetiva_q'+str(i+1) for i in range(6)],
                 'edmonton'  : ['edmonton_q'+str(i+1) for i in range(9) if i not in {1, 4}] +
                               ['edmonton_q2_a', 'edmonton_q2_b', 'edmonton_q5_a', 'edmonton_q5_b']}
    cols = cols_aval[aval]
    
    # trocando nulos por 0
    not_nan = df[cols].fillna(0)
    
    ret = []
    for index, row in not_nan.iterrows():        
        dist = 0
        for a, b in zip(vet_answ, row):
            dist += abs(a - b)
        if dist <= dist_max:
            ret.append(index)
    return(ret)


#--------------#
# Fisher Score #
#--------------#
# Parâmetros:
# * df_prox: <pandas dataframe> Dataframe dos indíviduos próximos
# * df_dist: <pandas dataframe> Dataframe dos indíviduos distantes
# Retorno:
# * Retorna uma lista das 5 variáveis que obtiveram maior pontuação no Critério de Fisher
def getFisherRank(df_prox, df_dist):
    # calcula score
    score = (df_prox.mean() - df_dist.mean()).pow(2) / (df_prox.var() + df_dist.var())

    # ordena
    score.sort_values(ascending=False, inplace=True)
    
    # retorna as 5 primeiras variáveis
    return score[:5].index

#------------#
# Incidência #
#------------#
# Parâmetros:
# * df_prox: <pandas dataframe> Dataframe dos indíviduos próximos
# Retorno:
# * Retorna uma lista das 5 variáveis que obtiveram maior pontuação na Análise por Incidência
def getIncidenciaRank(df_prox, df_feat_cat):
    import pandas as pd

    incidencia = pd.Series()

    df_incidencia = df_feat_cat.loc[df_prox.index]

    incidencia['meem_cat']  = df_incidencia[df_incidencia['meem_cat']  == 1].shape[0]
    incidencia['gds_cat2']  = df_incidencia[df_incidencia['gds_cat2']  == 2].shape[0]
    incidencia['aavd_cat']  = df_incidencia[df_incidencia['aavd_cat']  == 2].shape[0]
    incidencia['katz_cat2'] = df_incidencia[df_incidencia['katz_cat2'] == 2].shape[0]
    incidencia['tug_cat']   = df_incidencia[df_incidencia['tug_cat']   == 2].shape[0]
    incidencia['berg_cat2'] = df_incidencia[df_incidencia['berg_cat2'] == 1].shape[0]

    # faz a proporção (normaliza)
    incidencia = incidencia/df_prox.shape[0]

    # ordena
    incidencia.sort_values(ascending=False, inplace=True)

    # retorna as 5 primeiras variáveis
    return incidencia[:5].index

#-------------#
# Borda Count #
#-------------#
# - Aplica o método da Contagem de Borda, ou seja, seleciona as variáveis de maior 
# - pontuação em duas listas
# Parâmetros:
# * df_prox: <pandas dataframe> Dataframe dos indíviduos próximos
# * df_dist: <pandas dataframe> Dataframe dos indíviduos distantes
# Retorno:
# * Retorna uma lista das 5 variáveis que obtiveram maior pontuação no Borda Count
def getFinalRank(df_prox, df_dist, df_feat_cat):
    rank = getFisherRank(df_prox, df_dist)
    fisher_rank = [[5-i, dict_exib[var]] for i, var in enumerate(rank)]

    rank = getIncidenciaRank(df_prox, df_feat_cat)
    incidencia_rank = [[5-i, dict_exib[var]] for i, var in enumerate(rank)]

    for score, var in fisher_rank:
        i = [i for i, v in enumerate(incidencia_rank) if v[1] == var]
        if not i:
            incidencia_rank.append([score, var])
        else:
            incidencia_rank[i[0]][0] += score

    incidencia_rank.sort(key=lambda tup: tup[0], reverse=True)

    return [i[1] for i in incidencia_rank][:5]

# Retorna toda a tabela coleta em um pandas dataframe
def selectColeta():
    import pandas as pd
    import mysql.connector

    conn = mysql.connector.connect(user='ppsus', password='rede243', host='localhost', database='ppsus')
    return pd.read_sql('SELECT * FROM ppsus_app_coleta', con=conn)


#***********#
# ATRIBUTOS #
#***********#

df_coleta = selectColeta()

dict_exib = {
    'meem'            : 'Desempenho Cognitivo',
    'meem_cat'        : 'Desempenho Cognitivo',
    'ativ_fis'        : 'Atividade Física',
    'temp_sent'       : 'Tempo Sentado',
    'gds'             : 'Sintomas Depressivos',
    'gds_cat2'        : 'Sintomas Depressivos',
    'fes'             : 'Medo de Cair',
    'man'             : 'Estado Nutricional',
    'fraq_musc_media' : 'Média da Força Manual',
    'fraq_musc_max'   : 'Força Manual Máxima',
    'lawton'          : 'Atividades Instrumentais de Vida Diária',
    'katz'            : 'Atividades Básicas de Vida Diária',
    'katz_cat2'       : 'Atividades Básicas de Vida Diária',
    'aavd'            : 'Atividades Avançadas de Vida Diária',
    'aavd_cat'        : 'Atividades Avançadas de Vida Diária',
    'tug'             : 'Mobilidade',
    'tug_cat'         : 'Mobilidade',
    'caminhada'       : 'Velocidade da Marcha',
    'mos'             : 'Suporte Social',
    'circ_cint'       : 'Circunferência da Cintura',
    'circ_quad'       : 'Circunferência do Quadril',
    'circ_pant'       : 'Circunferência da Panturrilha',
    'berg'            : 'Equilíbrio',
    'berg_cat2'       : 'Equilíbrio',
    'relogio'         : 'Desempenho Cognitivo',
    'quedas'          : 'Número de Quedas'}