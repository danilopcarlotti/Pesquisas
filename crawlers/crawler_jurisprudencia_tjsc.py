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
		self.tabela_colunas = 'justica_estadual.jurisprudencia_sc (ementas)'
		self.botao_proximo_iniXP = '//*[@id="paginacao"]/ul/li[7]/a'
		self.botao_proximoXP = '//*[@id="paginacao"]/ul/li[%s]/a'
		self.data_inicialXP = '//*[@id="dtini"]'
		self.data_finalXP = '//*[@id="dtfim"]'

	def download_tj(self,data_ini,data_fim):
		cursor = cursorConexao()
		driver = webdriver.Chrome(self.chromedriver)
		driver.get(self.link_inicial)
		driver.find_element_by_xpath(self.pesquisa_livre).send_keys('processo')
		driver.find_element_by_xpath(self.data_inicialXP).send_keys(data_ini)
		driver.find_element_by_xpath('//*[@id="busca_avancada"]/table[1]/tbody/tr/td[1]/span[1]').click()
		driver.find_element_by_xpath(self.data_finalXP).send_keys(data_fim)
		driver.find_element_by_xpath('//*[@id="busca_avancada"]/table[1]/tbody/tr/td[1]/span[1]').click()
		time.sleep(1)
		driver.find_element_by_xpath(self.botao_pesquisar).click()
		time.sleep(1)
		links_inteiro_teor = driver.find_elements_by_partial_link_text('')
		for l in links_inteiro_teor:
			try:
				if re.search(r'html\.do',l.get_attribute('href')):
					texto = l.get_attribute('href')
					cursor.execute('INSERT INTO %s value ("%s");' % (self.tabela_colunas,texto))	
			except:
				pass
		try:
			driver.find_element_by_xpath(self.botao_proximo_iniXP).click()
		except:
			driver.close()
			return
		loop_counter = 0
		while True:
			try:
				time.sleep(1)
				links_inteiro_teor = driver.find_elements_by_partial_link_text('')
				for l in links_inteiro_teor:
					try:
						if re.search(r'html\.do',l.get_attribute('href')):
							texto = l.get_attribute('href')
							cursor.execute('INSERT INTO %s value ("%s");' % (self.tabela_colunas,texto))
					except:
						pass
				try:
					driver.find_element_by_xpath(self.botao_proximoXP % '9').click()
				except:
					try:
						driver.find_element_by_xpath(self.botao_proximoXP % '8').click()
					except:
						driver.find_element_by_xpath(self.botao_proximoXP % '7').click()
			except Exception as e:
				driver.close()
				return
		driver.close()

if __name__ == '__main__':
	c = crawler_jurisprudencia_tjsc()
	print('comecei ',c.__class__.__name__)
	for a in c.lista_anos:
		print(a)
		for m in range(len(c.lista_meses)):
			try:
				c.download_tj('01/'+c.lista_meses[m]+'/'+a,'14/'+c.lista_meses[m]+'/'+a)
			except Exception as e:
				print(e,c.lista_meses[m])
			try:
				c.download_tj('15/'+c.lista_meses[m]+'/'+a,'28/'+c.lista_meses[m]+'/'+a)
			except Exception as e:
				print(e,c.lista_meses[m])