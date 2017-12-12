import sys, re, time, os
from crawler_jurisprudencia_tj import crawler_jurisprudencia_tj
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from common.conexao_local import cursorConexao

class crawler_jurisprudencia_tjmt():
	"""Crawler especializado em retornar textos da jurisprudência de segunda instância do Mato Grosso"""
	def __init__(self):
		crawler_jurisprudencia_tj.__init__(self)
		self.link_inicial = 'http://jurisprudencia.tjmt.jus.br/'
		self.pesquisa_livre = '//*[@id="FiltroBasico"]'
		self.botao_pesquisar = '//*[@id="BotaoConsulta"]' 
		self.botao_proximo_XP = '//*[@id="AcordaoPagination"]/ul/li[%s]/a'  
		self.tabela_colunas = 'justica_estadual.jurisprudencia_mt (ementas)' 

	def download_tj(self):
		cursor = cursorConexao()
		driver = webdriver.Chrome(self.chromedriver)
		driver.get(self.link_inicial)
		driver.find_element_by_xpath(self.pesquisa_livre).send_keys('a')
		driver.find_element_by_xpath(self.botao_pesquisar).click()
		time.sleep(5)
		texto = crawler_jurisprudencia_tj.extrai_texto_html(self,(driver.page_source).replace('"',''))
		cursor.execute('INSERT INTO %s value ("%s");' % (self.tabela_colunas,texto))
		botao_prox = self.botao_proximo_XP % '10'
		driver.find_element_by_xpath(botao_prox).click()
		contador_proximo = 2
		while True:
			try:
				time.sleep(2)
				texto = crawler_jurisprudencia_tj.extrai_texto_html(self,(driver.page_source).replace('"',''))
				cursor.execute('INSERT INTO %s value ("%s");' % (self.tabela_colunas,texto))
				if contador_proximo < 4:
					contador_proximo += 1
				elif contador_proximo < 6:
					botao_prox = self.botao_proximo_XP % str(contador_proximo + 7)
					contador_proximo += 1
				else:
					botao_prox = self.botao_proximo_XP % '13'
				driver.find_element_by_xpath(botao_prox).click()
			except Exception as e:
				print(e)
				if input('ajude-me'):
					pass
		driver.close()

if __name__ == '__main__':
	c = crawler_jurisprudencia_tjmt()
	print('comecei ',c.__class__.__name__)
	try:
		c.download_tj()
	except Exception as e:
		print(e)
		print('finalizei com erro\n')