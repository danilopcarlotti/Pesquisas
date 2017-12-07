import sys, re, time
from crawler_jurisprudencia_tj import crawler_jurisprudencia_tj
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from common.conexao_local import cursorConexao

class crawler_jurisprudencia_tjba():
	"""Crawler especializado em retornar textos da jurisprudência de segunda instância da Bahia"""
	def __init__(self):
		crawler_jurisprudencia_tj.__init__(self)
		self.link_inicial = 'https://www2.tjba.jus.br/erp-portal/publico/jurisprudencia/consultaJurisprudencia.xhtml'
		self.pesquisa_livre = 'palavrasChaveId'
		self.botao_pesquisar = 'j_idt153'
		self.data_julgamento_inicialID = 'dtJulgamentoInicialId_input'
		self.data_julgamento_finalID = 'dtJulgamentoFinalId_input'
		self.botao_proximoXP = '//*[@id="jurisprudenciaGridId_paginator_top"]/span[5]/span'
		self.tabela_colunas = 'justica_estadual.jurisprudencia_ba (ementas)'

	def download_tj(self,data_ini,data_fim):
		cursor = cursorConexao()
		driver = webdriver.Chrome(self.chromedriver)
		driver.get(self.link_inicial)
		driver.find_element_by_id(self.pesquisa_livre).send_keys('acordam')
		driver.find_element_by_id(self.data_julgamento_inicialID).send_keys(data_ini)
		driver.find_element_by_id(self.data_julgamento_finalID).send_keys(data_fim)
		driver.find_element_by_id(self.botao_pesquisar).click()
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
	c = crawler_jurisprudencia_tjba()
	print('comecei ',c.__class__.__name__)
	for l in c.lista_anos:
		try:
			print(l[0], '  ',l[1])
			c.download_tj(l[0],l[1])
		except:
			print('finalizei com erro o ano ',l[0],'  ',l[1])