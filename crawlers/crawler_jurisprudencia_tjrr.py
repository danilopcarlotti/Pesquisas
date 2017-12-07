import sys, re, time
from crawler_jurisprudencia_tj import crawler_jurisprudencia_tj
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from common.conexao_local import cursorConexao

class crawler_jurisprudencia_tjrr():
	"""Crawler especializado em retornar textos da jurisprudência de segunda instância de São Paulo"""
	def __init__(self):
		crawler_jurisprudencia_tj.__init__(self)
		self.link_inicial = 'http://www.tjrr.jus.br/sistemas/php/jurisprudencia/pesqform.php'
		self.pesquisa_livre = '//*[@id="pesqjuris"]/table/tbody/tr[5]/td[2]/input'
		self.botao_pesquisar = '//*[@id="pesqjuris"]/table/tbody/tr[11]/td/input'
		self.botao_proximoXP = '//*[@id="conteudo"]/table[1]/tbody/tr/td/a[%s]/b'
		self.lista_proximos = ['5','8','9','10']
		self.tabela_colunas = 'justica_estadual.jurisprudencia_rr (ementas)'

	def download_tj(self):
		cursor = cursorConexao()
		driver = webdriver.Chrome(self.chromedriver)
		driver.get(self.link_inicial)
		driver.find_element_by_xpath(self.pesquisa_livre).send_keys('a')
		driver.find_element_by_xpath(self.botao_pesquisar).click()
		for i in self.lista_proximos:
			bota_p = self.botao_proximoXP % i
			texto = crawler_jurisprudencia_tj.extrai_texto_html(self,(driver.page_source).replace('"',''))
			cursor.execute('INSERT INTO %s value ("%s");' % (self.tabela_colunas,texto))
			driver.find_element_by_xpath(bota_p).click()
		self.botao_proximoXP = '//*[@id="conteudo"]/table[1]/tbody/tr/td/a[11]/b'
		loop_counter = 0
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
					print('finalizei com erro')
					break
		driver.close()

if __name__ == '__main__':
	c = crawler_jurisprudencia_tjrr()
	print('comecei ',c.__class__.__name__)
	try:
		c.download_tj()
	except:
		print('finalizei com erro')