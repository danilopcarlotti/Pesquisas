from diarios_base import *
import re, pandas as pd, subprocess

sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))
from Pesquisas.common.recursive_folders import recursive_folders
from Pesquisas.common.parallel_programming import parallel_programming

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
		texto = '\n'.join([i for i in open(filepath,'r')])
		publicacoes = encontra_publicacoes(tribunal, texto)
		for pub in publicacoes:
			if pub:
				pub = ''.join(pub)
				numero = encontra_numero(tribunal, pub).replace('\n','').replace(' ','')
				rows.append({'tribunal':tribunal,'texto_publicacao':pub.replace('\n',' '),'nome_arquivo':filepath,'data':'','numero_processo':numero})
		index = [j for j in range(len(rows))]
		df = pd.DataFrame(rows, index=index)
		df.to_csv(nome_arquivo.replace('.txt','.csv'),index=False)
		subprocess.Popen('mv "%s.csv" "%s"' % (nome_arquivo[:-4],filepath.replace(nome_arquivo,'')), shell=True)

def main(path_diarios):
	rec_f = recursive_folders()
	parallel = parallel_programming()
	arquivos_path = rec_f.find_files(path_diarios)
	diarios_processar = [i for i in arquivos_path if i[-4:] == '.txt']
	# parallel.run_f_nbatches(create_csv,diarios_processar)
	for diario in diarios_processar:
		create_csv(diario)

if __name__ == '__main__':
	path_diarios = sys.argv[1]
	main(path_diarios)