import sys, re
from crawlerJus import crawlerJus
from bs4 import BeautifulSoup

class crawler_jurisprudencia_tjma():
	"""Crawler especializado em retornar textos da jurisprudência de segunda instância de Maranhão"""
	def __init__(self):
		self.link_inicial = 'http://jurisconsult.tjma.jus.br/'
		self.pesquisa_livre = '//*[@id="txtChaveJurisprudencia"]'
		self.data_julgamento_inicial = '//*[@id="dp1510686081205"]'
		self.data_julgamento_final = '//*[@id="dp1510686081206"]'
		self.botao_pesquisar = '//*[@id="btnConsultar"]'