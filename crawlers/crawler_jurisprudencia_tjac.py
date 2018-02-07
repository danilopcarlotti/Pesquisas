import sys, re, os, time
from crawler_jurisprudencia_tj import crawler_jurisprudencia_tj
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from common.conexao_local import cursorConexao

class crawler_jurisprudencia_tjac(crawler_jurisprudencia_tj):
	"""Crawler especializado em retornar textos da jurisprudência de segunda instância do Acre"""
	def __init__(self):
		crawler_jurisprudencia_tj.__init__(self)
		self.link_inicial = 'http://esaj.tjac.jus.br/cjsg/resultadoCompleta.do'
		self.pesquisa_livre = '//*[@id="iddados.buscaInteiroTeor"]'
		self.data_julgamento_inicialXP = '//*[@id="dtJulgamentoInicio"]/input'
		self.data_julgamento_finalXP = '//*[@id="dtJulgamentoFim"]/input'
		self.botao_pesquisar = '//*[@id="pbSubmit"]'
		self.botao_proximo_ini = '//*[@id="paginacaoSuperior-A"]/table/tbody/tr[1]/td[2]/div/a[5]'
		self.botao_proximo = '//*[@id="paginacaoSuperior-A"]/table/tbody/tr[1]/td[2]/div/a[6]'
		self.tabela_colunas = 'justica_estadual.jurisprudencia_ac (ementas)'

	def download_tj(self, termo = 'a'):
		cursor = cursorConexao()
		driver = webdriver.Chrome(self.chromedriver)
		driver.get(self.link_inicial)
		driver.find_element_by_xpath(self.pesquisa_livre).send_keys(termo)
		driver.find_element_by_xpath(self.botao_pesquisar).click()
		texto = crawler_jurisprudencia_tj.extrai_texto_html(self,(driver.page_source)).replace('"','')
		cursor.execute('INSERT INTO %s value ("%s");' % (self.tabela_colunas,texto))
		driver.find_element_by_xpath(self.botao_proximo_ini).click()
		contador = 0
		while True:
			try:
				time.sleep(1)
				texto = crawler_jurisprudencia_tj.extrai_texto_html(self,(driver.page_source)).replace('"','')
				cursor.execute('INSERT INTO %s value ("%s");' % (self.tabela_colunas,texto))
				driver.find_element_by_xpath(self.botao_proximo).click()
				contador = 0
			except Exception as e:
				print(e)
				contador += 1
				time.sleep(5)
				if contador > 3:
					driver.close()
					break

def main():
	c = crawler_jurisprudencia_tjac()
	print('comecei ',c.__class__.__name__)
	try:
		c.download_tj()
	except Exception as e:
		print(e)

if __name__ == '__main__':
	main()