import sys, re, time
from crawler_jurisprudencia_tj import crawler_jurisprudencia_tj
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from common.conexao_local import cursorConexao

class crawler_jurisprudencia_tjpa():
	"""Crawler especializado em retornar textos da jurisprudência de segunda instância do Pará"""
	def __init__(self):
		crawler_jurisprudencia_tj.__init__(self)
		self.link_inicial = 'http://gsa-index.tjpa.jus.br/consultas/search?q=&client=consultas&proxystylesheet=consultas&site=jurisprudencia&sort=date%3AD%3AS%3Ad1&aba=JP'
		self.pesquisa_livre = '//*[@id="advancedForm"]/div[1]/div[1]/div/input'
		self.botao_mostrar_pesquisa_avancada = '//*[@id="show_search_advanced"]'
		self.botao_pesquisar_avancado = '//*[@id="advancedForm"]/div[1]/div[1]/div/span/button'
		self.botao_proximo_iniXP = '//*[@id="resultados"]/div/div[1]/div[2]/div/span[1]/a'
		self.botao_proximoXP = '//*[@id="resultados"]/div/div[1]/div[2]/div/span[3]/a'
		self.data_julgamento_inicialXP = '//*[@id="julg_dataIni"]'
		self.data_julgamento_finalXP = '//*[@id="julg_dataFim"]'
		self.tabela_colunas = 'justica_estadual.jurisprudencia_pa (ementas)'

	def download_tj(self,data_ini,data_fim):
		cursor = cursorConexao()
		driver = webdriver.Chrome(self.chromedriver)
		driver.get(self.link_inicial)
		driver.find_element_by_xpath(self.pesquisa_livre).send_keys('a')
		driver.find_element_by_xpath(self.botao_mostrar_pesquisa_avancada).click()
		driver.find_element_by_xpath(self.data_julgamento_inicialXP).send_keys(data_ini)
		driver.find_element_by_xpath(self.data_julgamento_finalXP).send_keys(data_fim)
		driver.find_element_by_xpath(self.botao_pesquisar_avancado).click()
		links = driver.find_elements_by_partial_link_text('')
		for l in links:
			try:
				if re.search(r'\?q\=cache\:',l.get_attribute('href')):
					l.click()
					driver.switch_to.window(driver.window_handles[-1])
					texto = crawler_jurisprudencia_tj.extrai_texto_html(self,(driver.page_source).replace('"',''))
					print(texto)
					cursor.execute('INSERT INTO %s value ("%s");' % (self.tabela_colunas,texto))
					driver.switch_to.window(driver.window_handles[0])
			except Exception as e:
				print(e)
		driver.find_element_by_xpath(self.botao_proximo_iniXP).click()
		loop_counter = 0
		while True:
			try:
				time.sleep(2)
				links = driver.find_elements_by_partial_link_text('')
				for l in links:
					try:
						if re.search(r'\?q\=cache\:',l.get_attribute('href')):
							l.click()
							driver.switch_to.window(driver.window_handles[-1])
							texto = crawler_jurisprudencia_tj.extrai_texto_html(self,(driver.page_source).replace('"',''))
							print(texto)
							cursor.execute('INSERT INTO %s value ("%s");' % (self.tabela_colunas,texto))
							driver.switch_to.window(driver.window_handles[0])
					except Exception as e:
						print(e)
				driver.find_element_by_xpath(self.botao_proximoXP).click()
			except:
				loop_counter += 1
				time.sleep(5)
				if loop_counter > 3:
					if input('me ajude'):
						break
		driver.close()

if __name__ == '__main__':
	c = crawler_jurisprudencia_tjpa()
	print('comecei ',c.__class__.__name__)
	try:
		for a in c.lista_anos:
			for m in range(len(c.lista_meses)):
				c.download_tj('01/'+c.lista_meses[m]+'/'+a,'14/'+c.lista_meses[m]+'/'+a)
				c.download_tj('15/'+c.lista_meses[m]+'/'+a,'28/'+c.lista_meses[m]+'/'+a)
	except Exception as e:
		print('finalizei com erro ',e)