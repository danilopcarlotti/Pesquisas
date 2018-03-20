import sys, re, time, pyautogui
from bs4 import BeautifulSoup
from common.conexao_local import cursorConexao
from common_nlp.parse_texto import busca
from crawler_jurisprudencia_tj import crawler_jurisprudencia_tj
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
					cursor.execute('INSERT INTO %s value ("%s");' % (self.tabela_colunas,texto))
					pyautogui.hotkey('ctrl','w')
					driver.switch_to.window(driver.window_handles[0])
			except Exception as e:
				pass
		try: 
			driver.find_element_by_xpath(self.botao_proximo_iniXP).click()
		except:
			driver.close()
			return
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
							cursor.execute('INSERT INTO %s value ("%s");' % (self.tabela_colunas,texto))
							pyautogui.hotkey('ctrl','w')
							driver.switch_to.window(driver.window_handles[0])
					except Exception as e:
						pass
				driver.find_element_by_xpath(self.botao_proximoXP).click()
			except:
				driver.close()
				break

	def parser_acordaos(self, texto, cursor):
		numero = busca(r'[\d\.\-]{11,25}', texto, ngroup = 0)
		julgador = busca(r'\nRELATOR.*?\:(.*?)__', texto, args = re.DOTALL).replace('\n','')
		orgao_julgador = busca(r'Turma Julgadora da (.*?)\,', texto)
		data_disponibilizacao = busca(r'\d{2} de \w+ de \d{4}', texto, ngroup = 0)
		cursor.execute('INSERT INTO jurisprudencia_2_inst.jurisprudencia_2_inst (tribunal, numero, data_decisao, orgao_julgador, julgador, texto_decisao) values ("%s", "%s", "%s", "%s", "%s", "%s");' % ('pa', numero, data_disponibilizacao, orgao_julgador, julgador, texto))


if __name__ == '__main__':
	c = crawler_jurisprudencia_tjpa()
# 	print('comecei ',c.__class__.__name__)
# 	for a in c.lista_anos:
# 		try:
			
# 			for m in range(len(c.lista_meses)):
# 				for i in range(1,8):
# 					try:
# 						c.download_tj('0'+str(i)+'/'+c.lista_meses[m]+'/'+a,'0'+str(i+1)+'/'+c.lista_meses[m]+'/'+a)
# 					except Exception as e:
# 						print(e)		
# 				for i in range(10,27):
# 					try:
# 						c.download_tj(str(i)+'/'+c.lista_meses[m]+'/'+a,str(i+1)+'/'+c.lista_meses[m]+'/'+a)
# 					except Exception as e:
# 						print(e)
# 		except Exception as e:
# 			print(e)
	cursor = cursorConexao()
	cursor.execute('SELECT ementas from justica_estadual.jurisprudencia_pa limit 1000000')
	dados = cursor.fetchall()
	for dado in dados:
		c.parser_acordaos(dado[0], cursor)