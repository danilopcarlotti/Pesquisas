import sys, re, os, time
from bs4 import BeautifulSoup
from common.conexao_local import cursorConexao
from crawler_jurisprudencia_tj import crawler_jurisprudencia_tj
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

sys.path.append(os.path.dirname(os.getcwd()))
from common_nlp.parse_texto import busca

class crawler_jurisprudencia_tjes():
	"""Crawler especializado em retornar textos da jurisprudência de segunda instância do Espírito Santo"""
	def __init__(self):
		crawler_jurisprudencia_tj.__init__(self)
		self.link_inicial = 'http://aplicativos.tjes.jus.br/sistemaspublicos/consulta_jurisprudencia/cons_jurisp.cfm'
		self.pesquisa_livre = 'edPesquisaJuris'
		self.botao_pesquisar = 'Pesquisar'
		self.tabela_colunas = 'justica_estadual.jurisprudencia_es (ementas)'
		self.botao_proximoXP = '//*[@id="conteudo"]/table[2]/tbody/tr[1]/td[2]/a[1]'

	def download_tj(self, termo='ementa'):
		cursor = cursorConexao()
		driver = webdriver.Chrome(self.chromedriver)
		driver.get(self.link_inicial)
		time.sleep(5)
		driver.find_element_by_id(self.pesquisa_livre).send_keys(termo)
		driver.find_element_by_id(self.botao_pesquisar).click()
		loop_counter = 0
		while True:
			try:
				texto = crawler_jurisprudencia_tj.extrai_texto_html(self,(driver.page_source).replace('"',''))
				cursor.execute('INSERT INTO %s value ("%s");' % (self.tabela_colunas,texto))
				driver.find_element_by_xpath(self.botao_proximoXP).click()
				time.sleep(2)
			except Exception as e:
				if loop_counter > 3:
					break
				loop_counter += 1
		driver.close()

	def parser_acordaos(self,texto, cursor):
		decisoes = re.split(r'\n\d+\.',texto)
		for d in range(1,len(decisoes)):
			numero = busca(r'\d{7}\-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}', decisoes[d],ngroup=0)
			classe = busca(r'\n\s*?Classe\:(.+)',decisoes[d])
			julgador = busca(r'\n\s*?Relator.*?\:\n\s*?(.*?)', decisoes[d])
			orgao_julgador = busca(r'\n\s*?.rgão julgador\:\n\s*?\n\s*?(.+)', decisoes[d])
			data_disponibilizacao = busca(r'\n\s*?Data d[oe]? julgamento\:\n\s*?\n\s*?(\d{2}/\d{2}/\d{4})', decisoes[d])
			cursor.execute('INSERT INTO jurisprudencia_2_inst.jurisprudencia_2_inst (tribunal, numero, classe, data_decisao, orgao_julgador, julgador, texto_decisao) values ("%s","%s","%s","%s","%s","%s","%s");' % ('es',numero, classe, data_disponibilizacao, orgao_julgador, julgador, decisoes[d]))


if __name__ == '__main__':
	c = crawler_jurisprudencia_tjes()
	# print('comecei ',c.__class__.__name__)
	# try:
	# 	c.download_tj()
	# except Exception as e:
	# 	print('finalizei com erro ',e)

	cursor = cursorConexao()
	cursor.execute('SELECT ementas from justica_estadual.jurisprudencia_es;')
	dados = cursor.fetchall()
	for dado in dados:
		c.parser_acordaos(dado[0], cursor)
