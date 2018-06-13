import sys, re
from crawler_jurisprudencia_tj import crawler_jurisprudencia_tj
from common.conexao_local import cursorConexao
from common_nlp.parse_texto import busca
from bs4 import BeautifulSoup

class crawler_jurisprudencia_tjce():
	"""Crawler especializado em retornar textos da jurisprudência de segunda instância do Ceará"""
	def __init__(self):
		crawler_jurisprudencia_tj.__init__(self)
		self.link_inicial = 'http://www.tjce.jus.br/institucional/consulta-de-acordao/'
		self.pesquisa_livre = '//*[@id="iddados.buscaInteiroTeor"]'
		self.data_julgamento_inicialXP = '//*[@id="dtJulgamentoInicio"]/input'
		self.data_julgamento_finalXP = '//*[@id="dtJulgamentoFim"]/input'
		self.botao_pesquisar = '//*[@id="pbSubmit"]'
		self.botao_proximo_ini = '//*[@id="paginacaoSuperior-A"]/table/tbody/tr[1]/td[2]/div/a[5]'
		self.botao_proximo = '//*[@id="paginacaoSuperior-A"]/table/tbody/tr[1]/td[2]/div/a[6]'
		self.tabela_colunas = 'justica_estadual.jurisprudencia_ce (ementas)'

	def parser_acordaos(self, texto, cursor):
		decisoes = re.split(r'\n\d+\s*?\-',texto)
		for d in range(1,len(decisoes)):
			numero = busca(r'\d{7}\-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}', decisoes[d],ngroup=0)
			classe_assunto = busca(r'\n\s*?Classe/Assunto\s*?\:\n(.*?)\n',decisoes[d])
			try:
				classe = classe_assunto.split('/')[0]
				assunto = classe_assunto.split('/')[1]
			except:
				classe = ''
				assunto = ''
			julgador = busca(r'\n\s*?Relator.*?\:\n\s*?(.*?)\-', decisoes[d])
			orgao_julgador = busca(r'\n\s*?.rgão julgador\:\n\n\s*?(.*?)\n', decisoes[d])
			data_disponibilizacao = busca(r'\n\s*?Data d[oe]? publicação\s*?\:\n\n\s*?(\d{2}/\d{2}/\d{4})', decisoes[d])
			cursor.execute('INSERT INTO jurisprudencia_2_inst.jurisprudencia_2_inst (tribunal, numero, classe, assunto, data_decisao, orgao_julgador, julgador, texto_decisao) values ("%s","%s","%s","%s","%s","%s","%s","%s");' %	('ce',numero, classe, assunto, data_disponibilizacao, orgao_julgador, julgador, decisoes[d]))

if __name__ == '__main__':
	c = crawler_jurisprudencia_tjce()
	# print('comecei ',c.__class__.__name__)
	# try:
	# 	for l in range(len(c.lista_anos)):
	# 		print(c.lista_anos[l],'\n')
	# 		try:
	# 			crawler_jurisprudencia_tj.download_tj_ESAJ_recaptcha(c,crawler_jurisprudencia_tj,'0101'+c.lista_anos[l],'3112'+c.lista_anos[l],termo='processo')
	# 		except Exception as e:
	# 			print(e)
	# except Exception as e:
	# 	print('finalizei o ano com erro ', e)

	cursor = cursorConexao()
	cursor.execute('SELECT ementas from justica_estadual.jurisprudencia_ce;')
	dados = cursor.fetchall()
	for ementa in dados:
		c.parser_acordaos(ementa[0], cursor)