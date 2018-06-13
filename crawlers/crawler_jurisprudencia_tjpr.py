import sys, re, time
from bs4 import BeautifulSoup
from common.conexao_local import cursorConexao
from common_nlp.parse_texto import busca
from crawler_jurisprudencia_tj import crawler_jurisprudencia_tj
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from common.conexao_local import cursorConexao

class crawler_jurisprudencia_tjpr():
	"""Crawler especializado em retornar textos da jurisprudência de segunda instância do Paraná"""
	def __init__(self):
		crawler_jurisprudencia_tj.__init__(self)
		self.link_inicial = 'http://portal.tjpr.jus.br/jurisprudencia/'
		self.pesquisa_livre = 'pesquisaLivre'
		self.botao_pesquisar = '//*[@id="includeContent"]/table[2]/tbody/tr/td[2]/input'
		self.botao_proximo_iniXP = '//*[@id="navigator"]/div[1]/a[5]'
		self.botao_proximoXP = '//*[@id="navigator"]/div[1]/a[7]'
		self.tabela_colunas = 'justica_estadual.jurisprudencia_pr (ementas)'

	def download_tj(self, termo='ementa'):
		cursor = cursorConexao()
		driver = webdriver.Chrome(self.chromedriver)
		driver.get(self.link_inicial)
		driver.find_element_by_id(self.pesquisa_livre).send_keys(termo)
		driver.find_element_by_xpath(self.botao_pesquisar).click()
		time.sleep(1)
		contador = 0		
		texto = crawler_jurisprudencia_tj.extrai_texto_html(self,(driver.page_source).replace('"',''))
		cursor.execute('INSERT INTO %s value ("%s");' % (self.tabela_colunas,texto))
		driver.find_element_by_xpath(self.botao_proximo_iniXP).click()
		time.sleep(1)
		texto = crawler_jurisprudencia_tj.extrai_texto_html(self,(driver.page_source).replace('"',''))
		cursor.execute('INSERT INTO %s value ("%s");' % (self.tabela_colunas,texto))
		self.botao_proximo_iniXP = '//*[@id="navigator"]/div[1]/a[6]'
		driver.find_element_by_xpath(self.botao_proximo_iniXP).click()
		while True:
			try:
				texto = crawler_jurisprudencia_tj.extrai_texto_html(self,(driver.page_source).replace('"',''))
				cursor.execute('INSERT INTO %s value ("%s");' % (self.tabela_colunas,texto))
				driver.find_element_by_xpath(self.botao_proximoXP).click()
				time.sleep(2)
			except:
				sucesso = False
				while not sucesso:
					try:
						time.sleep(1)
						driver.execute_script("window.history.go(-1)")
						driver.find_element_by_xpath(self.botao_proximoXP).click()
						sucesso = True
					except:
						pass
		driver.close()

	def parser_acordaos(self,texto,cursor):
		decisoes = re.split(r'\n\d+\.\s*?\n',texto)
		for d in range(1,len(decisoes)):
			numero = busca(r'\d{7}\-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}', decisoes[d],ngroup=0)
			data_disponibilizacao = busca(r'\nData Publicação\:\s*?(\d{2}/\d{2}/\d{4})', decisoes[d])
			orgao_julgador = busca(r'\n.rgão Julgador\:(.+)', decisoes[d])
			julgador = busca(r'\nRelator.*?\:(.+)', decisoes[d])
			cursor.execute('INSERT INTO jurisprudencia_2_inst.jurisprudencia_2_inst (tribunal, numero, data_decisao, orgao_julgador, julgador, texto_decisao) values ("%s","%s","%s","%s","%s","%s");' % ('pr',numero, data_disponibilizacao, orgao_julgador, julgador, decisoes[d]))

if __name__ == '__main__':
	c = crawler_jurisprudencia_tjpr()
	# print('comecei ',c.__class__.__name__)
	# try:
	# 	c.download_tj()
	# except Exception as e:
	# 	print('finalizei com erro ',e)

	cursor = cursorConexao()
	cursor.execute('SELECT ementas from justica_estadual.jurisprudencia_pr limit 1000000')
	dados = cursor.fetchall()
	for dado in dados:
		c.parser_acordaos(dado[0], cursor)