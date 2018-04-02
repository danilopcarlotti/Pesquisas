import sys, re, time, urllib.request
from crawlerJus import crawlerJus
from bs4 import BeautifulSoup
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from common.conexao_local import cursorConexao

class crawler_jurisprudencia_tjrj(crawlerJus):
	"""Crawler especializado em retornar textos da jurisprudência de segunda instância do Rio de Janeiro"""
	def __init__(self):
		crawlerJus.__init__(self)
		self.botao_pesquisar = '//*[@id="ContentPlaceHolder1_btnPesquisar"]'
		self.botao_ano_inicial = '//*[@id="ContentPlaceHolder1_cmbAnoInicio"]'
		self.botao_ano_final = '//*[@id="ContentPlaceHolder1_cmbAnoFim"]'
		self.botao_proximo_iniXP = '//*[@id="placeholder"]/span/table/tbody/tr[7]/td/a'
		self.botao_proximo_XP = '//*[@id="placeholder"]/span/table/tbody/tr[7]/td/a[2]'
		self.link_inicial = 'http://www4.tjrj.jus.br/ejuris/ConsultarJurisprudencia.aspx'
		self.lista_anos = [str(i) for i in range(2011,date.today().year+1)]
		self.pesquisa_livre = '//*[@id="ContentPlaceHolder1_txtTextoPesq"]'
		self.tabela_colunas = 'justica_estadual.jurisprudencia_rj (ementas)'

	def download_tj(self,ano_inicial,ano_final):
		cursor = cursorConexao()
		driver = webdriver.Chrome(self.chromedriver)
		driver.get(self.link_inicial)
		driver.find_element_by_xpath(self.pesquisa_livre).send_keys('direito')
		driver.find_element_by_xpath(self.botao_ano_inicial).send_keys(ano_inicial)
		driver.find_element_by_xpath(self.botao_ano_final).send_keys(ano_final)
		driver.find_element_by_xpath(self.botao_pesquisar).click()
		time.sleep(20)
		contador = 0
		links_inteiro_teor = driver.find_elements_by_partial_link_text('')
		for link in links_inteiro_teor:
			try:
				if re.search(r'gedcacheweb',link.get_attribute('href')):
					self.baixa_html_pdf(link.get_attribute('href'),'acordao_rj_'+str(contador))
					contador += 1
			except Exception as e:
				print(e)
		driver.find_element_by_xpath(self.botao_proximo_iniXP).click()
		loop_counter = 0
		while True:
			try:
				time.sleep(4)
				links_inteiro_teor = driver.find_elements_by_partial_link_text('')
				for link in links_inteiro_teor:
					try:
						if re.search(r'gedcacheweb',link.get_attribute('href')):
							crawlerJus.baixa_html_pdf(link.get_attribute('href'),'acordao_rj_'+str(contador))
							contador += 1
					except:
						pass
				driver.find_element_by_xpath(self.botao_proximo_XP).click()
			except Exception as e:
				time.sleep(10)
				print(e)
				loop_counter += 1
				if loop_counter > 2:
					break
		driver.close()

	def parser_acordaos(self, texto, cursor, pdf_class):
		texto = pdf_class.convert_pdfminer(arquivo)
		numero = busca(r'\d{7}\-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}', texto)
		julgador = busca(r'\n\s*?RELATOR.*?\:(.*?)\n', texto)
		data_decisao = busca(r'\n\s*?Rio de Janeiro, (.*?)\.', texto)
		cursor.execute('INSERT INTO jurisprudencia_2_inst.jurisprudencia_2_inst (tribunal, numero, data_decisao, julgador, texto_decisao) values ("%s","%s","%s","%s","%s");' % ('rj',numero, data_decisao, julgador, texto))

if __name__ == '__main__':
	c = crawler_jurisprudencia_tjrj()
	print('comecei ',c.__class__.__name__)
	try:
		for l in c.lista_anos:
			print(l,'\n')
			c.download_tj(l,l)
	except Exception as e:
		print(e)
