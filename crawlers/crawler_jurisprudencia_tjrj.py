import sys, re, time
from crawler_jurisprudencia_tj import crawler_jurisprudencia_tj
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from common.conexao_local import cursorConexao

class crawler_jurisprudencia_tjrj():
	"""Crawler especializado em retornar textos da jurisprudência de segunda instância do Rio de Janeiro"""
	def __init__(self):
		crawler_jurisprudencia_tj.__init__(self)
		self.link_inicial = 'http://www4.tjrj.jus.br/ejuris/ConsultarJurisprudencia.aspx'
		self.pesquisa_livre = '//*[@id="ContentPlaceHolder1_txtTextoPesq"]'
		self.botao_pesquisar = '//*[@id="ContentPlaceHolder1_btnPesquisar"]'
		self.botao_proximo_iniXP = '//*[@id="placeholder"]/span/table/tbody/tr[7]/td/a'
		self.botao_proximo_XP = '//*[@id="placeholder"]/span/table/tbody/tr[7]/td/a[2]'
		self.tabela_colunas = 'justica_estadual.jurisprudencia_tjrj (ementas)'

	def download_tj(self):
		cursor = cursorConexao()
		driver = webdriver.Chrome(self.chromedriver)
		driver.get(self.link_inicial)
		driver.find_element_by_xpath(self.pesquisa_livre).send_keys('direito')
		driver.find_element_by_xpath(self.botao_pesquisar).click()
		time.sleep(4)
		texto = crawler_jurisprudencia_tj.extrai_texto_html(self,(driver.page_source).replace('"',''))
		cursor.execute('INSERT INTO %s value ("%s");' % (self.tabela_colunas,texto))
		driver.find_element_by_xpath(self.botao_proximo_iniXP).click()
		while True:
			try:
				time.sleep(4)
				texto = crawler_jurisprudencia_tj.extrai_texto_html(self,(driver.page_source).replace('"',''))
				cursor.execute('INSERT INTO %s value ("%s");' % (self.tabela_colunas,texto))
				driver.find_element_by_xpath(self.botao_proximo_XP).click()
			except Exception as e:
				print(e)

if __name__ == '__main__':
	c = crawler_jurisprudencia_tjrj()
	print('comecei ',c.__class__.__name__)
	try:
		c.download_tj()
	except Exception as e:
		print(e)
