import sys, re, os
from crawler_jurisprudencia_tj import crawler_jurisprudencia_tj
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class crawler_jurisprudencia_tjrn():
	"""Crawler especializado em retornar textos da jurisprudência de segunda instância de Rio Grande do Norte"""
	def __init__(self):
		crawler_jurisprudencia_tj.__init__(self)
		self.link_inicial = 'http://esaj.tjrn.jus.br/cjosg/'
		self.pesquisa_livre = '/html/body/table[4]/tbody/tr/td/table[2]/tbody/tr[1]/td/div/form/table/tbody/tr/td/table/tbody/tr[1]/td[3]/input'
		self.data_julgamento_inicialXP = '/html/body/table[4]/tbody/tr/td/table[2]/tbody/tr[1]/td/div/form/table/tbody/tr/td/table/tbody/tr[7]/td[3]/table/tbody/tr/td[1]/input'
		self.data_julgamento_finalXP = '/html/body/table[4]/tbody/tr/td/table[2]/tbody/tr[1]/td/div/form/table/tbody/tr/td/table/tbody/tr[7]/td[3]/table/tbody/tr/td[3]/input'
		self.botao_pesquisar = '/html/body/table[4]/tbody/tr/td/table[2]/tbody/tr[1]/td/div/form/table/tbody/tr/td/table/tbody/tr[9]/td[3]/input[1]'
		self.botao_proximo_ini = '/html/body/table[4]/tbody/tr/td/table/tbody/tr/td/table[4]/tbody/tr[2]/td/table/tbody/tr[2]/td/table/tbody/tr/td[27]/a'
		self.botao_proximo = '/html/body/table[4]/tbody/tr/td/table/tbody/tr/td/table[4]/tbody/tr[2]/td/table/tbody/tr[2]/td/table/tbody/tr/td[27]/a'
		self.tabela_colunas = 'justica_estadual.jurisprudencia_rn (ementas)'
		self.link_esaj = ''

if __name__ == '__main__':
	c = crawler_jurisprudencia_tjrn()
	print('comecei ',c.__class__.__name__)
	for l in c.lista_anos:
		try:
			print(l,'\n')
			crawler_jurisprudencia_tj.download_tj_ESAJ(c,crawler_jurisprudencia_tj,'0101'+l,'3112'+l,termo='ementa')
		except Exception as e:
			print(e)

# 