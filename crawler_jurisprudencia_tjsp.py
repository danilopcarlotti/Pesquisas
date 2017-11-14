import sys, re
from crawlerJus import crawlerJus
from bs4 import BeautifulSoup

class crawler_jurisprudencia_tjsp():
	"""Crawler especializado em retornar textos da jurisprudência de segunda instância de São Paulo"""
	def __init__(self):
		self.link_inicial = 'https://esaj.tjsp.jus.br/cjsg/consultaCompleta.do'
		self.pesquisa_livre = '//*[@id="iddados.buscaInteiroTeor"]'
		self.data_julgamento_inicial = '//*[@id="iddados.dtJulgamentoInicio"]'
		self.data_julgamento_final = '//*[@id="iddados.dtJulgamentoFim"]'
		self.botao_pesquisar = '//*[@id="pbSubmit"]'