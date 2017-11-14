import sys, re
from crawlerJus import crawlerJus
from bs4 import BeautifulSoup

class crawler_jurisprudencia_tjrr():
	"""Crawler especializado em retornar textos da jurisprudência de segunda instância de São Paulo"""
	def __init__(self):
		self.link_inicial = 'http://www.tjrr.jus.br/sistemas/php/jurisprudencia/pesqform.php'
		self.pesquisa_livre = '//*[@id="pesqjuris"]/table/tbody/tr[5]/td[2]/input'
		self.data_julgamento_inicial = '//*[@id="djulIni"]'
		self.data_julgamento_final = '//*[@id="djulFim"]'
		self.botao_pesquisar = '//*[@id="pesqjuris"]/table/tbody/tr[11]/td/input'