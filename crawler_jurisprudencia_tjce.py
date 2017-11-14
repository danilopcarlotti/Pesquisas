import sys, re
from crawlerJus import crawlerJus
from bs4 import BeautifulSoup

class crawler_jurisprudencia_tjce():
	"""Crawler especializado em retornar textos da jurisprudência de segunda instância de Ceará"""
	def __init__(self):
		self.link_inicial = 'www.tjce.jus.br/institucional/consulta-de-acordao/'
		self.pesquisa_livre = '/html/body/table[4]/tbody/tr/td/form/table[2]/tbody/tr/td[2]/input'
		self.data_julgamento_inicial = '//*[@id="dtJulgamentoInicio"]/input'
		self.data_julgamento_final = '//*[@id="dtJulgamentoFim"]/input'
		self.botao_pesquisar = '//*[@id="pbSubmit"]'