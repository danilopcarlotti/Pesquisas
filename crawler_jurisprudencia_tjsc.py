import sys, re
from crawlerJus import crawlerJus
from bs4 import BeautifulSoup

class crawler_jurisprudencia_tjsc():
	"""Crawler especializado em retornar textos da jurisprudência de segunda instância de São Paulo"""
	def __init__(self):
		self.link_inicial = 'http://busca.tjsc.jus.br/jurisprudencia/buscaForm.do'
		self.pesquisa_livre = '//*[@id="q"]'
		self.inteiro_teor = '//*[@id="busca_avancada"]/table[1]/tbody/tr/td[2]/span[1]]'
		self.data_julgamento_inicial = '//*[@id="dtini"]'
		self.data_julgamento_final = '//*[@id="dtfim"]'
		self.botao_pesquisar = '//*[@id="busca_avancada"]/input[2]'