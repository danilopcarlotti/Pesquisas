import sys, re
from crawlerJus import crawlerJus
from bs4 import BeautifulSoup

class crawler_jurisprudencia_tjes():
	"""Crawler especializado em retornar textos da jurisprudência de segunda instância de São Paulo"""
	def __init__(self):
		self.link_inicial = 'http://aplicativos.tjes.jus.br/sistemaspublicos/consulta_jurisprudencia/cons_jurisp.cfm'
		self.pesquisa_livre = '//*[@id="edPesquisaJuris"]'
		self.data_julgamento_inicial = '//*[@id="edIni"]'
		self.data_julgamento_final = '//*[@id="edFim"]'
		self.botao_pesquisar = '//*[@id="Pesquisar"]'
