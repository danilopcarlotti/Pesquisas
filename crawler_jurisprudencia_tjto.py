import sys, re
from crawlerJus import crawlerJus
from bs4 import BeautifulSoup

class crawler_jurisprudencia_tjsp():
	"""Crawler especializado em retornar textos da jurisprudência de segunda instância de Tocantins"""
	def __init__(self):
		self.link_inicial = 'http://jurisprudencia.tjto.jus.br/'
		self.pesquisa_livre = '//*[@id="consulta_input"]'
		self.data_julgamento_inicial = '//*[@id="iddados.dtJulgamentoInicio"]'
		self.data_julgamento_final = '//*[@id="iddados.dtJulgamentoFim"]'
		self.botao_pesquisar = '/html/body/div[1]/div/form/div/div/div/div/button'
		

		

