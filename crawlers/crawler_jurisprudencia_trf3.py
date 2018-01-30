import time, ssl
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from crawler_jurisprudencia_tj import crawler_jurisprudencia_tj
from common.conexao_local import cursorConexao

class crawler_jurisprudencia_trf3():
	"""Crawler especializado em retornar textos da jurisprudência de segunda instância de Maranhão"""
	def __init__(self):
		crawler_jurisprudencia_tj.__init__(self)
		ssl._create_default_https_context = ssl._create_unverified_context 
		self.link_inicial = 'http://web.trf3.jus.br/base-textual/Home/BuscaAcordaos/0'
		self.botao_pesquisar = '//*[@id="pesquisar"]'
		self.botao_prox = '//*[@id="navegacaoSuperior"]/a[%s]'
		self.botao_prox_ini = '4'
		self.botao_prox_outros = '6'
		self.link_primeiro_resultado = '//*[@id="blocoesquerdo"]/span[2]/a'
		self.link_resultado_xpath = '//*[@id="itemlistaresultados"]/span[3]/a'
		self.pesquisa_livre = '//*[@id="txtPesqLivre"]'
		self.tabela_colunas = 'justica_federal.jurisprudencia_trf3 (ementas)'

	def download_trf3(self, termo = 'recurso'):
		cursor = cursorConexao()
		driver = webdriver.Chrome(self.chromedriver)
		driver.get(self.link_inicial)
		time.sleep(1)
		driver.find_element_by_xpath(self.pesquisa_livre).send_keys(termo)
		driver.find_element_by_xpath(self.botao_pesquisar).click()
		time.sleep(1)
		driver.find_element_by_xpath(self.link_resultado_xpath).click()
		time.sleep(1)
		links_inteiro_teor = driver.find_elements_by_partial_link_text('')
		for l in links_inteiro_teor:
			try:
				if re.search(r'http\://www\.trf3\.jus\.br/trf3r/index\.php\?',l.get_attribute('href')):
					texto = l.get_attribute('href')
					cursor.execute('INSERT INTO %s value ("%s");' % (self.tabela_colunas,texto))		
					break
			except:
				pass
		driver.find_element_by_xpath(self.botao_prox % self.botao_prox_ini)
		contador = 0
		while True:
			try:
				time.sleep(2)
				links_inteiro_teor = driver.find_elements_by_partial_link_text('')
				for l in links_inteiro_teor:
					links_inteiro_teor = driver.find_elements_by_partial_link_text('')
					try:
						if re.search(r'http\://www\.trf3\.jus\.br/trf3r/index\.php\?',l.get_attribute('href')):
							texto = l.get_attribute('href')
							cursor.execute('INSERT INTO %s value ("%s");' % (self.tabela_colunas,texto))		
							break
					except:
						pass
				driver.find_element_by_xpath(self.botao_prox % self.botao_prox_outros)
			except Exception as e:
				print(e)
				time.sleep(5)
				if contador > 3:
					driver.close()
					break

if __name__ == '__main__':
	c = crawler_jurisprudencia_trf3()
	try:
		c.download_trf3()
	except Exception as e:
		print(e)