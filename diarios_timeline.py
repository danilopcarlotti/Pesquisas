import pandas as pd, re, arrow

COLUNAS_EXEC_CIVIL = ['Acordo',
	'Arquivamento',
	'Certidão negativa - mandado',
	'Certidão positiva - mandado',
	'Deferimento pesquisa em órgãos',
	'Deferimento tutela',
	'Indeferimento pesquisa em órgãos',
	'Indeferimento tutela',
	'Satisfação da execução',
	'Sentença'
]

def tipo_texto_execucao_civil(texto):
    if re.search(r'[\s\.\,]defiro.{1,40}(tutela|cautelar|apreensão|bloqueio)|concedo.{1,20}liminar',texto):
        return 'Deferimento tutela'
    elif re.search(r'[\s\.\,]defiro.{1,40}pesquisa',texto):
        return 'Deferimento pesquisa em órgãos'
    elif re.search(r'indefiro.{1,40}(tutela|cautelar|apreensão|bloqueio)',texto):
        return 'Indeferimento tutela'
    elif re.search(r'indefiro.{1,40}pesquisa',texto):
        return 'Indeferimento pesquisa em órgãos'
    elif re.search(r'julgo.{1,30}procedente',texto):
        return 'Sentença'
    elif re.search(r'arquive',texto):
        return 'Arquivamento'
    elif re.search(r'homolog.{1,30}acordo|acordo.{1,30}homolog',texto):
        return 'Acordo'
    elif re.search(r'levantamento.{1,20}penhora|guia.{1,20}levantamento',texto):
        return 'Satisfação da execução'
    elif re.search(r'certidão|cumprimento.{1,20}mandado',texto):
        if re.search(r'negativ|deix.{1,20}cumprir',texto):
			return 'Certidão negativa - mandado'
        else:
			return 'Certidão positiva - mandado'
    else:
        return False

def processar_timeline(chunk, timeline_processos, colunas=COLUNAS_EXEC_CIVIL, tipo_f=tipo_texto_execucao_civil):
	for index, row in chunk.iterrows():
		tipo = tipo_f(row['texto_publicacao'].lower().replace('\n',' '))
		if tipo:
			if row['numero_processo'] not in timeline_processos:
				timeline_processos[row['numero_processo']] = {
					'Número do processo':row['numero_processo']
				}
				for c in colunas:
					timeline_processos[row['numero_processo']][c] = '0'
			timeline_processos[row['numero_processo']][tipo] = row['nome_arquivo']

def main(path_ini,path_final):
	df = pd.read_csv(path_ini,chunksize=1000)
	timeline_processos = {}
	for chunk in df:
	    processar_timeline(chunk, timeline_processos)
	rows = []
	for k,v in timeline_processos.items():
		rows.append(v)
	df_datas = pd.DataFrame(rows,index=[i for i in range(len(rows))])
	df_datas.to_csv(path_final,index=False)

if __name__ == '__main__':
	main('/media/danilo/66F5773E19426C79/extracao_execucao_credito.csv','/media/danilo/66F5773E19426C79/datas_alienacao_fid_sp.csv')