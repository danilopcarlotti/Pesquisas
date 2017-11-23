import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from crawler_jurisprudencia_tj import crawler_jurisprudencia_tj
from conexao_local import cursorConexao

class crawler_jurisprudencia_tjma():
	"""Crawler especializado em retornar textos da jurisprudência de segunda instância de Maranhão"""
	def __init__(self):
		crawler_jurisprudencia_tj.__init__(self)
		self.link_inicial = 'http://jurisconsult.tjma.jus.br/'
		self.pesquisa_livre = '//*[@id="txtChaveJurisprudencia"]'
		self.data_julgamento_inicial = 'dtaInicio'
		self.data_julgamento_final = 'dtaTermino'
		self.botao_pesquisar = 'btnConsultar'

	def download_tj(self, data_julg_ini, data_julg_fim, termo = 'acordam'):
		cursor = cursorConexao()
		driver = webdriver.Chrome(self.chromedriver)
		driver.get(self.link_inicial)
		driver.find_element_by_xpath(self.pesquisa_livre).send_keys(termo)
		driver.find_element_by_name(self.data_julgamento_inicial).send_keys(data_julg_ini)
		driver.find_element_by_name(self.data_julgamento_final).send_keys(data_julg_fim)
		driver.find_elements_by_name(self.botao_pesquisar)[2].click()
		texto = crawler_jurisprudencia_tj.extrai_texto_html(self,driver.page_source)
		while True:
			try:
				time.sleep(2)
				driver.find_element_by_xpath('//*[@id="pagination"]/ul/li[13]').click()
				texto = crawler_jurisprudencia_tj.extrai_texto_html(self,driver.page_source)
				cursor.execute('INSERT INTO justica_estadual.jurisprudencia_tjma (textos_brutos) value("%s")' % texto.replace('"',''))
			except:
				time.sleep(3)
				try:
					driver.find_element_by_xpath('//*[@id="pagination"]/ul/li[13]').click()
					texto = crawler_jurisprudencia_tj.extrai_texto_html(self,driver.page_source)
					cursor.execute('INSERT INTO justica_estadual.jurisprudencia_tjma (textos_brutos) value("%s")' % texto.replace('"',''))
				except:
					break

if __name__ == '__main__':
	c = crawler_jurisprudencia_tjma()
	c.download_tj('01/01/2011','10/10/2017')