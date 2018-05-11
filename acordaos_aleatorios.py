from crawlers.common.conexao_local import cursorConexao
import csv, random, pandas

def main(tabela, lower, upper, n):
	dados_aleatorios = []
	random.seed()
	cursor = cursorConexao()
	ids_aleatorios = random.sample(range(lower, upper), n*2)
	contador = 0
	id_dado = 0
	while contador < n and id_dado < len(ids_aleatorios):
		cursor.execute('SELECT * FROM {} where id = {} and lower(texto_decisao) like "%saúde%";'.format(tabela,str(ids_aleatorios[id_dado])))
		id_dado += 1
		dado = cursor.fetchall()
		if dado:
			contador += 1
			dados_aleatorios.append(dado)
	return dados_aleatorios

if __name__ == '__main__':
	dados = main('jurisprudencia_2_inst.jurisprudencia_2_inst',1324911, 5000000, 30000)
	with open('extracao_cnj.csv', 'w', newline='') as csvfile:
		writer_e = csv.writer(csvfile, delimiter=';',quotechar='"', quoting=csv.QUOTE_MINIMAL)
		writer_e.writerow(['id','tribunal','numero','assunto','classe','data_decisao','orgao_julgador','julgador','texto_decisao','relatorio','fundamentacao','dispositivo','polo_ativo','polo_passivo','origem'])
		for d in dados:
			writer_e.writerow([i for i in d[0]])

	dataframe = pandas.read_csv('extracao_cnj.csv', sep=';')
	with open('extracao_cnj_ids_classes.csv', 'w', newline='') as csvfile:
		for index, row in dataframe.iterrows():
			writer_e = csv.writer(csvfile, delimiter=';',quotechar='"', quoting=csv.QUOTE_MINIMAL)
			writer_e.writerow([row['id'],0])