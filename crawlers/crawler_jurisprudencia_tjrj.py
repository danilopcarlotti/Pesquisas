import sys, re, time
from crawler_jurisprudencia_tj import crawler_jurisprudencia_tj
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from common.conexao_local import cursorConexao

class crawler_jurisprudencia_tjrj():
	"""Crawler especializado em retornar textos da jurisprudência de segunda instância do Rio de Janeiro"""
	def __init__(self):
		crawler_jurisprudencia_tj.__init__(self)
		self.link_inicial = 'http://www4.tjrj.jus.br/ejuris/ConsultarJurisprudencia.aspx'
		self.pesquisa_livre = '//*[@id="ContentPlaceHolder1_txtTextoPesq"]'
		self.botao_pesquisar = '//*[@id="ContentPlaceHolder1_btnPesquisar"]'
		self.botao_ano_inicial = '//*[@id="ContentPlaceHolder1_cmbAnoInicio"]'
		self.botao_proximo_iniXP = '//*[@id="placeholder"]/span/table/tbody/tr[7]/td/a'
		self.botao_proximo_XP = '//*[@id="placeholder"]/span/table/tbody/tr[7]/td/a[2]'
		self.tabela_colunas = 'justica_estadual.jurisprudencia_tjrj (ementas)'

	def download_tj(self):
		cursor = cursorConexao()
		driver = webdriver.Chrome(self.chromedriver)
		driver.get(self.link_inicial)
		driver.find_element_by_xpath(self.pesquisa_livre).send_keys('direito')
		driver.find_element_by_xpath(self.botao_ano_inicial).send_keys('2011')
		driver.find_element_by_xpath(self.botao_pesquisar).click()
		time.sleep(4)
		links_inteiro_teor = driver.find_elements_by_partial_link_text('')
		for link in links_inteiro_teor:
			try:
				if re.search(r'gedcacheweb',link.get_attribute('href')):
					cursor.execute('INSERT INTO %s value ("%s");' % (self.tabela_colunas,link.get_attribute('href')))
			except:
				pass
		driver.find_element_by_xpath(self.botao_proximo_iniXP).click()
		loop_counter = 0
		while True:
			try:
				time.sleep(4)
				links_inteiro_teor = driver.find_elements_by_partial_link_text('')
				for link in links_inteiro_teor:
					try:
						if re.search(r'gedcacheweb',link.get_attribute('href')):
							cursor.execute('INSERT INTO %s value ("%s");' % (self.tabela_colunas,link.get_attribute('href')))
					except:
						pass
				driver.find_element_by_xpath(self.botao_proximo_XP).click()
			except Exception as e:
				print(e)
				loop_counter += 1
				if loop_counter > 2:
					break
		driver.close()

if __name__ == '__main__':
	c = crawler_jurisprudencia_tjrj()
	print('comecei ',c.__class__.__name__)
	try:
		c.download_tj()
	except Exception as e:
		print(e)
