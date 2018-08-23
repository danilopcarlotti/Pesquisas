import re, pandas as pd
from crawlers.common.conexao_local import cursorConexao


class extracao_variaveis():
	"""docstring for extracao_variaveis"""
	def __init__(self):
		self.var_bool = {
			"Privado": r"suplementar|seguro-sa.de|ANS|plano de sa.de|cooperativa m.dica",
			"Público": r"Secretaria|Minist.rio|Prefeitura|Munic.pio|Estado",
			"Representação": r"defensor|Defensoria",
			"ANS": r"ANS|Agencia Nacional de Saude",
			"Pedido Administrativo": r"administrativa|administrativo",
			"Coletiva relatório": r"A..o Civil P.blica|Mandado de Segurança Coletivo|A..o Popular",
			"Coletiva fundamentação": r"coletivo|coletiva|difusos|estrutural",
			"Medicamento": r"medicamento",
			"Dietas": r"dieta|alimento|suplemento|enteral",
			"Insumo ou materiais": r"material|seringas|tiras|insumos|bomba",
			"Procedimentos": r"procedimento|procedimento cirurgico|cirurgia",
			"Exames": r"exame|ultrassom|resson.ncia|diagn.stico por imagem",
			"Internação": r"interna..o",
			"Vagas": r"vaga",
			"Leitos": r"leito",
			"Orteses, Proteses, Meios auxiliares de locomoção": r"ortese|protese|cadeira de rodas",
			"Transplante": r"transplante",
			"Imunização": r"vacina|imuniza..o",
			"Pericia médica judicial": r"per.cia|perito",
			"Anvisa": r"Anvisa",
			"Protocolos Clínicos": r"Protocolo|PCDT",
			"RENAME": r"RENAME",
			"RENUME": r"RENUME",
			"RENASE": r"RENASE",
			"Registro Nacional de Implantes": r"RNI|Registro Nacional de Implantes",
			"Medicamento importado": r"importado|importa..o",
			"Erro Médico": r"erro m.dico|neglig.ncia|imper.cia|imprud.ncia"
		}
		self.var_regex = {
			"Secretaria Estadual": r"Secretaria.{1,20}Est.{1,20}Sa.de|Secretaria.{1,20}Sa.de.{1,10}Estad|SES",
			"Secretaria Municipal": r"Secretaria.{1,20}Munic.{1,20}Sa.de|Secretaria.{1,20}Sa.de.{1,10}Munic|SMS"
			# "Sanções": r"multa", r"bloqueio", r"sequestro", r"prisão", r"responsabilização pessoal" #aguardo de exemplos
		}
	def variaveis_textos(self, dicionario, dados):
		rows = []
		index = []
		index_counter = 1
		for id_p, texto in dados:
			dicionario_df = {'id':id_p}
			for k,v in dicionario.items():
				dicionario_df[k] = 0
			for k,v in dicionario.items():
				if re.search(v, texto):
					print(texto)
					dicionario_df[k] = 1
			rows.append(dicionario_df)
			index.append(index_counter)
			index_counter += 1
		data_frame = pd.DataFrame(rows, index=index)
		return data_frame

def main():
	ext = extracao_variaveis()
	df_saude = pd.read_csv('relatorio_cnj.csv', sep=';')
	dados = []
	for column in df_saude:
		dados.append((df_saude['id'],df_saude['texto_decisao']))
		print(df_saude['id'])
		print(df_saude['texto_decisao'])
		break
	df = ext.variaveis_textos(ext.var_bool, dados)
	print(df)

if __name__ == '__main__':
	main()