#-------------------------------------#
# Vetor da pontuação em cada resposta #
#-------------------------------------#
def getVetAnswer(aval, data):

    if aval == 'subjetiva':
        vet_answ = [0, 0, 0, 0, 0, 0]

        if int(data['q1_perdeu_peso']) == 1 and float(data['q1_perdeu_peso_kg']) >= 4.5:
            vet_answ[0] = 1
        if int(data['q2_ativ_fisica']) == 1:
            vet_answ[1] = 1
        if int(data['q3_red_forca']) == 1:
            vet_answ[2] = 1
        if int(data['q4_red_caminhada']) == 1:
            vet_answ[3] = 1
        if int(data['q5_fadiga']) in (4, 3):
            vet_answ[4] = 1
        if int(data['q6_desanimo']) in (4, 3):
            vet_answ[5] = 1
    else:
        vet_answ = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        vet_answ[0] = int(data['q1_cognicao']) - 1

        vet_answ[1] = int(data['q2_estado_saude_A']) - 1

        if int(data['q2_estado_saude_B']) >= 4:
            vet_answ[2] = int(data['q2_estado_saude_B']) - 3

        if 'q3_ind_func' in data:
            qtd = len(dict(data)['q3_ind_func'])
            if qtd >= 5:
                vet_answ[3] += 2
            elif qtd >= 2:
                vet_answ[3] += 1
                
        vet_answ[4] = int(data['q4_sup_social']) - 1

        if int(data['q5_medicamento_A']) == 1:
            vet_answ[5] += 1

        if int(data['q5_medicamento_B']) == 1:
            vet_answ[6] += 1

        if int(data['q6_nutricao']) == 1:
            vet_answ[7] += 1

        if int(data['q7_humor']) == 1:
            vet_answ[8] += 1

        if int(data['q8_continencia']) == 1:
            vet_answ[9] += 1

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


# Migra os dados da tabela excel para a base de dados
def migrate_data(engine, connection):

    import pandas as pd

    df_sh = pd.read_excel("ppsus_app/src/data/collected_data.xlsx", sheet_name=0)

    col_list = list(df_sh)

    #-----------#
    # variáveis #
    #-----------#

    df_feat = pd.DataFrame()

    df_feat['meem'] = df_sh['RESULTADO MEEM']

    cols = col_list[293 : 297]
    df_feat['ativ_fis'] = df_sh[cols].sum(axis=1)

    df_feat['temp_sent'] = df_sh['MINUTOS AF/TEMPO SENTADO']

    df_feat['gds'] = df_sh['GDS TOTAL']

    df_feat['fes'] = df_sh['FES TOTAL']

    df_feat['man'] = df_sh[' MAN_TOTAL']

    cols = col_list[200 : 203]
    df_feat['fraq_musc_media'] = df_sh[cols].mean(axis=1)

    df_feat['fraq_musc_max'] = df_sh['MAIOR FORÇA_PREENSÃO']

    df_feat['lawton'] = df_sh['LAWTON_TOTAL']

    df_feat['katz'] = df_sh['KATZ_TOTAL']

    df_feat['ativ_ava'] = df_sh['CONTAGEM AINDA FAZ']

    df_feat['tug'] = df_sh['TUG']

    df_feat['caminhada'] = df_sh['MENOR_VELOCIDADE_CAT']

    df_feat['mos'] = df_sh['MOS TOTAL']

    df_feat['circ_cint'] = df_sh['CIRCUNF.CINTURA']
    df_feat['circ_quad'] = df_sh['CINCUNF.QUADRIL']
    df_feat['circ_pant'] = df_sh['CINCUNF.PANTURILHA']

    df_feat['berg'] = df_sh['BERG TOTAL']

    df_feat['idade'] = df_sh['IDADE'] 

    df_feat['relogio'] = df_sh['ITEM 1 RELÓGIO']

    df_feat['quedas'] = df_sh[col_list[126]]

    # Exames de sangue [443 : 468] + Biomarcadores inflamatórios [468 : 475]
    cols = col_list[443 : 475]
    df_feat = pd.concat([df_feat, df_sh[cols]], axis=1)

    #---------------#
    # classificação #
    #---------------#

    def cat_class(cat):
        if (cat == 1):
            return('N')
        if (cat == 2):
            return('P')
        if (cat == 3):
            return('F')

    df_feat.insert(0, 'subjetiva', df_sh['SUBJETIVA_CAT'].apply(cat_class))
    df_feat.insert(1, 'fried',     df_sh['FRIED_CAT'].apply(cat_class))
    df_feat.insert(2, 'edmonton',  df_sh['EDMONTON_CAT2'].apply(cat_class))

    # remove as categóricas, para deixar todas agrupadas no fim
    df_coleta = df_feat.drop({'PROTEINA TOTAL_CAT','ALBUMINA_CAT','GLOBULINAS_CAT','HEMOGLOBINA_CAT ','HEMATÓCRITO_CAT '}, axis=1)

    # concatena com as categóricas
    df_coleta = pd.concat([df_coleta, df_sh[['INTERNAÇÃO_CAT', 'MEEM_CAT', 'DOENÇA RENAL_CAT', 'FUMO_CAT', 'GDS_CAT2', 'INDEPEN_CAT', 'ITEM 4 VELOCIDADE_CAT',        'ITEM 5 (IPAQ_CAT (GASTO CALÓRICO)', 'ITEM 5 e 6 FADIGA_CAT', 'IPAQ_TOTAL_CAT1 (TRABALHO/TRANSPORTE/DOMÉSTICA/LAZER)', 'IPAQ_CAT2 (TRANSPORTE/LAZER)', 'AAVD_CAT', 'KATZ_CAT 2', 'TUG_CAT', 'BERG_CAT2', 'PROTEINA TOTAL_CAT', 'ALBUMINA_CAT', 'GLOBULINAS_CAT', 'HEMOGLOBINA_CAT ', 'HEMATÓCRITO_CAT ']]], axis=1)

    # respostas da subjetiva
    df_coleta.insert(3, 'subjetiva_q1',    df_sh[col_list[222]])
    df_coleta.insert(4, 'subjetiva_q1_kg', df_sh[col_list[221]]) 
    df_coleta.insert(5, 'subjetiva_q2',    df_sh[col_list[224]]) 
    df_coleta.insert(6, 'subjetiva_q3',    df_sh[col_list[226]]) 
    df_coleta.insert(7, 'subjetiva_q4',    df_sh[col_list[228]]) 
    df_coleta.insert(8, 'subjetiva_q5',    df_sh[col_list[229]].apply(lambda x: 1 if x!=0 else 0)) 
    df_coleta.insert(9, 'subjetiva_q6',    df_sh[col_list[230]].apply(lambda x: 1 if x!=0 else 0))

    # respostas da fried
    df_coleta.insert(10, 'fried_q1', df_sh[col_list[195]])
    df_coleta.insert(11, 'fried_q2', df_sh[col_list[199]])
    df_coleta.insert(12, 'fried_q3', df_sh[col_list[208]])
    df_coleta.insert(13, 'fried_q4', df_sh[col_list[214]])
    df_coleta.insert(14, 'fried_q5', df_sh[col_list[216]])
    # respostas da edmonton
    df_coleta.insert(15, 'edmonton_q1',   df_sh[col_list[169]])
    df_coleta.insert(16, 'edmonton_q2_b', df_sh[col_list[171]])
    df_coleta.insert(17, 'edmonton_q2_a', df_sh[col_list[173]])
    df_coleta.insert(18, 'edmonton_q3',   df_sh[col_list[175]])
    df_coleta.insert(19, 'edmonton_q4',   df_sh[col_list[177]])
    df_coleta.insert(20, 'edmonton_q5_a', df_sh[col_list[179]])
    df_coleta.insert(21, 'edmonton_q5_b', df_sh[col_list[181]])
    df_coleta.insert(22, 'edmonton_q6',   df_sh[col_list[184]])
    df_coleta.insert(23, 'edmonton_q7',   df_sh[col_list[186]])
    df_coleta.insert(24, 'edmonton_q8',   df_sh[col_list[188]])
    df_coleta.insert(25, 'edmonton_q9',   df_sh[col_list[190]])

    df_coleta.rename(index=str, inplace=True, columns={
        'meem' : 'meem',                      
        'ativ_fis' : 'ativ_fis',                  
        'temp_sent' : 'temp_sent',                 
        'gds' : 'gds',                       
        'fes' : 'fes',                       
        'man' : 'man',                       
        'fraq_musc_media' : 'fraq_musc_media',           
        'fraq_musc_max' : 'fraq_musc_max',             
        'lawton' : 'lawton',                    
        'katz' : 'katz',                      
        'ativ_ava' : 'aavd',                      
        'tug' : 'tug',                       
        'caminhada' : 'caminhada',                 
        'mos' : 'mos',                       
        'circ_cint' : 'circ_cint',                 
        'circ_quad' : 'circ_quad',                 
        'circ_pant' : 'circ_pant',                 
        'berg' : 'berg',                      
        'idade' : 'idade',                     
        'relogio' : 'relogio',                   
        'quedas' : 'quedas',                    
        'GLICOSE mg/dL' : 'glicose',                   
        'HDL mg/dL' : 'hdl',                       
        'LDL mg/dL' : 'ldl',                       
        'VLDL mg/dL' : 'vldl',                      
        'URÉIA mg/dL' : 'ureia',                     
        'CREATININA mg/dL' : 'creatina',                  
        'DHEA mg/dL' : 'dhea',                      
        '25-HIDROXIVITAMINA D ng/mL' : 'hidroxivitamina_d',         
        'INSULINA µUI/mL' : 'insulina',                  
        'HGH ng/mL' : 'hgh',                       
        'TRIGLICÉRIDES mg/dL' : 'triglicerides',             
        'PROTEINA TOTAL g/dL' : 'proteina_total',            
        'ALBUMINA g/dL' : 'albumina',                  
        'GLOBULINAS g/dL' : 'globulinas',                
        'COLESTEROL TOTAL mg/dL' : 'colesterol_total',          
        'S-DHEA µg/dL' : 's_dhea',                    
        'SOMATOMEDINA C ng/dL' : 'somatomedina_c',            
        'HEMOGLOBINA g/dL' : 'hemoglobina',               
        'HEMATÓCRITO (%)' : 'hematocrito',               
        'HEMOGLOBINA GLICADA (%)' : 'hemoglobina_glicada',       
        'ADAM10 pg/mL' : 'adam10',                    
        'IL-10 pg/mL' : 'il_10',                     
        'IL-1α pg/mL' : 'il_1alpha',                 
        'IL-1β pg/mL' : 'il_1beta',                  
        'IL-6 pg/mL' : 'il_6',                      
        'TNFα pg/mL' : 'tnf_alpha',                 
        'TNFβ pg/mL' : 'tnf_beta',                  
        'INTERNAÇÃO_CAT' : 'internacao_cat',            
        'MEEM_CAT' : 'meem_cat',                  
        'DOENÇA RENAL_CAT' : 'doenca_renal_cat',          
        'FUMO_CAT' : 'fumo_cat',                  
        'GDS_CAT2' : 'gds_cat2',                   
        'INDEPEN_CAT' : 'indepen_cat',               
        'ITEM 4 VELOCIDADE_CAT' : 'velocidade_cat',            
        'ITEM 5 (IPAQ_CAT (GASTO CALÓRICO)' : 'ipaq_gasto_calorico_cat',   
        'ITEM 5 e 6 FADIGA_CAT' : 'fadiga_cat',     
        'IPAQ_TOTAL_CAT1 (TRABALHO/TRANSPORTE/DOMÉSTICA/LAZER)' : 'ipaq_total_cat',            
        'IPAQ_CAT2 (TRANSPORTE/LAZER)' : 'ipaq_transp_lazer_cat2',                
        'AAVD_CAT' : 'aavd_cat',                  
        'KATZ_CAT 2' : 'katz_cat2',                  
        'TUG_CAT' : 'tug_cat',                   
        'BERG_CAT2' : 'berg_cat2',                  
        'PROTEINA TOTAL_CAT' : 'proteina_total_cat',        
        'ALBUMINA_CAT' : 'albumina_cat',              
        'GLOBULINAS_CAT' : 'globulinas_cat',            
        'HEMOGLOBINA_CAT ' : 'hemoglobina_cat',           
        'HEMATÓCRITO_CAT ' :'hematocrito_cat'      
    })

    # converto a resposta da questão para pontuação obtida
    df_coleta['subjetiva_q5'] = df_coleta['subjetiva_q5'].apply(lambda x: 1 if x!=0 else 0)


    print("DataFrame criado.")


    # cria tabela e insere os dados
    df_coleta.to_sql('ppsus_app_coleta', engine, if_exists='replace', index=False)


    print("Tabela criada. Criando chave primaria.")

    # cria chave primária para coleta
    connection.execute('ALTER TABLE ppsus_app_coleta ADD COLUMN id INT AUTO_INCREMENT PRIMARY KEY FIRST;')

    print("Chave criada com sucesso")

    print("Bye =D")


# Retorna toda a tabela coleta em um pandas dataframe
def selectColeta():
    import pandas as pd
    from sqlalchemy import create_engine
    from django.conf import settings

    name = settings.DATABASES['default']['NAME']
    user = settings.DATABASES['default']['USER']
    password = settings.DATABASES['default']['PASSWORD']
    host = settings.DATABASES['default']['HOST']
    port = settings.DATABASES['default']['PORT']

    engine = create_engine('mysql+mysqldb://'+user+':'+password+'@'+host+':'+port+'/'+name)
    connection = engine.connect()

    # se a tabela não foi criada, então cria e insere os dados
    if not engine.dialect.has_table(engine, 'ppsus_app_coleta'):
        migrate_data(engine, connection)

    return pd.read_sql('SELECT * FROM ppsus_app_coleta', con=connection)


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