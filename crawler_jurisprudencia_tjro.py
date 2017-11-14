import sys, re
from crawlerJus import crawlerJus
from bs4 import BeautifulSoup

class crawler_jurisprudencia_tjsp():
	"""Crawler especializado em retornar textos da jurisprudência de segunda instância de São Paulo"""
	def __init__(self):
		self.link_inicial = 'http://webapp.tjro.jus.br/juris/consulta/consultaJuris.jsf'
		self.pesquisa_livre = '//*[@id="frmJuris:formConsultaJuris:iPesquisa"]'
		self.botao_pesquisar = '//*[@id="frmJuris:formConsultaJuris:btPesquisar"]/span[2]'