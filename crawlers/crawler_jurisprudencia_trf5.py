import time, re, os, sys
from bs4 import BeautifulSoup
from common.conexao_local import cursorConexao
from crawler_jurisprudencia_tj import crawler_jurisprudencia_tj
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

sys.path.append(os.path.dirname(os.getcwd()))
from common_nlp.parse_texto import busca

class crawler_jurisprudencia_trf5():
	"""Crawler especializado em retornar textos da jurisprudência do tribunal regional federal da quarta região"""
	def __init__(self):
		crawler_jurisprudencia_tj.__init__(self)
		self.link_inicial = 'https://www4.trf5.jus.br/Jurisprudencia/'
		self.botao_pesquisar = '//*[@id="pesquisar"]'
		self.botao_prox = '//*[@id="resultado-topo"]/ul/li[4]/a'
		self.data_inicial_xpath = '//*[@id="dataInicial"]'
		self.data_final_xpath = '//*[@id="dataFinal"]'
		self.link_resultado_xpath = '//*[@id="resultado"]/div[1]/a'
		self.pesquisa_livre = '//*[@id="termos"]'
		self.tabela_colunas = 'justica_federal.jurisprudencia_trf5 (ementas)'

	def download_trf5(self, data_ini, data_fim, termo = 'direito'):
		cursor = cursorConexao()
		driver = webdriver.Chrome(self.chromedriver)
		driver.get(self.link_inicial)
		time.sleep(1)
		driver.find_element_by_xpath(self.pesquisa_livre).send_keys(termo)
		driver.find_element_by_xpath(self.data_inicial_xpath).send_keys(data_ini)
		driver.find_element_by_xpath(self.data_final_xpath).send_keys(data_fim)
		driver.find_element_by_xpath(self.botao_pesquisar).click()
		time.sleep(1)
		contador = 0
		while True:
			try:
				driver.find_element_by_xpath(self.link_resultado_xpath).click()
				break
			except:
				contador += 1
				time.sleep(1)
				if contador > 3:
					driver.close()
					return
		time.sleep(1)
		texto = crawler_jurisprudencia_tj.extrai_texto_html(self,(driver.page_source)).replace('"','')
		cursor.execute('INSERT INTO %s value ("%s");' % (self.tabela_colunas,texto))
		try:
			driver.find_element_by_xpath(self.botao_prox).click()
		except:
			driver.close()
			return
		contador = 0
		while True:
			try:
				time.sleep(1)
				texto = crawler_jurisprudencia_tj.extrai_texto_html(self,(driver.page_source)).replace('"','')
				cursor.execute('INSERT INTO %s value ("%s");' % (self.tabela_colunas,texto))
				driver.find_element_by_xpath(self.botao_prox).click()
				contador = 0
			except Exception as e:
				print(e)
				contador += 1
				time.sleep(5)
				if contador > 3:
					driver.close()
					break
		driver.close()

	def parser_acordaos(self,texto, cursor):
		decisoes = re.split(r'\nDOCUMENTO\s*?\d+',texto)
		for d in range(1,len(decisoes)):
			numero = busca(r'\nNúmero do Processo\s*?\:\s*?(\d+)', decisoes[d])
			classe = busca(r'\nClasse\s*?\:(.*?)\-', decisoes[d])
			julgador = busca(r'\n\s*?Relator.*?\:(.*?)\n', decisoes[d])
			orgao_julgador = busca(r'\nÓrgão julgador\s*?\:\s*?(.*?)\n', decisoes[d], args=re.I | re.DOTALL)
			data_disponibilizacao = busca(r'\n\s*?Data do Julgamento\s*?\:\s*?(\d{2}/\d{2}/\d{4})', decisoes[d])
			cursor.execute('INSERT INTO jurisprudencia_2_inst.jurisprudencia_2_inst (tribunal, numero, data_decisao, orgao_julgador, julgador, texto_decisao) values ("%s","%s","%s","%s","%s","%s");' % ('trf5',numero, data_disponibilizacao, orgao_julgador, julgador, decisoes[d].strip()))

if __name__ == '__main__':
	c = crawler_jurisprudencia_trf5()
	# try:
	# 	for l in range(len(c.lista_anos)):
	# 		print(c.lista_anos[l],'\n')
	# 		for m in range(len(c.lista_meses)):
	# 			for i in range(1,9):
	# 				try:
	# 					c.download_trf5('0'+str(i)+c.lista_meses[m]+c.lista_anos[l],'0'+str(i+1)+c.lista_meses[m]+c.lista_anos[l])
	# 				except Exception as e:
	# 					print(e)		
	# 			for i in range(10,27):
	# 				try:
	# 					c.download_trf5(str(i)+c.lista_meses[m]+c.lista_anos[l],str(i+1)+c.lista_meses[m]+c.lista_anos[l])
	# 				except Exception as e:
	# 					print(e)
	# except Exception as e:
	# 	print(e)

	cursor = cursorConexao()
	cursor.execute('SELECT ementas FROM justica_federal.jurisprudencia_trf5;')
	dados = cursor.fetchall()
	for ementa in dados:
		c.parser_acordaos(ementa[0],cursor)