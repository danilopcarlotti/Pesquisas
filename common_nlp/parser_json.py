import json, os

class parser_json():
	"""Classe para parseamento de json's"""
	def __init__(self):
		pass

	def parse_bec_basico(self, file_path, multiple=False):
		resultados = []
		if multiple:
			arquivos = []
			for f in os.listdir(file_path):
				arquivos.append(file_path+'/'+f)
		else:
			arquivos = [file_path]
		for a in arquivos:
			json_dct = json.load(open(a,'r'))[0]
			# # PREGÕES
			# if 'DESC_ATA_GERADAPR' in json_dct and json_dct['DESC_ATA_GERADAPR']:
			# 	numero_oc = json_dct['OC']
			# 	uf = json_dct['UF']
			# 	modalidade = json_dct['MODALIDADE']
			# 	ente_federativo = json_dct['DESC_ATA_GERADAPR']['OCCompleta']['EnteFederativo']
			# 	responsaveis = str(json_dct['DESC_ATA_GERADAPR']['OCCompleta']['Responsaveis'])
			# 	equipe_apoio = str(json_dct['DESC_ATA_GERADAPR']['OCCompleta']['EquipeApoio'])
			# 	data_ini = json_dct['DT_INICIO']
			# 	data_fim = json_dct['DT_FIM']
			# 	resultados.append((numero_oc, uf, modalidade, ente_federativo, responsaveis, equipe_apoio, data_ini, data_fim))
			if 'DESC_ATA_GERADACV_ENCERRAMENTO' in json_dct and json_dct['DESC_ATA_GERADACV_ENCERRAMENTO']:
				numero_oc = json_dct['OC']
				uf = json_dct['UF']
				modalidade = json_dct['MODALIDADE']
				ente_federativo = json_dct['UNIDADE_COMPRADORA'].replace('"','').replace('\\','').replace('\'','')
				try:
					responsaveis = str(json_dct['DESC_ATA_GERADACV_ENCERRAMENTO']['RESPONSAVEL']).replace('"','').replace('\\','').replace('\'','')
				except:
					responsaveis = str(json_dct['DESC_ATA_GERADACV_ENCERRAMENTO']['RESPONSAVEIS']).replace('"','').replace('\\','').replace('\'','')
				equipe_apoio = ''
				data_ini = json_dct['DT_INICIO']
				data_fim = json_dct['DT_FIM']
				resultados.append((numero_oc, uf, modalidade, ente_federativo, responsaveis, equipe_apoio, data_ini, data_fim))
		return resultados

def main():
	p = parser_json()
	p.parse_bec_basico('/home/danilo/Downloads/BEC_json')

if __name__ == '__main__':
	main()