import time, re, sys, os
from bs4 import BeautifulSoup
from common.conexao_local import cursorConexao
from common.download_path_diarios import path as path_diarios
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from crawler_jurisprudencia_tj import crawler_jurisprudencia_tj

sys.path.append(os.path.dirname(os.getcwd()))
from common_nlp.parse_texto import busca

class crawler_jurisprudencia_trf1(crawler_jurisprudencia_tj):
	"""Crawler especializado em retornar textos da jurisprudência de segunda instância de Maranhão"""
	def __init__(self):
		crawler_jurisprudencia_tj.__init__(self)
		self.link_inicial = 'http://www.cjf.jus.br/juris/trf1/index.jsp'
		self.pesquisa_livre = '//*[@id="td_00001"]'
		self.tipo_acordao = '//*[@id="label13"]'
		self.link_acordaos = '//*[@id="td_0005"]'
		self.botao_pesquisar = 'btnConsultar'
		self.botao_prox = '//*[@id="conteudo"]/div[1]/input[3]'

	def download_diarios_retroativo_2015(self):
		link_basico = 'https://portal.trf1.jus.br/dspace/handle/123/'
		link_basico_links = 'https://portal.trf1.jus.br/dspace/handle/123/163457?offset='
		for i in range(220,1360,20):
			links_paginas = []
			self.encontrar_links_html(link_basico_links+str(i), links_paginas, r'dspace/handle/123/\d{2,}$')
			counter = i
			for l in links_paginas:
				try:
					lista_links = []
					self.encontrar_links_html('https://portal.trf1.jus.br'+l, lista_links, r'pdf')
					self.baixa_html_pdf('https://portal.trf1.jus.br'+lista_links[0],'/mnt/Dados/Diarios_trf1/trf1_'+str(counter))
					counter += 1
					time.sleep(20)
				except:
					time.sleep(60)
		# print(lista_links)
	
	def download_diarios_retroativo_2020(self):
		dic_pag_diarios_ano = {
			'2016':224,
			'2017':232,
			'2018':236,
			'2019':238,
			'2020':163 #Setembro de 2020
		}
		for ano in ['2016','2017','2018','2019','2020']:
			for n_page in range(1,dic_pag_diarios_ano[ano]):
				link_basico = 'https://edj.trf1.jus.br/edj/handle/123/3/discover?rpp=17&etal=0&group_by=none&page={}&sort_by=dc.date.issued_dt&order=desc&filtertype_0=dateIssued&filtertype_1=dateIssued&filter_relational_operator_1=contains&filter_relational_operator_0=equals&filter_1=&filter_0={}'.format(n_page, ano)
				lista_links = []
				self.encontrar_links_html(link_basico, lista_links, r'edj/handle/\d+/\d{2,}')
				for l in lista_links:
					lista_pdf = []
					self.encontrar_links_html('https://edj.trf1.jus.br'+l, lista_pdf, r'\.pdf\?')
					try:
						print(lista_pdf[0])
						self.baixa_html_pdf('https://edj.trf1.jus.br'+lista_pdf[0],path_diarios+'/Diarios_trf1/dir_008/'+re.search(r'/Caderno\_(.*?)\?',lista_pdf[0]).group(1))
					except:
						pass
					time.sleep(1)

	def download_tj(self, termo = 'a'):
		cursor = cursorConexao()
		driver = webdriver.Chrome(self.chromedriver)
		driver.get(self.link_inicial)
		driver.find_element_by_xpath(self.pesquisa_livre).send_keys(termo)
		driver.find_element_by_xpath(self.tipo_acordao).click()
		driver.find_element_by_xpath(self.botao_pesquisar).click()
		time.sleep(2)
		driver.find_element_by_xpath(self.link_acordaos).click()
		contador = 0
		while True:
			try:
				time.sleep(2)
				texto = crawler_jurisprudencia_tj.extrai_texto_html(self,driver.page_source)
				cursor.execute('INSERT INTO justica_federal.jurisprudencia_trf1 (ementas) value("%s")' % texto.replace('"',''))
			except Exception as e:
				print(e)
				time.sleep(3)
				if contador > 8:
					driver.close()

	def parser_acordaos(self,texto, cursor):
		decisoes = re.split(r'\nDocumento\s*?\d+\s*?\-',texto)
		for d in range(1,len(decisoes)):
			numero = busca(r'\d{7}\-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}', decisoes[d],ngroup=0)
			julgador = busca(r'\n\s*?Relator.*?\n\n(.*?)\n', decisoes[d])
			orgao_julgador = busca(r'\nÓrgão julgador\n\n(.+)\n', decisoes[d])
			data_disponibilizacao = busca(r'\n\s*?Data da decisão\n\n(\d{6,10})', decisoes[d])
			cursor.execute('INSERT INTO jurisprudencia_2_inst.jurisprudencia_2_inst (tribunal, numero, data_decisao, orgao_julgador, julgador, texto_decisao) values ("%s","%s","%s","%s","%s","%s");' % ('trf1',numero, data_disponibilizacao, orgao_julgador, julgador, decisoes[d]))

if __name__ == '__main__':
	c = crawler_jurisprudencia_trf1()
	# try:
	# 	c.download_tj()
	# except Exception as e:
	# 	print(e)
	
	# c.download_diarios_retroativo_2015()
	c.download_diarios_retroativo_2020()

	# cursor = cursorConexao()
	# cursor.execute('SELECT ementas from justica_federal.jurisprudencia_trf1;')
	# dados = cursor.fetchall()
	# print(len(dados))
	# for dado in dados:
	# 	c.parser_acordaos(dado[0], cursor)
