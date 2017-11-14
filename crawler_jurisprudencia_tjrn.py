import sys, re
from crawlerJus import crawlerJus
from bs4 import BeautifulSoup

class crawler_jurisprudencia_tjrn():
	"""Crawler especializado em retornar textos da jurisprudência de segunda instância de Rio Grande do Norte"""
	def __init__(self):
		self.link_inicial = 'http://esaj.tjrn.jus.br/cjosg/'
		self.pesquisa_livre = '/html/body/table[4]/tbody/tr/td/table[2]/tbody/tr[1]/td/div/form/table/tbody/tr/td/table/tbody/tr[2]/td[3]/input'
		self.data_julgamento_inicial = '/html/body/table[4]/tbody/tr/td/table[2]/tbody/tr[1]/td/div/form/table/tbody/tr/td/table/tbody/tr[7]/td[3]/table/tbody/tr/td[1]/input'
		self.data_julgamento_final = '/html/body/table[4]/tbody/tr/td/table[2]/tbody/tr[1]/td/div/form/table/tbody/tr/td/table/tbody/tr[7]/td[3]/table/tbody/tr/td[3]/input'
		self.botao_pesquisar = '/html/body/table[4]/tbody/tr/td/table[2]/tbody/tr[1]/td/div/form/table/tbody/tr/td/table/tbody/tr[7]/td[3]/table/tbody/tr/td[3]/input'