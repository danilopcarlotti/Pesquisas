import sys, re, time
from crawler_jurisprudencia_tj import crawler_jurisprudencia_tj
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from common.conexao_local import cursorConexao

class crawler_jurisprudencia_tjgo():
	"""Crawler especializado em retornar textos da jurisprudência de segunda instância de São Paulo"""
	def __init__(self):
		crawler_jurisprudencia_tj.__init__(self)
		self.link_inicial = 'http://www.tjgo.jus.br/jurisprudencia/juris.php'
		self.pesquisa_livre = 'SearchText'
		self.botao_pesquisar = 'button1'
		self.botao_proximoXP = '//*[@id="posicao"]'
		self.botao_proximo = '//*[@id="button3"]'
		self.tabela_colunas = 'justica_estadual.jurisprudencia_go (ementas)'
		self.contador_paginas = 2

	def download_tj(self):
		cursor = cursorConexao()
		driver = webdriver.Chrome(self.chromedriver)
		driver.get(self.link_inicial)
		driver.find_element_by_id(self.pesquisa_livre).send_keys('acordam')
		driver.find_element_by_id(self.botao_pesquisar).click()
		texto = crawler_jurisprudencia_tj.extrai_texto_html(self,(driver.page_source).replace('"',''))
		cursor.execute('INSERT INTO %s value ("%s");' % (self.tabela_colunas,texto))
		loop_counter = 0
		while True:
			try:
				driver.find_element_by_xpath(self.botao_proximoXP).clear()
				driver.find_element_by_xpath(self.botao_proximoXP).send_keys(str(self.contador_paginas))
				driver.find_element_by_xpath(self.botao_proximo).click()
				time.sleep(2)
				self.contador_paginas += 1
				texto = crawler_jurisprudencia_tj.extrai_texto_html(self,(driver.page_source).replace('"',''))
				cursor.execute('INSERT INTO %s value ("%s");' % (self.tabela_colunas,texto))
			except:

				loop_counter +=1
				if loop_counter > 3:
					break
				time.sleep(5)
				driver.execute_script("window.history.go(-1)")
		driver.close()

if __name__ == '__main__':
	c = crawler_jurisprudencia_tjgo()
	print('comecei ',c.__class__.__name__)
	try:
		c.download_tj()
	except:
		print('finalizei')