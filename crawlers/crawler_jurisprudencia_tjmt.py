import sys, re
from crawlerJus import crawlerJus
from bs4 import BeautifulSoup

class crawler_jurisprudencia_tjmt():
	"""Crawler especializado em retornar textos da jurisprudência de segunda instância de Tocantins"""
	def __init__(self):
		self.link_inicial = 'http://jurisprudencia.tjmt.jus.br/'
		self.pesquisa_livre = '//*[@id="FiltroBasico"]'
		self.botao_pesquisar = '//*[@id="BotaoConsulta"]'