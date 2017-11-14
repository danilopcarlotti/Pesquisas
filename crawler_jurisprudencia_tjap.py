import sys, re
from crawlerJus import crawlerJus
from bs4 import BeautifulSoup

class crawler_jurisprudencia_tjap():
	"""Crawler especializado em retornar textos da jurisprudência de segunda instância de São Paulo"""
	def __init__(self):
		self.link_inicial = 'http://tucujuris.tjap.jus.br/tucujuris/pages/consultar-jurisprudencia/consultar-jurisprudencia.html'
		self.pesquisa_livre = '//*[@id="ementa"]'
		self.botao_pesquisar = '//*[@id="btPesquisar"]'