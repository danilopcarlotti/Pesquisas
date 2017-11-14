import sys, re
from crawlerJus import crawlerJus
from bs4 import BeautifulSoup

class crawler_jurisprudencia_tjgo():
	"""Crawler especializado em retornar textos da jurisprudência de segunda instância de São Paulo"""
	def __init__(self):
		self.link_inicial = 'http://www.tjgo.jus.br/jurisprudencia/juris.php'
		self.pesquisa_livre = '//*[@id="SearchText"]'
		self.botao_pesquisar = '//*[@id="button1"]'
