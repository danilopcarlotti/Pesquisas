import sys, re, time
from crawler_jurisprudencia_tj import crawler_jurisprudencia_tj
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from conexao_local import cursorConexao

class crawler_jurisprudencia_tjpb():
	"""Crawler especializado em retornar textos da jurisprudência de segunda instância de Rio Grande do Norte"""
	def __init__(self):
		crawler_jurisprudencia_tj.__init__(self)
		self.link_inicial = 'http://juris.tjpb.jus.br/search?site=jurisp_digitalizada&client=tjpb_index&output=xml_no_dtd&proxystylesheet=tjpb_index&proxycustom=%3CHOME/%3E'
		self.pesquisa_livre = 'q'
		self.botao_pesquisar = '//*[@id="central"]/span/div/input[1]'
		self.tabela_colunas = 'justica_estadual.jurisprudencia_pb (ementas)'
		self.botao_proximo_iniXP = '//*[@id="content"]/div[2]/div[2]/div/div/span[2]/a '
		self.botao_proximoXP = '//*[@id="content"]/div[2]/div[2]/div/div/span[4]/a'
		self.tabela_colunas = 'justica_estadual.jurisprudencia_pb (ementas)'

	def download_tj(self):
		cursor = cursorConexao()
		driver = webdriver.Chrome(self.chromedriver)
		driver.get(self.link_inicial)
		driver.find_element_by_id(self.pesquisa_livre).send_keys('a')
		driver.find_element_by_xpath(self.botao_pesquisar).click()
		loop_counter = 0
		texto = crawler_jurisprudencia_tj.extrai_texto_html(self,(driver.page_source).replace('"',''))
		cursor.execute('INSERT INTO %s value ("%s");' % (self.tabela_colunas,texto))
		driver.find_element_by_xpath(self.botao_proximo_iniXP).click()
		while True:
			try:
				texto = crawler_jurisprudencia_tj.extrai_texto_html(self,(driver.page_source).replace('"',''))
				cursor.execute('INSERT INTO %s value ("%s");' % (self.tabela_colunas,texto))
				driver.find_element_by_xpath(self.botao_proximoXP).click()
				time.sleep(2)
			except:
				loop_counter += 1
				time.sleep(5)
				if loop_counter > 3:
					break
		driver.close()

if __name__ == '__main__':
	c = crawler_jurisprudencia_tjpb()
	print('comecei ',c.__class__.__name__)
	try:
		c.download_tj()
	except:
		print('finalizei')