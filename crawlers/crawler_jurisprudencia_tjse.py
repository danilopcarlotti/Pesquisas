import sys, re, time
from crawler_jurisprudencia_tj import crawler_jurisprudencia_tj
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from common.conexao_local import cursorConexao

class crawler_jurisprudencia_tjse():
	"""Crawler especializado em retornar textos da jurisprudência de segunda instância de Santa Catarina"""
	def __init__(self):
		crawler_jurisprudencia_tj.__init__(self)
		self.link_inicial = 'http://www.tjse.jus.br/Dgorg/paginas/jurisprudencia/consultarJurisprudencia.tjse'
		self.pesquisa_livre = '//*[@id="itTermos"]'
		self.botao_pesquisar = '//*[@id="btPesquisarVoto"]'
		self.tabela_colunas = 'justica_estadual.jurisprudencia_se (ementas)'
		self.botao_proximoXP = '//*[@id="dgResultadoJurisprudencia2_paginator_top"]/a[3]'

	def download_tj(self):
		cursor = cursorConexao()
		driver = webdriver.Chrome(self.chromedriver)
		driver.get(self.link_inicial)
		time.sleep(1)
		driver.find_element_by_xpath(self.pesquisa_livre).send_keys('processo')
		if input('Resolva o captcha do Google e digite um número diferente de zero:\n'):
			pass
		contador_loop = 0
		while True:
			try:
				time.sleep(1)
				texto = crawler_jurisprudencia_tj.extrai_texto_html(self,driver.page_source).replace('"','')
				cursor.execute('INSERT INTO %s value ("%s");' % (self.tabela_colunas,texto))
				driver.find_element_by_xpath(self.botao_proximoXP).click()
			except Exception as e:
				print(e)
				time.sleep(2)
				if contador_loop > 2:
					break
				contador_loop += 1
		driver.close()
		time.sleep(1)

def main():
	pass

if __name__ == '__main__':
	c = crawler_jurisprudencia_tjse()
	print('comecei ',c.__class__.__name__)
	try:
		c.download_tj()
	except Exception as e:
		print(e)