import sys, re, os
from common.conexao_local import cursorConexao
from crawler_jurisprudencia_tj import crawler_jurisprudencia_tj
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

sys.path.append(os.path.dirname(os.getcwd()))
from common_nlp.parse_texto import busca

class crawler_jurisprudencia_tjms():
	"""Crawler especializado em retornar textos da jurisprudência de segunda instância de Mato Grosso do Sul"""
	def __init__(self):
		crawler_jurisprudencia_tj.__init__(self)
		self.link_inicial = 'https://www.tjms.jus.br/cjsg/resultadoCompleta.do'
		self.pesquisa_livre = '//*[@id="iddados.buscaInteiroTeor"]'
		self.data_julgamento_inicialXP = '//*[@id="iddados.dtJulgamentoInicio"]'
		self.data_julgamento_finalXP = '//*[@id="iddados.dtJulgamentoFim"]'
		self.botao_pesquisar = '//*[@id="pbSubmit"]'
		self.botao_proximo_ini = '//*[@id="paginacaoSuperior-A"]/table/tbody/tr[1]/td[2]/div/a[5]'
		self.botao_proximo = '//*[@id="paginacaoSuperior-A"]/table/tbody/tr[1]/td[2]/div/a[6]'
		self.tabela_colunas = 'justica_estadual.jurisprudencia_ms (ementas)'

	def parser_acordaos(self,texto,cursor):
		def parse(texto_decisao,cursor):
			numero = busca(r'\d{7}\-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}', texto_decisao,ngroup=0)
			classe_assunto = busca(r'Classe/Assunto\:\n\s*?(.*?)\n', texto_decisao)
			classe = classe_assunto.split('/')[0]
			assunto = classe_assunto.split('/')[1]
			julgador = busca(r'\n\s*?Relator.*?\:\n\s*?(.*?)\n', texto_decisao)
			orgao_julgador = busca(r'\n\s*?.rgão julgador\:\n\s*?\n\s*?(.*?)\n', texto_decisao)
			origem = busca(r'\n\s*?Comarca\:\n\s*?\n\s*?(.*?)\n',texto_decisao)
			data_disponibilizacao = busca(r'\n\s*?Data de publicação\:\n\s*?\n\s*?(\d{2}/\d{2}/\d{4})', texto_decisao)
			cursor.execute('INSERT INTO jurisprudencia_2_inst.jurisprudencia_2_inst (tribunal, numero, assunto, classe, data_decisao, orgao_julgador, julgador, texto_decisao, origem) values ("%s","%s","%s","%s","%s","%s","%s","%s","%s");' % ('ms',numero, assunto, classe, data_disponibilizacao, orgao_julgador, julgador, texto_decisao, origem))
		decisoes = re.split(r'\n\s*?\d+\s*?\-\s*?\n',texto)
		for d in range(1,len(decisoes)):
			try:
				parse(decisoes[d],cursor)
			except:
				pass


if __name__ == '__main__':
	c = crawler_jurisprudencia_tjms()
# 	print('comecei ',c.__class__.__name__)
# 	try:
# 		for l in range(len(c.lista_anos)):
# 			print(c.lista_anos[l],'\n')
# 			try:
# 				crawler_jurisprudencia_tj.download_tj_ESAJ_recaptcha(c,crawler_jurisprudencia_tj,'0101'+c.lista_anos[l],'3112'+c.lista_anos[l])
# 			except Exception as e:
# 				print(e)
# 	except Exception as e:
# 		print('finalizei o ano com erro ',e)

	cursor = cursorConexao()
	cursor.execute('SELECT ementas from justica_estadual.jurisprudencia_ms limit 1000000')
	dados = cursor.fetchall()
	for dado in dados:
		c.parser_acordaos(dado[0], cursor)