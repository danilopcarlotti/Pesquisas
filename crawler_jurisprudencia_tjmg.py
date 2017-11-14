import sys, re
from crawlerJus import crawlerJus
from bs4 import BeautifulSoup

class crawler_jurisprudencia_tjmg():
	"""Crawler especializado em retornar textos da jurisprudência de segunda instância de São Paulo"""
	def __init__(self):
		self.link_inicial = 'http://www5.tjmg.jus.br/jurisprudencia/formEspelhoAcordao.do'
		self.pesquisa_livre = '//*[@id="palavras"]'
		self.inteiro_teor = '//*[@id="pesqAcordao"]'
		self.data_julgamento_inicial = '//*[@id="dataJulgamentoInicial"]'
		self.data_julgamento_final = '//*[@id="dataJulgamentoFinal"]'
		self.botao_pesquisar = '//*[@id="pesquisaLivre"]'
		self.link_captcha = '/html/body/table/tbody/tr[3]/td/table/tbody/tr[3]/td/a[2]'