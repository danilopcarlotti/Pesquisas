from crawler_jurisprudencia_tj import crawler_jurisprudencia_tj
import time, datetime, urllib.request,logging, click, os, sys
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
from common.conexao_local import cursorConexao

class crawler_jurisprudencia_tjto():
	"""Crawler especializado em retornar textos da jurisprudência de segunda instância do Tocantins"""
	def __init__(self):
		crawler_jurisprudencia_tj.__init__(self)
		self.link_inicial = 'http://jurisprudencia.tjto.jus.br/consulta?q=a&start=%s&rows=20'
		self.tabela_colunas = 'justica_estadual.jurisprudencia_to (ementas)'

	def download_tj(self):
		cursor = cursorConexao()
		for i in range(0,65501,20):
			try:
				link = self.link_inicial % str(i)
				driver = webdriver.Chrome(self.chromedriver)
				driver.get(self.link)
				links_inteiro_teor = driver.find_elements_by_link_text('Inteiro Teor')
				for l in links_inteiro_teor:
					try:
						cursor.execute('INSERT INTO %s value ("%s");' % (self.tabela_colunas,l.get_attribute('href')))		
					except:
						pass
			except Exception as e:
				print('erro com ',i,' ',e)

if __name__ == '__main__':
	c = crawler_jurisprudencia_tjto()
	print('comecei ',c.__class__.__name__)
	try:
		c.download_tj()
	except Exception as e:
		print('finalizei com erro ',e)