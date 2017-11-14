import sys, re
from crawlerJus import crawlerJus
from bs4 import BeautifulSoup

class crawler_jurisprudencia_tjpr():
	"""Crawler especializado em retornar textos da jurisprudência de segunda instância de São Paulo"""
	def __init__(self):
		self.link_inicial = 'http://portal.tjpr.jus.br/jurisprudencia/'
		self.pesquisa_livre = '//*[@id="criterioPesquisa"]'
		self.data_julgamento_inicial = '//*[@id="dataJulgamentoInicio"]'
		self.data_julgamento_final = '//*[@id="dataJulgamentoFim"]'
		self.botao_pesquisar = '//*[@id="includeContent"]/table[3]/tbody/tr/td[2]/input'