import sys, re
from crawlerJus import crawlerJus
from bs4 import BeautifulSoup

class crawler_jurisprudencia_tjpb():
	"""Crawler especializado em retornar textos da jurisprudência de segunda instância de Rio Grande do Norte"""
	def __init__(self):
		self.link_inicial = 'http://juris.tjpb.jus.br/search?site=jurisp_digitalizada&client=tjpb_index&output=xml_no_dtd&proxystylesheet=tjpb_index&proxycustom=%3CHOME/%3E'
		self.pesquisa_livre = '//*[@id="q"]'
		self.data_julgamento_inicial = '//*[@id="dataIni"]'
		self.data_julgamento_final = '//*[@id="dataFim"]'
		self.botao_pesquisar = '//*[@id="central"]/span/div/input[1]'