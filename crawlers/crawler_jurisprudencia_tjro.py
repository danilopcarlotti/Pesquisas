import sys, re, time
from crawler_jurisprudencia_tj import crawler_jurisprudencia_tj
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from common.conexao_local import cursorConexao

class crawler_jurisprudencia_tjro():
	"""Crawler especializado em retornar textos da jurisprudência de segunda instância de Rondônia"""
	def __init__(self):
		crawler_jurisprudencia_tj.__init__(self)
		self.link_inicial = 'http://webapp.tjro.jus.br/juris/consulta/consultaJuris.jsf'
		self.pesquisa_livreXP = '//*[@id="frmJuris:formConsultaJuris:iPesquisa"]'
		self.botao_pesquisarXP = '//*[@id="frmJuris:formConsultaJuris:btPesquisar"]'
		self.link_decisoesXP = '//*[@id="frmJuris:formDetalhesJuris:painelResultadosPesquisa_data"]/tr[1]/td/span/input'
		self.botao_proximoXP = '//*[@id="frmJuris:formDetalhesJuris:painelProcessosAcordaos_paginator_bottom"]/a[3]/span'
		self.tabela_colunas = 'justica_estadual.jurisprudencia_ro (ementas)'

	def download_tj(self):
		cursor = cursorConexao()
		driver = webdriver.Chrome(self.chromedriver)
		driver.get(self.link_inicial)
		driver.find_element_by_xpath(self.pesquisa_livreXP).send_keys('ementa')
		driver.find_element_by_xpath(self.botao_pesquisarXP).click()
		driver.find_element_by_xpath(self.link_decisoesXP).click()
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
					break
		driver.close()

if __name__ == '__main__':
	c = crawler_jurisprudencia_tjro()
	print('comecei ',c.__class__.__name__)
	try:
		c.download_tj()
	except:
		print('finalizei com erro\n')