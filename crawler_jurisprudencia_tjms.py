import sys, re, os
from crawler_jurisprudencia_tj import crawler_jurisprudencia_tj
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class crawler_jurisprudencia_tjms():
	"""Crawler especializado em retornar textos da jurisprudência de segunda instância de São Paulo"""
	def __init__(self):
		crawler_jurisprudencia_tj.__init__(self)
		self.link_inicial = 'https://www.tjms.jus.br/cjsg/resultadoCompleta.do'
		self.pesquisa_livre = '//*[@id="iddados.buscaInteiroTeor"]'
		self.data_julgamento_inicialXP = '//*[@id="iddados.dtJulgamentoInicio"]'
		self.data_julgamento_finalXP = '//*[@id="iddados.dtJulgamentoFim"]'
		self.botao_pesquisar = '//*[@id="pbSubmit"]'
		self.botao_proximo_ini = '//*[@id="paginacaoSuperior-A"]/table/tbody/tr[1]/td[2]/div/a[5]'
		self.botao_proximo = '//*[@id="paginacaoSuperior-A"]/table/tbody/tr[1]/td[2]/div/a[6]'
		self.tabela_colunas = 'justica_estadual.jurisprudencia_ms (ementas)'

if __name__ == '__main__':
	# só vai baixar as ementas
	c = crawler_jurisprudencia_tjms()
	print('comecei ',c.__class__.__name__)
	for l in c.lista_anos:
		try:
			print(l[0],'  ',l[1])
			crawler_jurisprudencia_tj.download_tj_ESAJ(c,crawler_jurisprudencia_tj,l[0],l[1],'a')
		except:
			print('finalizei o ano',l[0],' ',l[1])