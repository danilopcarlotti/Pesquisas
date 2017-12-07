import sys, re
from crawlerJus import crawlerJus
from bs4 import BeautifulSoup

class crawler_jurisprudencia_tjpe():
	"""Crawler especializado em retornar textos da jurisprudência de segunda instância de Rio Grande do Norte"""
	def __init__(self):
		self.link_inicial = 'http://www.tjpe.jus.br/consultajurisprudenciaweb/xhtml/consulta/consulta.xhtml'
		self.pesquisa_livre = '//*[@id="formPesquisaJurisprudencia:inputBuscaSimples"]'
		self.data_julgamento_inicial = '//*[@id="formPesquisaJurisprudencia:j_id59InputDate"]'
		self.data_julgamento_final = '//*[@id="formPesquisaJurisprudencia:j_id61InputDate"]'
		self.botao_pesquisar = '//*[@id="formPesquisaJurisprudencia"]/div[5]/div/a[1]'