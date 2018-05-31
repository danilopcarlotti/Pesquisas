# -*- coding: utf-8 -*-

from collections import Counter
from crawlers.common.conexao_local import cursorConexao
# from crawlers.common_nlp.topicModelling import topicModelling
from common_nlp.mNB_classification_text import mNB_classification_text
import pandas as pd, utils

class relatorio_justica():
	'''Classe para geração de relatórios sobre a justiça'''
	def __init__(self):
		self.colunas_2_inst = ['id','tribunal','numero','assunto','classe','data_decisao','orgao_julgador','julgador','texto_decisao','relatorio','fundamentacao','dispositivo','polo_ativo','polo_passivo','origem']
		self.instancia_1 = 'jurisprudencia_1_inst.jurisprudencia_1_inst'
		self.instancia_2 = 'jurisprudencia_2_inst.jurisprudencia_2_inst'
		self.estados = ['ac','al','ap','am','ba','ce','df','es','go','ma','mt','ms','mg','pa','pb','pr','pe','pi','rj','rn','rs','ro','rr','sc','sp','se','to']
		self.cursor = cursorConexao()

	def dados_2_dic(self, dados, colunas):
		dicionario_dados = {}
		for coluna in colunas:
			dicionario_dados[coluna] = []
		for dado in dados:
			contador = 0
			for coluna in colunas:
				dicionario_dados[coluna].append(dado[contador])
				contador += 1
		return dicionario_dados

	def dicionario_estatisticas(self,df):
		dicionario_dados = {}
		for estado in self.estados:
			dicionario_dados[estado] = {
			'Estado':estado,
			'Numero de processos identificados':0, 
			'Assunto':[],
			'Classe':[],
			'orgao julgador':[],
			'Local de origem do recurso':[],
			'polo Ativo':[],
			'polo Passivo':[]
			}
		for estado in self.estados:
			for index, row in df.iterrows():
				if row['tribunal'] == estado:
					dicionario_dados[estado]['Numero de processos identificados'] += 1
					dicionario_dados[estado]['Assunto'].append(row['assunto'])
					dicionario_dados[estado]['Classe'].append(row['classe'])
					dicionario_dados[estado]['orgao julgador'].append((row['orgao_julgador'],row['julgador']))
					dicionario_dados[estado]['Local de origem do recurso'].append(row['origem'])
					dicionario_dados[estado]['polo Ativo'].append(row['polo_ativo'])
					dicionario_dados[estado]['polo Passivo'].append(row['polo_passivo'])
		return dicionario_dados

	def estatistica_descritiva(self, dicionario_dados, mais_frequentes = 10):
		if dicionario_dados['Numero de processos identificados'] == 0:
			return {'Nao encontrado':True}
		resultado = {'Nao encontrado':False}
		resultado['Numero de processos identificados'] = dicionario_dados['Numero de processos identificados']
		resultado['Principais assuntos'] = Counter(dicionario_dados['Assunto']).most_common(mais_frequentes)
		resultado['Principais classes'] = Counter(dicionario_dados['Classe']).most_common(mais_frequentes)
		resultado['Principais orgaos julgadores'] = Counter(dicionario_dados['orgao julgador']).most_common(mais_frequentes)
		resultado['Principais locais de origem'] = Counter(dicionario_dados['Local de origem do recurso']).most_common(mais_frequentes)
		resultado['Principais polos ativos'] = Counter(dicionario_dados['polo Ativo']).most_common(mais_frequentes)
		resultado['Principais polos passivos'] = Counter(dicionario_dados['polo Passivo']).most_common(mais_frequentes)
		return resultado

	def query_padrao(self, parametros=None, query=None, instancia='jurisprudencia_2_inst.jurisprudencia_2_inst', condicoes=None):
		if query:
			self.cursor.execute(query)
		else:
			if not parametros:
				return False
			elif condicoes:
				self.cursor.execute('select %s from %s %s;' % (parametros, instancia, condicoes))
			else:
				self.cursor.execute('select %s from %s;' % (parametros, instancia))
		return self.cursor.fetchall()

	def resultados_2_df(self, dados, colunas, coluna_indice='id'):
		dicionario_dados = self.dados_2_dic(dados, colunas)
		return pd.DataFrame(dicionario_dados, index=[i for i in range(len(dicionario_dados[coluna_indice]))])

	def textos_estado(self, df):
		dicionario_textos = {}
		for estado in self.estados:
			dicionario_textos[estado] = []
		for estado in self.estados:
			for index, row in df.iterrows():
				if row['tribunal'] == estado:
					dicionario_textos[estado].append(row['texto_decisao'])
		return dicionario_textos


def main():
	rel = relatorio_justica()
	# termos_excluir_saude = ['Saúde animal','Inadimplemento por motivo de saúde','Ação de Interdição','Interditanda','Funasa','Atividades nocivas à saúde do trabalhador','Regime Celetista','Trabalhista','Execução fiscal','Crédito fazendário','Improbidade administrativa','Tráfico','Fazenda Pública','Tributo','Curatela','PREVIDENCIA PRIVADA','VARA DE FAMILIA','SUCESSOES','DIREITO PREVIDENCIARIO','GUARDA PROVISÓRIA','TESTAMENTO','AÇÃO PREVIDENCIÁRIA','PRISÃO DOMICILIAR','ALIMENTOS PROVISÓRIOS','adicional de insalubridade','PISO SALARIAL','Trabalhadores Sindicalizados da Área de Saúde','penal pública incondicionada','PENSÃO POR MORTE','licença para tratamento de saúde','concurso','REDUÇÃO DA JORNADA DE TRABALHO','Coordenador de Finanças do Sindicato dos Trabalhadores em Saúde no Estado do Pará - SINDSAÚDE','RECLAMAÇÃO TRABALHISTA']
	# query_rel_saude = 'select * from jurisprudencia_2_inst.jurisprudencia_2_inst where lower(texto_decisao) like "%saúde%" and '
	# for t in termos_excluir_saude:
	# 	query_rel_saude += 'texto_decisao not like "%{}%" and '.format(t)
	# query_rel_saude = query_rel_saude[:-4]

	# print('rodando o classificador em toda a base')
	# # CLASSE DO CLASSIFICADOR
	model = utils.load_model('modelo.pickle')

	cursor = cursorConexao()

	# for i in range(0,int(numero_textos),1000):
	# 	try:
	# 		cursor.execute('SELECT id, texto_decisao from jurisprudencia_2_inst.jurisprudencia_2_inst where lower(texto_decisao) like "%saúde%" limit {},1000;'.format(str(i)))
	# 		dados_aux = cursor.fetchall()
	# 		for id_p, texto in dados_aux:

	# 			# APLICAÇÃO DO CLASSIFICADOR A UM TEXTO
	# 			token_texto = [utils.tokenize(texto, stem=True)]
	# 			classificacao = model.predict(token_texto)
	# 			print(classificacao)			
				
	# 			cursor.execute('UPDATE jurisprudencia_2_inst.jurisprudencia_2_inst set classificacao_auto = "{}" where id = {};'.format(classificacao[0],id_p))
	# 	except Exception as e:
	# 		print(e)
	# 		break

	print('recolhendo os textos com saude para classificacao')
	cursor.execute('SELECT id, texto_decisao from jurisprudencia_2_inst.jurisprudencia_2_inst where lower(texto_decisao) like "%saude%" limit 1;')
	dados_aux = cursor.fetchall()
	print(len(dados_aux))

	# APLICAÇÃO DO CLASSIFICADOR A UM TEXTO
	for id_p, texto in dados_aux:
		token_texto = [utils.tokenize(texto, stem=True)]
		classificacao = model.predict(token_texto)
		cursor.execute('UPDATE jurisprudencia_2_inst.jurisprudencia_2_inst set classificacao_auto = "{}" where id = {};'.format(classificacao[0],id_p))

	print('exportando a classificacao para um csv')
	dados = rel.query_padrao(parametros='*',condicoes='where classificacao_auto = "1"')
	rel.resultados_2_df(dados, rel.colunas_2_inst).to_csv(path_or_buf='relatorio_cnj.csv', sep=';', quotechar='"')
	df = pd.read_csv('relatorio_cnj.csv', sep=';', quotechar='"')

	# ESTATÍSTICA DESCRITIVA PARA CADA ESTADO
	estatistica_d = {}
	for k,v in rel.dicionario_estatisticas(df).items():
		estatistica_d[k] = rel.estatistica_descritiva(v)

	# TOPIC MODELLING PARA CADA ESTADO
	# tp = topicModelling()
	# textos_e = rel.textos_estado(df)
	# topicos = {}
	# for k,v in textos_e.items():
	# 	topicos[k] = tp.lda_Model(v)

	# TEXTO DO RELATÓRIO
	relatorio_final = open('relatorio_cnj_06_2018.txt','w',encoding='utf-8')
	relatorio_final.write('Relatorio final\n\n\n')
	relatorio_final.write('Estatistica descritiva sobre os processos nos tribunais\n\n\n')
	for k,v in estatistica_d.items():
		relatorio_final.write('Estado: ')
		relatorio_final.write(k)
		relatorio_final.write('\n\n')
		if v['Nao encontrado']:
			relatorio_final.write('Nao foram encontrados dados para este Estado\n\n')
		else:
			for m,n in v.items():
				relatorio_final.write(m)
				relatorio_final.write(' : ')
				relatorio_final.write(str(n))
				relatorio_final.write('\n')
			# relatorio_final.write('\nPrincipais tópicos das ações relacionadas à saúde neste tribunal:\n\n')
			# relatorio_final.write(topicos[k])

if __name__ == '__main__':
	main()
