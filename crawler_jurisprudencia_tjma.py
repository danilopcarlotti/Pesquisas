import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from crawler_jurisprudencia_tj import crawler_jurisprudencia_tj
from crawlerJus import crawlerJus

class crawler_jurisprudencia_tjma():
	"""Crawler especializado em retornar textos da jurisprudência de segunda instância de Maranhão"""
	def __init__(self):
		crawler_jurisprudencia_tj.__init__(self)
		self.link_inicial = 'http://jurisconsult.tjma.jus.br/'
		self.pesquisa_livre = '//*[@id="txtChaveJurisprudencia"]'
		self.data_julgamento_inicial = 'dtaInicio'
		self.data_julgamento_final = 'dtaTermino'
		self.botao_pesquisar = 'btnConsultar'

	def download_tj(self,termo, data_julg_ini, data_julg_fim):
		def download_texto(pagina):
			pag = BeautifulSoup(pagina,'lxml')
			for script in soup(["script", "style"]):
				script.extract()
			return soup.get_text()
		driver = webdriver.Chrome(self.chromedriver)
		driver.get(self.link_inicial)
		driver.find_element_by_xpath(self.pesquisa_livre).send_keys(termo)
		driver.find_element_by_name(self.data_julgamento_inicial).send_keys(data_julg_ini)
		driver.find_element_by_name(self.data_julgamento_final).send_keys(data_julg_fim)
		driver.find_elements_by_name(self.botao_pesquisar)[2].click()
		texto = download_texto(driver.page_source)
		# apertar botão de próximo e refazer


c = crawler_jurisprudencia_tjma()
c.download_tj('acordam','01/01/2014','10/10/2017')