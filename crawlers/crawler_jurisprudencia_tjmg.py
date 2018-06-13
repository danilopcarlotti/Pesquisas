import sys, re, time, common.download_path, os
from bs4 import BeautifulSoup
from common.conexao_local import cursorConexao
from common_nlp.parse_texto import busca
from crawler_jurisprudencia_tj import crawler_jurisprudencia_tj
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

	def download_tj(self,data_ini,data_fim, termo='direito'):
		crawler_jurisprudencia_tj.delete_audios(self)
		cursor = cursorConexao()
		driver = webdriver.Chrome(self.chromedriver)
		driver.get(self.link_inicial)
		driver.find_element_by_xpath(self.pesquisa_livre).send_keys(termo)
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

	def parser_acordaos(self,texto, cursor):
		numero = busca(r'\d{7}\-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}', texto,ngroup=0)
		julgador = busca(r'\n\s*?Relator.*?\:\n\s*?(.*?)', texto)
		orgao_julgador = busca(r'\n\s*?.rgão julgador.*?\n\s*?(.*?)/', texto)
		origem = busca(r'\nComarca de Origem\n(.+)', texto)
		data_disponibilizacao = busca(r'\n\s*?Data d[oe] julgamento\:\n\s*?\n\s*?(\d{2}/\d{2}/\d{4})', texto)
		cursor.execute('INSERT INTO jurisprudencia_2_inst.jurisprudencia_2_inst (tribunal, numero, origem, data_decisao, orgao_julgador, julgador, texto_decisao) values ("%s","%s","%s","%s","%s","%s","%s");' % ('mg',numero, origem, data_disponibilizacao, orgao_julgador, julgador, texto))

if __name__ == '__main__':
	c = crawler_jurisprudencia_tjmg()
	# print('comecei ',c.__class__.__name__)
	# try:
	# 	for a in c.lista_anos:
	# 		for m in range(3,len(c.lista_meses)):
	# 			c.download_tj('01'+c.lista_meses[m]+a,'14'+c.lista_meses[m]+a)
	# 			c.download_tj('15'+c.lista_meses[m]+a,'28'+c.lista_meses[m]+a)
	# except Exception as e:
	# 	print('finalizei com erro ',e)

	cursor = cursorConexao()
	cursor.execute('SELECT ementas from justica_estadual.jurisprudencia_mg limit 1000000')
	dados = cursor.fetchall()
	for dado in dados:
		c.parser_acordaos(dado[0], cursor)