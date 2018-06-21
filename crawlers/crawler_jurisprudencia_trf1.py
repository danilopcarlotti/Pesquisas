import time, re
from bs4 import BeautifulSoup
from common.conexao_local import cursorConexao
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from crawler_jurisprudencia_tj import crawler_jurisprudencia_tj

sys.path.append(os.path.dirname(os.getcwd()))
from common_nlp.parse_texto import busca

class crawler_jurisprudencia_trf1():
	"""Crawler especializado em retornar textos da jurisprudência de segunda instância de Maranhão"""
	def __init__(self):
		crawler_jurisprudencia_tj.__init__(self)
		self.link_inicial = 'http://www.cjf.jus.br/juris/trf1/index.jsp'
		self.pesquisa_livre = '//*[@id="td_00001"]'
		self.tipo_acordao = '//*[@id="label13"]'
		self.link_acordaos = '//*[@id="td_0005"]'
		self.botao_pesquisar = 'btnConsultar'
		self.botao_prox = '//*[@id="conteudo"]/div[1]/input[3]'

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

	cursor = cursorConexao()
	cursor.execute('SELECT ementas from justica_federal.jurisprudencia_trf1;')
	dados = cursor.fetchall()
	print(len(dados))
	for dado in dados:
		c.parser_acordaos(dado[0], cursor)
