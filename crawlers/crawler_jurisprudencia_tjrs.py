import sys, re, time
from crawler_jurisprudencia_tj import crawler_jurisprudencia_tj
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from common.conexao_local import cursorConexao

class crawler_jurisprudencia_tjrs():
	"""Crawler especializado em retornar textos da jurisprudência de segunda instância do Rio Grande do Sul"""
	def __init__(self):
		crawler_jurisprudencia_tj.__init__(self)
		self.link_inicial = 'http://www.tjrs.jus.br/busca/?tb=jurisnova&partialfields=tribunal%3ATribunal%2520de%2520Justi%25C3%25A7a%2520do%2520RS.(TipoDecisao%3Aac%25C3%25B3rd%25C3%25A3o|TipoDecisao%3Amonocr%25C3%25A1tica|TipoDecisao:null)&t=s&pesq=ementario.#main_res_juris'
		self.pesquisa_livre = '//*[@id="q"]'
		self.botao_pesquisar = '//*[@id="conteudo"]/form/div[1]/div/div/input'
		self.botao_proximo_iniXP = '//*[@id="main_res_juris"]/div/div[2]/span[1]/a'
		self.botao_proximoXP = '//*[@id="main_res_juris"]/div/div[2]/span[3]/a'
		self.tabela_colunas = 'justica_estadual.jurisprudencia_rs (ementas)'

	def download_tj(self):
		cursor = cursorConexao()
		driver = webdriver.Chrome(self.chromedriver)
		driver.get(self.link_inicial)
		driver.find_element_by_xpath(self.pesquisa_livre).send_keys('a')
		driver.find_element_by_xpath(self.botao_pesquisar).click()
		links_inteiro_teor = driver.find_elements_by_link_text('html')
		for l in links_inteiro_teor:
			try:
				texto = crawler_jurisprudencia_tj.extrai_texto_html(self,(l.get_attribute('href')).replace('"',''))
				cursor.execute('INSERT INTO %s value ("%s");' % (self.tabela_colunas,texto))		
			except:
				pass
		driver.find_element_by_xpath(self.botao_proximo_iniXP).click()
		loop_counter = 0
		while True:
			try:
				time.sleep(1)
				for l in links_inteiro_teor:
					try:
						texto = crawler_jurisprudencia_tj.extrai_texto_html(self,(l.get_attribute('href')).replace('"',''))
						cursor.execute('INSERT INTO %s value ("%s");' % (self.tabela_colunas,texto))		
					except:
						pass
				driver.find_element_by_xpath(self.botao_proximoXP).click()
			except:
				loop_counter += 1
				time.sleep(5)
				if loop_counter > 3:
					if input('me ajude'):
						break
		driver.close()

if __name__ == '__main__':
	c = crawler_jurisprudencia_tjrs()
	print('comecei ',c.__class__.__name__)
	try:
		c.download_tj()
	except Exception as e:
		print('finalizei com erro ',e)

		

