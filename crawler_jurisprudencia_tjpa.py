import sys, re
from crawlerJus import crawlerJus
from bs4 import BeautifulSoup

class crawler_jurisprudencia_tjpa():
	"""Crawler especializado em retornar textos da jurisprudência de segunda instância de São Paulo"""
	def __init__(self):
		self.link_inicial = 'http://www.tjpa.jus.br/PortalExterno/institucional/Acordaos-e-Jurisprudencia/168242-Pesquisa-de-Jurisprudencia.xhtml'
		self.pesquisa_livre = '//*[@id="pesquisar"]/form/div/div/input[1]'
		self.botao_pesquisar = '//*[@id="pesquisar"]/form/div/div/input[2]'