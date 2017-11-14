import sys, re
from crawlerJus import crawlerJus
from bs4 import BeautifulSoup

class crawler_jurisprudencia_tjba():
	"""Crawler especializado em retornar textos da jurisprudência de segunda instância de São Paulo"""
	def __init__(self):
		self.link_inicial = 'https://www2.tjba.jus.br/erp-portal/publico/jurisprudencia/consultaJurisprudencia.xhtml'

		

