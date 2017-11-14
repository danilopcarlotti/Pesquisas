import sys, re
from crawlerJus import crawlerJus
from bs4 import BeautifulSoup

class crawler_jurisprudencia_tjdf():
	"""Crawler especializado em retornar textos da jurisprudência de segunda instância de São Paulo"""
	def __init__(self):
		self.link_inicial = 'https://pesquisajuris.tjdft.jus.br/IndexadorAcordaos-web/sistj?visaoId=tjdf.sistj.acordaoeletronico.buscaindexada.apresentacao.VisaoBuscaAcordao'
		self.pesquisa_livre = '//*[@id="argumentoDePesquisa"]'
		self.data_julgamento_inicial = '//*[@id="dataInicio"]'
		self.data_julgamento_final = '//*[@id="dataFim"]'
		self.botao_pesquisar = '//*[@id="id_comando_pesquisar"]'
		

		

