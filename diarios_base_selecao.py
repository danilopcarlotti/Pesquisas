from common.recursive_folders import recursive_folders
from common.parallel_programming import parallel_programming
from crawlers.common.conexao_local import cursorConexao
from common_nlp.parserTextoJuridico import parserTextoJuridico
import re, pandas as pd, subprocess

def csv_base(filepath):
	cursor = cursorConexao()
	df = pd.read_csv(filepath,error_bad_lines=False)
	for index, row in df.iterrows():
		# if not re.search(r'penal',row['texto_publicacao'],re.I) and re.search(r'saúde|medicamento|médic',row['texto_publicacao'],re.I) and re.search(r'(concedo|autorizo|defiro).{1,30}(antecipa..o.{1,20}tutela|tutela.{1,20}emerg.ncia|tutela.{,20}antecipada|liminar)',row['texto_publicacao'].lower(),flags=re.DOTALL|re.I):
		if re.search(r'aliena.{1,15}fiduciária',row['texto_publicacao'].lower(),re.DOTALL):
			cursor.execute('INSERT INTO diarios.publicacoes_diarias (tribunal, texto_publicacao, nome_arquivo, data, numero_processo) VALUES ("%s","%s","%s","%s","%s")' % (row['tribunal'],row['texto_publicacao'].replace('\n',' ').replace('"','').replace('\\',''),row['nome_arquivo'],row['data'],row['numero_processo']))

def main(path_diarios, path_relatorio_final):
	print('comecei')
	rec_f = recursive_folders()
	parallel = parallel_programming()
	arquivos_path = rec_f.find_files(path_diarios)
	diarios_processar = [i for i in arquivos_path if i[-3:] == 'csv']
	parallel.run_f_nbatches(csv_base,diarios_processar)
	print('terminei de inserir dados na base')

	print('gerando o csv com publicacoes')
	rows = []
	cursor = cursorConexao()
	cursor.execute('SELECT tribunal, texto_publicacao, nome_arquivo, data, numero_processo from diarios.publicacoes_diarias')
	dados = cursor.fetchall()
	for tribunal, texto_publicacao, nome_arquivo, data, numero_processo in dados:
		rows.append({'tribunal':tribunal, 'texto_publicacao':texto_publicacao, 'nome_arquivo':nome_arquivo, 'data':data, 'numero_processo':numero_processo})
	data_frame = pd.DataFrame(rows, index=[i for i in range(len(rows))])
	data_frame.to_csv(path_relatorio_final)
	print('fim')

if __name__ == '__main__':
	path_diarios = '/media/danilo/66F5773E19426C79/Diarios/Diarios_sp'
	main(path_diarios, '/media/danilo/66F5773E19426C79/extracao_execucao_credito.csv')