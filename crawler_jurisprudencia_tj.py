from crawlerJus import crawlerJus
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from conexao_local import cursorConexao
from datetime import date
import time

class crawler_jurisprudencia_tj():
	"""Generic class with methods for crawler_jurisprudencia_tj's"""
	def __init__(self):
		crawlerJus.__init__(self)
		self.lista_anos = [str(i) for i in range(2011,date.today().year+1)]
		self.lista_meses = ['0'+str(i) for i in range(1,10)]
		self.lista_meses += ['10','11','12']

	def download_jurisprudencia(self,driver,pesquisa_livre,data_julg_iniXP,data_julg_ini,data_julg_fimXP,data_julg_fim,botao_pesquisar,termo):
		driver.find_element_by_xpath(pesquisa_livre).send_keys(termo)
		driver.find_element_by_xpath(data_julg_iniXP).send_keys(data_julg_ini)
		driver.find_element_by_xpath(data_julg_fimXP).send_keys(data_julg_fim)
		driver.find_element_by_xpath(botao_pesquisar).click()

	def extrai_texto_html(self,pagina):
		return crawlerJus.extrai_texto_html(self,pagina)

	def download_tj_ESAJ(self,superC,data_julg_ini,data_julg_fim,termo='acordam'):
		cursor = cursorConexao()
		driver = webdriver.Chrome(self.chromedriver)
		driver.get(self.link_inicial)
		superC.download_jurisprudencia(self,driver,self.pesquisa_livre,self.data_julgamento_inicialXP,data_julg_ini,self.data_julgamento_finalXP,data_julg_fim,self.botao_pesquisar,termo=termo)
		texto = crawlerJus.extrai_texto_html(self,(driver.page_source).replace('"',''))
		cursor.execute('INSERT INTO %s value ("%s");' % (self.tabela_colunas,texto))
		driver.find_element_by_xpath(self.botao_proximo_ini).click()
		texto = crawlerJus.extrai_texto_html(self,(driver.page_source).replace('"',''))
		cursor.execute('INSERT INTO %s value ("%s");' % (self.tabela_colunas,texto))
		contador = 0
		loop_counter = 0
		while True:
			time.sleep(2)
			try:
				contador += 1
				driver.find_element_by_xpath(self.botao_proximo).click()
				texto = crawlerJus.extrai_texto_html(self,(driver.page_source).replace('"',''))
				cursor.execute('INSERT INTO %s value ("%s");' % (self.tabela_colunas,texto))
			except:
				try:
					time.sleep(2)
					driver.find_element_by_xpath(self.botao_proximo).click()
					texto = crawlerJus.extrai_texto_html(self,(driver.page_source).replace('"',''))
					cursor.execute('INSERT INTO %s value ("%s");' % (self.tabela_colunas,texto))
				except:
					loop_counter += 1
					time.sleep(5)
					print(contador)
					if loop_counter > 3:
						break
		driver.close()

# create_statement_ESAJ = '''
# use justica_estadual;
# CREATE TABLE `jurisprudencia_am` (
#   `id` int(11) NOT NULL AUTO_INCREMENT,
#   `ementas` longtext,
#   PRIMARY KEY (`id`)
# ) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;
# '''