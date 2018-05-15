import time, re
from bs4 import BeautifulSoup
from common.conexao_local import cursorConexao
from common_nlp.parse_texto import busca
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from crawler_jurisprudencia_tj import crawler_jurisprudencia_tj
from common.conexao_local import cursorConexao


class crawler_jurisprudencia_trt02():
	"""Crawler especializado em retornar textos da jurisprudência de segunda instância de Maranhão"""
	def __init__(self):
		crawler_jurisprudencia_tj.__init__(self)
		self.link_inicial = 'http://search.trtsp.jus.br/EasySearchFrontEnd/AcordaosUnificados.jsp'
		self.botao_pesquisar = '//*[@id="acordaoForm"]/table/tbody/tr/td[2]/input'
		self.botao_prox = '//*[@id="next"]'
		self.data_iniXP = '//*[@id="dataPublicacaoDe"]'
		self.data_fimXP = '//*[@id="dataPublicacaoAte"]'
		self.pesquisa_livre = '//*[@id="acordaoForm"]/table/tbody/tr/td[1]/input'

	def download_tj(self, data_inicial = '', data_final = '', termo='a'):
		cursor = cursorConexao()
		driver = webdriver.Chrome(self.chromedriver)
		driver.get(self.link_inicial)
		driver.find_element_by_xpath(self.pesquisa_livre).send_keys(termo)
		driver.find_element_by_xpath(self.data_iniXP).send_keys(data_inicial)
		driver.find_element_by_xpath(self.data_fimXP).send_keys(data_final)
		time.sleep(2)
		driver.find_element_by_xpath(self.botao_pesquisar).click()
		contador = 0
		while True:
			try:
				time.sleep(2)
				
				texto = crawler_jurisprudencia_tj.extrai_texto_html(self,driver.page_source)
				print(texto)
				break
				# cursor.execute('INSERT INTO justica_federal.jurisprudencia_trf1 (ementas) value("%s")' % texto.replace('"',''))
				contador = 0
			except Exception as e:
				print(e)
				time.sleep(3)
				contador += 1
				if contador > 3:
					driver.close()
					break

def main():
	c = crawler_jurisprudencia_trt02()
	c.download_tj()

if __name__ == '__main__':
	main()