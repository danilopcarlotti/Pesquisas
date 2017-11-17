import sys, re
from crawler_jurisprudencia_tj import crawler_jurisprudencia_tj
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from conexao_local import cursorConexao
import time

class crawler_jurisprudencia_tjba():
	"""Crawler especializado em retornar textos da jurisprudência de segunda instância da Bahia"""
	def __init__(self):
		self.link_inicial = 'https://www2.tjba.jus.br/erp-portal/publico/jurisprudencia/consultaJurisprudencia.xhtml'
		self.pesquisa_livre = 'palavrasChaveId'
		self.botao_pesquisar = 'j_idt153'

	def download_tj(self):
		cursor = cursorConexao()
		driver = webdriver.Chrome(self.chromedriver)
		driver.get(self.link_inicial)
		driver.find_element_by_id(self.pesquisa_livre).send_keys('acordam')


if __name__ == '__main__':
	c = crawler_jurisprudencia_tjba()
	print('comecei ',c.__class__.__name__)
	c.download_tj()