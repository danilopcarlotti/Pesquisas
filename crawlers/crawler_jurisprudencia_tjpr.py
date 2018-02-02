import sys, re, time
from crawler_jurisprudencia_tj import crawler_jurisprudencia_tj
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from common.conexao_local import cursorConexao

class crawler_jurisprudencia_tjpr():
	"""Crawler especializado em retornar textos da jurisprudência de segunda instância do Paraná"""
	def __init__(self):
		crawler_jurisprudencia_tj.__init__(self)
		self.link_inicial = 'http://portal.tjpr.jus.br/jurisprudencia/'
		self.pesquisa_livre = 'pesquisaLivre'
		self.botao_pesquisar = '//*[@id="includeContent"]/table[2]/tbody/tr/td[2]/input'
		self.botao_proximo_iniXP = '//*[@id="navigator"]/div[1]/a[5]'
		self.botao_proximoXP = '//*[@id="navigator"]/div[1]/a[7]'
		self.tabela_colunas = 'justica_estadual.jurisprudencia_pr (ementas)'

	def download_tj(self):
		cursor = cursorConexao()
		driver = webdriver.Chrome(self.chromedriver)
		driver.get(self.link_inicial)
		driver.find_element_by_id(self.pesquisa_livre).send_keys('ementa')
		driver.find_element_by_xpath(self.botao_pesquisar).click()
		time.sleep(1)
		contador = 0		
		texto = crawler_jurisprudencia_tj.extrai_texto_html(self,(driver.page_source).replace('"',''))
		cursor.execute('INSERT INTO %s value ("%s");' % (self.tabela_colunas,texto))
		driver.find_element_by_xpath(self.botao_proximo_iniXP).click()
		time.sleep(1)
		texto = crawler_jurisprudencia_tj.extrai_texto_html(self,(driver.page_source).replace('"',''))
		cursor.execute('INSERT INTO %s value ("%s");' % (self.tabela_colunas,texto))
		self.botao_proximo_iniXP = '//*[@id="navigator"]/div[1]/a[6]'
		driver.find_element_by_xpath(self.botao_proximo_iniXP).click()
		loop_counter = 0
		while True:
			try:
				if (contador % 10000 == 0):
					print(contador)
				texto = crawler_jurisprudencia_tj.extrai_texto_html(self,(driver.page_source).replace('"',''))
				cursor.execute('INSERT INTO %s value ("%s");' % (self.tabela_colunas,texto))
				driver.find_element_by_xpath(self.botao_proximoXP).click()
				time.sleep(2)
				contador += 1
			except:
				if input('me ajude'):
					texto = crawler_jurisprudencia_tj.extrai_texto_html(self,(driver.page_source).replace('"',''))
					cursor.execute('INSERT INTO %s value ("%s");' % (self.tabela_colunas,texto))
					driver.find_element_by_xpath(self.botao_proximoXP).click()
		driver.close()

if __name__ == '__main__':
	c = crawler_jurisprudencia_tjpr()
	print('comecei ',c.__class__.__name__)
	try:
		c.download_tj()
	except Exception as e:
		print('finalizei com erro ',e)

# HÁ MUITO POUCOS LINKS!!!!