import sys, re, time, common.download_path, os
from crawler_jurisprudencia_tj import crawler_jurisprudencia_tj
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from common.conexao_local import cursorConexao

class crawler_jurisprudencia_tjmg():
	"""Crawler especializado em retornar textos da jurisprudência de segunda instância de Minas Gerais"""
	def __init__(self):
		crawler_jurisprudencia_tj.__init__(self)
		self.link_inicial = 'http://www5.tjmg.jus.br/jurisprudencia/formEspelhoAcordao.do'
		self.pesquisa_livre = '//*[@id="palavras"]'
		self.inteiro_teor = '//*[@id="pesqAcordao"]'
		self.botao_pesquisar = '//*[@id="pesquisaLivre"]'
		self.link_captcha = '//*[@id="captcha_text"]'
		self.data_julgamento_inicialXP = '//*[@id="dataJulgamentoInicial"]'
		self.data_julgamento_finalXP = '//*[@id="dataJulgamentoFinal"]'
		self.botao_proximo_XP = '//*[@id="textoUmaColuna"]/table[1]/tbody/tr[4]/td/table/tbody/tr/td[5]/a'
		self.link_download_captcha = '/html/body/table/tbody/tr[3]/td/table/tbody/tr[4]/td/a[2]' 
		self.tabela_colunas = 'justica_estadual.jurisprudencia_mg (ementas)'

	def download_tj(self,data_ini,data_fim):
		crawler_jurisprudencia_tj.delete_audios(self)
		cursor = cursorConexao()
		driver = webdriver.Chrome(self.chromedriver)
		driver.get(self.link_inicial)
		driver.find_element_by_xpath(self.pesquisa_livre).send_keys('direito')
		driver.find_element_by_xpath(self.data_julgamento_inicialXP).send_keys(data_ini)
		driver.find_element_by_xpath(self.data_julgamento_finalXP).send_keys(data_fim)
		driver.find_element_by_xpath(self.botao_pesquisar).click()
		time.sleep(5)
		driver.find_element_by_xpath(self.link_download_captcha).click()
		time.sleep(5)
		driver.find_element_by_xpath(self.link_captcha).send_keys(crawler_jurisprudencia_tj.captcha(self))
		crawler_jurisprudencia_tj.delete_audios(self)
		while True:
			try:
				time.sleep(2)
				driver.find_element_by_class_name('linkListaEspelhoAcordaos').click()
				texto = crawler_jurisprudencia_tj.extrai_texto_html(self,(driver.page_source).replace('"',''))
				cursor.execute('INSERT INTO %s value ("%s");' % (self.tabela_colunas,texto))
				driver.find_element_by_xpath(self.botao_proximo_XP).click()
			except Exception as e:
				print(e)
				try:
					driver.find_element_by_xpath(self.link_download_captcha).click()
					time.sleep(5)
					driver.find_element_by_xpath(self.link_captcha).send_keys(crawler_jurisprudencia_tj.captcha(self))
					crawler_jurisprudencia_tj.delete_audios(self)
					time.sleep(5)
				except:
					driver.close()
					return	
		driver.close()

if __name__ == '__main__':
	c = crawler_jurisprudencia_tjmg()
	print('comecei ',c.__class__.__name__)
	try:
		for a in c.lista_anos:
			for m in range(3,len(c.lista_meses)):
				c.download_tj('01'+c.lista_meses[m]+a,'14'+c.lista_meses[m]+a)
				c.download_tj('15'+c.lista_meses[m]+a,'28'+c.lista_meses[m]+a)
	except Exception as e:
		print('finalizei com erro ',e)