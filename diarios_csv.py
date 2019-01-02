from crawlers.diarios_base import *
from common.recursive_folders import recursive_folders
from common.parallel_programming import parallel_programming
import re, pandas as pd, subprocess

def create_csv(filepath):
	rows = []
	partes_nome = filepath.split('/')
	nome_arquivo = filepath.split('/')[-1]
	tribunal = ''
	for p in partes_nome:
		if re.search(r'Diarios_',p):
			tribunal = p.split('_')[1]
			break
	if tribunal in diarios:
		texto = ' '.join([i for i in open(filepath,'r')])
		publicacoes = encontra_publicacoes(tribunal, texto)
		for pub in publicacoes:
			pub = ''.join(pub)
			numero = encontra_numero(tribunal, pub)
			rows.append({'tribunal':tribunal,'texto_publicacao':pub.replace('\n',''),'nome_arquivo':filepath,'data':'','numero_processo':numero})
	index = [j for j in range(len(rows))]
	df = pd.DataFrame(rows, index=index)
	df.to_csv(nome_arquivo.replace('.txt','.csv'))
	subprocess.Popen('mv "%s.csv" %s' % (nome_arquivo[:-4],filepath.replace(nome_arquivo,'')), shell=True) 

def main(path_diarios):
	rec_f = recursive_folders()
	parallel = parallel_programming()
	arquivos_path = rec_f.find_files(path_diarios)
	diarios_processar = [i for i in arquivos_path if re.search(r'\.txt',i)]
	parallel.run_f_nbatches(create_csv,diarios_processar)

if __name__ == '__main__':
	path_diarios = '/media/danilo/66F5773E19426C79/Diarios'
	main(path_diarios)