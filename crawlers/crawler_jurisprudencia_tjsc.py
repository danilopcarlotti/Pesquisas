import sys, re, time
from crawler_jurisprudencia_tj import crawler_jurisprudencia_tj
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from common.conexao_local import cursorConexao

class crawler_jurisprudencia_tjsc():
	"""Crawler especializado em retornar textos da jurisprudência de segunda instância de Santa Catarina"""
	def __init__(self):
		crawler_jurisprudencia_tj.__init__(self)
		self.link_inicial = 'http://busca.tjsc.jus.br/jurisprudencia/buscaForm.do'
		self.pesquisa_livre = '//*[@id="q"]'
		self.inteiro_teor = '//*[@id="busca_avancada"]/table[1]/tbody/tr/td[2]/span[1]]'
		self.botao_pesquisar = '//*[@id="busca_avancada"]/input[2]'
		self.tabela_colunas = 'justica_estadual.jurisprudencia_rs (ementas)'
		self.botao_proximo_iniXP = '//*[@id="paginacao"]/ul/li[7]/a'
		self.botao_proximoXP = '//*[@id="paginacao"]/ul/li[8]/a'

	def download_tj(self):
		cursor = cursorConexao()
		driver = webdriver.Chrome(self.chromedriver)
		driver.get(self.link_inicial)
		driver.find_element_by_xpath(self.pesquisa_livre).send_keys('processo')
		driver.find_element_by_xpath(self.botao_pesquisar).click()
		time.sleep(1)
		links_inteiro_teor = driver.find_elements_by_partial_link_text('')
		for l in links_inteiro_teor:
			try:
				if re.search(r'html\.do',l.get_attribute('href')):
					texto = crawler_jurisprudencia_tj.extrai_texto_html(self,(l.get_attribute('href')).replace('"',''))
					cursor.execute('INSERT INTO %s value ("%s");' % (self.tabela_colunas,texto))	
			except:
				pass
		driver.find_element_by_xpath(self.botao_proximo_iniXP).click()
		loop_counter = 0
		while True:
			try:
				time.sleep(1)
				links_inteiro_teor = driver.find_elements_by_partial_link_text('')
				for l in links_inteiro_teor:
					try:
						if re.search(r'html\.do',l.get_attribute('href')):
							texto = crawler_jurisprudencia_tj.extrai_texto_html(self,(l.get_attribute('href')).replace('"',''))
							cursor.execute('INSERT INTO %s value ("%s");' % (self.tabela_colunas,texto))	
					except:
						pass
				driver.find_element_by_xpath(self.botao_proximoXP).click()
			except:
				loop_counter += 1
				time.sleep(5)
				if loop_counter > 3:
					if input('me ajude'):
						break
		driver.close()

if __name__ == '__main__':
	c = crawler_jurisprudencia_tjsc()
	print('comecei ',c.__class__.__name__)
	try:
		c.download_tj()
	except Exception as e:
		print('finalizei com erro ',e)

		