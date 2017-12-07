from crawler_jurisprudencia_tj import crawler_jurisprudencia_tj
import time, datetime, urllib.request,logging, click, os
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
				req = urllib.request.Request(link, headers={'User-Agent': 'Mozilla/5.0'})
				html = urllib.request.urlopen(req,timeout=5).read()
				texto = crawler_jurisprudencia_tj.extrai_texto_html(self,(html)).replace('"','')
				cursor.execute('INSERT INTO %s value ("%s");' % (self.tabela_colunas,texto))
			except:
				print('erro com ',i)

if __name__ == '__main__':
	c = crawler_jurisprudencia_tjto()
	print('comecei ',c.__class__.__name__)
	try:
		c.download_tj()
	except:
		print('finalizei com erro\n')