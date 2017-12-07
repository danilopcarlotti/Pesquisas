import sys, re, time
from crawler_jurisprudencia_tj import crawler_jurisprudencia_tj
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from common.conexao_local import cursorConexao

class crawler_jurisprudencia_tjpa():
	"""Crawler especializado em retornar textos da jurisprudência de segunda instância de São Paulo"""
	def __init__(self):
		crawler_jurisprudencia_tj.__init__(self)
		self.link_inicial = 'http://www.tjpa.jus.br/PortalExterno/institucional/Acordaos-e-Jurisprudencia/168242-Pesquisa-de-Jurisprudencia.xhtml'
		self.pesquisa_livre = '//*[@id="pesquisar"]/form/div/div/input[1]'
		self.botao_pesquisar = '//*[@id="pesquisar"]/form/div/div/input[2]'
		self.botao_proximo_iniXP = '//*[@id="resultados"]/div/div[1]/div[2]/div/span[1]/a'
		self.botao_proximoXP = '//*[@id="resultados"]/div/div[1]/div[2]/div/span[3]/a'
		self.tabela_colunas = 'justica_estadual.jurisprudencia_pa (ementas)'

	def download_tj(self):
		cursor = cursorConexao()
		driver = webdriver.Chrome(self.chromedriver)
		driver.get(self.link_inicial)
		driver.find_element_by_xpath(self.pesquisa_livre).send_keys('a')
		driver.find_element_by_xpath(self.botao_pesquisar).click()
		texto = crawler_jurisprudencia_tj.extrai_texto_html(self,(driver.page_source).replace('"',''))
		cursor.execute('INSERT INTO %s value ("%s");' % (self.tabela_colunas,texto))
		driver.find_element_by_xpath(self.botao_proximo_iniXP).click()
		loop_counter = 0
		while True:
			try:
				time.sleep(2)
				texto = crawler_jurisprudencia_tj.extrai_texto_html(self,(driver.page_source).replace('"',''))
				cursor.execute('INSERT INTO %s value ("%s");' % (self.tabela_colunas,texto))
				driver.find_element_by_xpath(self.botao_proximoXP).click()
			except:
				loop_counter += 1
				time.sleep(5)
				if loop_counter > 3:
					input('me ajude')
					# print('finalizei com erro\n')
					# break
		driver.close()

if __name__ == '__main__':
	c = crawler_jurisprudencia_tjpa()
	print('comecei ',c.__class__.__name__)
	try:
		c.download_tj()	
	except:
		print('finalizei com erro\n')