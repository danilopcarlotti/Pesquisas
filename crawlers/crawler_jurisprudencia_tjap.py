import sys, re
from crawler_jurisprudencia_tj import crawler_jurisprudencia_tj
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

class crawler_jurisprudencia_tjap():
	"""Crawler especializado em retornar textos da jurisprudência de segunda instância do Amapá"""
	def __init__(self):
		crawler_jurisprudencia_tj.__init__(self)
		self.link_inicial = 'http://tucujuris.tjap.jus.br/tucujuris/pages/consultar-jurisprudencia/consultar-jurisprudencia.html'
		self.pesquisa_livre = 'ementa'
		self.botao_pesquisar = 'btPesquisar'

	def download_tj(self, termo='acordam'):
		driver = webdriver.Chrome(self.chromedriver)
		driver.get(self.link_inicial)
		time.sleep(2)
		driver.find_element_by_id(self.pesquisa_livre).send_keys(termo)
		driver.find_element_by_id(self.botao_pesquisar).click()
		while True:
			try:
				time.sleep(4)
				driver.find_element_by_id('btMaisResultados').click()
			except:
				break
		arq = open('jurisprudencia_tjap.txt','a')
		arq.write(crawler_jurisprudencia_tj.extrai_texto_html(self,driver.page_source))
		driver.close()

	def download_diario(self, ultimo_download=2765):
		driver = webdriver.Chrome(self.chromedriver)
		driver.get('http://tucujuris.tjap.jus.br/tucujuris/pages/consultar-dje/consultar-dje.html')
		time.sleep(5)
		driver.execute_script("document.getElementById('dje-%s').click()" % (str(ultimo_download+1),))
		time.sleep(5)
		#atualizar último_download

if __name__ == '__main__':
	c = crawler_jurisprudencia_tjap()
	print('comecei ',c.__class__.__name__)
	try:
		c.download_diario()
		# c.download_tj()
	except Exception as e:
		print('finalizei com erro ',e)