import sys, re, time
from crawler_jurisprudencia_tj import crawler_jurisprudencia_tj
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from common.conexao_local import cursorConexao

class crawler_jurisprudencia_tjrn():
	"""Crawler especializado em retornar textos da jurisprudência de segunda instância de Rio Grande do Norte"""
	def __init__(self):
		crawler_jurisprudencia_tj.__init__(self)
		self.link_inicial = 'http://esaj.tjrn.jus.br/cjosg/'
		self.pesquisa_livre = '/html/body/table[4]/tbody/tr/td/table[2]/tbody/tr[1]/td/div/form/table/tbody/tr/td/table/tbody/tr[1]/td[3]/input'
		self.data_julgamento_inicialXP = '/html/body/table[4]/tbody/tr/td/table[2]/tbody/tr[1]/td/div/form/table/tbody/tr/td/table/tbody/tr[7]/td[3]/table/tbody/tr/td[1]/input'
		self.data_julgamento_finalXP = '/html/body/table[4]/tbody/tr/td/table[2]/tbody/tr[1]/td/div/form/table/tbody/tr/td/table/tbody/tr[7]/td[3]/table/tbody/tr/td[3]/input'
		self.botao_pesquisar = '/html/body/table[4]/tbody/tr/td/table[2]/tbody/tr[1]/td/div/form/table/tbody/tr/td/table/tbody/tr[9]/td[3]/input[1]'
		self.botao_proximo = '/html/body/table[4]/tbody/tr/td/table/tbody/tr/td/table[1]/tbody/tr/td/input[2]'
		self.tabela_colunas = 'justica_estadual.jurisprudencia_rn (ementas)'

	def download_tj(self,data_ini,data_fim):
		cursor = cursorConexao()
		driver = webdriver.Chrome(self.chromedriver)
		driver.get(self.link_inicial)
		driver.find_element_by_xpath(self.pesquisa_livre).send_keys('ementa')
		driver.find_element_by_xpath(self.data_julgamento_inicialXP).send_keys(data_ini)
		driver.find_element_by_xpath(self.data_julgamento_finalXP).send_keys(data_fim)
		driver.find_element_by_xpath(self.botao_pesquisar).click()
		time.sleep(4)
		links_inteiro_teor = driver.find_elements_by_partial_link_text('')
		for link in links_inteiro_teor:
			try:
				if re.search(r'pcjoDecisao.jsp\?',link.get_attribute('href')):
					link.click()
					driver.switch_to.window(driver.window_handles[1])
					break
			except:
				pass
		texto = crawler_jurisprudencia_tj.extrai_texto_html(self,(driver.page_source)).replace('"','')
		cursor.execute('INSERT INTO %s value ("%s");' % (self.tabela_colunas,texto))
		ult_pag = driver.current_url
		driver.find_element_by_xpath(self.botao_proximo).click()
		loop_counter = 0
		while True:
			try:
				if ult_pag == driver.current_url:
					break
				time.sleep(2)
				texto = crawler_jurisprudencia_tj.extrai_texto_html(self,(driver.page_source)).replace('"','')
				cursor.execute('INSERT INTO %s value ("%s");' % (self.tabela_colunas,texto))
				ult_pag = driver.current_url
				driver.find_element_by_xpath(self.botao_proximo).click()
			except Exception as e:
				print(e)
				loop_counter += 1
				if loop_counter > 2:
					driver.close()
					break
		driver.close()


if __name__ == '__main__':
	c = crawler_jurisprudencia_tjrn()
	print('comecei ',c.__class__.__name__)
	try:
		for l in range(len(c.lista_anos)):
			print(c.lista_anos[l],'\n')
			for m in range(len(c.lista_meses)):
				try:
					c.download_tj('01'+c.lista_meses[m]+c.lista_anos[l],'28'+c.lista_meses[m]+c.lista_anos[l])
				except Exception as e:
					print(e)
	except Exception as e:
		print('finalizei o ano com erro ',e)