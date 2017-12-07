import sys, re, os
from crawler_jurisprudencia_tj import crawler_jurisprudencia_tj
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class crawler_jurisprudencia_tjal():
	"""Crawler especializado em retornar textos da jurisprudência de segunda instância de Alagoas"""
	def __init__(self):
		crawler_jurisprudencia_tj.__init__(self)
		self.link_inicial = 'https://www2.tjal.jus.br/cjsg/consultaCompleta.do'
		self.pesquisa_livre = '/html/body/table[4]/tbody/tr/td/form/table[2]/tbody/tr/td[2]/input'
		self.data_julgamento_inicialXP = '//*[@id="dtJulgamentoInicio"]/input'
		self.data_julgamento_finalXP = '//*[@id="dtJulgamentoFim"]/input'
		self.botao_pesquisar = '//*[@id="pbSubmit"]'
		self.botao_proximo_ini = '//*[@id="paginacaoSuperior-A"]/table/tbody/tr[1]/td[2]/div/a[5]'
		self.botao_proximo = '//*[@id="paginacaoSuperior-A"]/table/tbody/tr[1]/td[2]/div/a[7]'
		self.tabela_colunas = 'justica_estadual.jurisprudencia_al (ementas)'

if __name__ == '__main__':
	c = crawler_jurisprudencia_tjal()
	print('comecei ',c.__class__.__name__)
	for l in c.lista_anos:
		try:
			print(l,'\n')
			crawler_jurisprudencia_tj.download_tj_ESAJ(c,crawler_jurisprudencia_tj,'01/01/'+l,'31/12/'+l)
		except:
			print('finalizei o ano ',l,' com erro\n')