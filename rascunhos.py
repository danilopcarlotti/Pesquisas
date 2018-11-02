# from crawlers.common.conexao_local import cursorConexao
# from common_nlp.parser_json import parser_json
# import os

# cursor = cursorConexao()

# cursor.execute('select numero_oc from bec.dados_basicos;')
# numeros_existentes = [i[0].strip() for i in cursor.fetchall()]

# p = parser_json()
# for f in os.listdir('/home/danilo/Downloads/BEC_json'):
# 	n_oc = f.split('_')[-1][:-5]
# 	if n_oc not in numeros_existentes:
# 		try:
# 			resultados = p.parse_bec_basico('/home/danilo/Downloads/BEC_json/'+f)
# 			for numero_oc, uf, modalidade, ente_federativo, responsaveis, equipe_apoio, data_ini, data_fim in resultados:
# 				cursor.execute('INSERT INTO bec.dados_basicos (numero_oc, uf, modalidade, ente_federativo, responsaveis, equipe_apoio, data_ini, data_fim) values ("%s","%s","%s","%s","%s","%s","%s","%s")' % (numero_oc, uf, modalidade, ente_federativo, responsaveis.replace('\'','').replace('"','').replace('\\',''), equipe_apoio.replace('\'','').replace('"','').replace('\\',''), data_ini, data_fim))
# 		except Exception as e:
# 			print(e)
# 			print(f)

from common.recursive_folders import recursive_folders
import os, re, subprocess

path = '/media/danilo/66F5773E19426C79/Diarios'

r = recursive_folders()
files = r.find_files(path)

for file in files:
	try:
		subprocess.call(["java", "-jar", "pdfbox-app-2.0.12.jar", "ExtractText", "-debug",file, file[:-4]+'.txt'])
	except Exception as e:
		print(e)