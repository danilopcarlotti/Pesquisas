import sys, re
from crawlerJus import crawlerJus
from bs4 import BeautifulSoup

class crawler_jurisprudencia_tjpi():
	"""Crawler especializado em retornar textos da jurisprudência de segunda instância de Piauí"""
	def __init__(self):
		self.link_inicial = 'http://www.tjpi.jus.br/e-tjpi/home/jurisprudencia'
		self.pesquisa_livre = '//*[@id="palavras_chave"]'
		self.data_julgamento_inicial = '//*[@id="data_inicio"]'
		self.data_julgamento_final = '//*[@id="data_fim"]'
		self.botao_pesquisar = '//*[@id="filtros"]/button'