from bs4 import BeautifulSoup
from common.conexao_local import cursorConexao
from common.download_path import path
from common_nlp.parse_texto import busca
from common_nlp.pdf_to_text import pdf_to_text
from crawler_jurisprudencia_tj import crawler_jurisprudencia_tj
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sys, re, time, subprocess, urllib.request, os

class crawler_jurisprudencia_tjpb(crawler_jurisprudencia_tj):
	"""Crawler especializado em retornar textos da jurisprudência de segunda instância da Paraíba"""
	def __init__(self):
		crawler_jurisprudencia_tj.__init__(self)
		self.link_inicial = 'http://juris.tjpb.jus.br/search?site=jurisp_digitalizada&client=tjpb_index&output=xml_no_dtd&proxystylesheet=tjpb_index&proxycustom=%3CHOME/%3E'
		self.pesquisa_livre = 'q'
		self.botao_pesquisar = '//*[@id="central"]/span/div/input[1]'
		self.tabela_colunas = 'justica_estadual.jurisprudencia_pb (ementas)'
		self.botao_proximo_iniXP = '//*[@id="content"]/div[2]/div[2]/div/div/span[2]/a '
		self.botao_proximoXP = '//*[@id="content"]/div[2]/div[2]/div/div/span[4]/a'
		self.botao_data_iniXP = '//*[@id="dataIni"]'
		self.botao_data_fimXP = '//*[@id="dataFim"]'
		self.tabela_colunas = 'justica_estadual.jurisprudencia_pb (ementas)'

	def download_tj(self,dataIni,dataFim):
		cursor = cursorConexao()
		driver = webdriver.Chrome(self.chromedriver)
		driver.get(self.link_inicial)
		driver.find_element_by_id(self.pesquisa_livre).send_keys('a')
		driver.find_element_by_xpath(self.botao_data_iniXP).send_keys(dataIni)
		driver.find_element_by_xpath(self.botao_data_fimXP).send_keys(dataFim)
		driver.find_element_by_xpath('//*[@id="radio-intteor"]').click()
		driver.find_element_by_xpath(self.botao_pesquisar).click()
		loop_counter = 0
		links_inteiro_teor = driver.find_elements_by_class_name('inteiro-teor')
		for l in links_inteiro_teor:
			cursor.execute('INSERT INTO %s value ("%s");' % (self.tabela_colunas,l.get_attribute("href")))
		driver.find_element_by_xpath(self.botao_proximo_iniXP).click()
		contador = 0
		while True:
			try:
				links_inteiro_teor = driver.find_elements_by_class_name('inteiro-teor')
				for l in links_inteiro_teor:
					cursor.execute('INSERT INTO %s value ("%s");' % (self.tabela_colunas,l.get_attribute("href")))
				driver.find_element_by_xpath(self.botao_proximoXP).click()
				time.sleep(2)
			except Exception as e:
				print(e)
				contador += 1
				if contador > 2:
					break
		driver.close()

	def download_acordao_pb(self,id_acordao,link):
		crawler_jurisprudencia_tj.download_pdf_acordao(self,link,'','','','pb_2_inst_' + id_acordao)
		subprocess.Popen('mv /home/danilo/Downloads/pb_2_inst_* /home/danilo/Downloads/acordaos_tj_pb', shell=True)

	def parser_acordaos(self, arquivo, cursor, pdf_class):
		texto = pdf_class.convert_PyPDF2(arquivo)
		numero = busca(r'\d{3,7}\.\d{4}\.\d{6}\-\d{1}/\d{3}', texto, ngroup=0)
		classe = busca(r'ACÓRDÃO(.*?)N.\s*?\d{3,7}\.\d{4}\.\d{6}\-\d{1}/\d{3}', texto)
		julgador = busca(r'RELATOR.*?\:(.*?Des\..*?)\.', texto)
		data_disponibilizacao = busca(r'\.\s*?João Pessoa(.*?)\.', texto)[:44]
		cursor.execute('INSERT INTO jurisprudencia_2_inst.jurisprudencia_2_inst (tribunal, numero, classe, data_decisao, julgador, texto_decisao) values ("%s","%s","%s","%s","%s","%s");' % ('pb',numero, classe, data_disponibilizacao, julgador, texto.replace('"','').replace('\\','').replace('/','')))

def main():
	c = crawler_jurisprudencia_tjpb()
	cursor = cursorConexao()

	p = pdf_to_text()
	for arq in os.listdir(path+'/pb_2_inst'):
		try:
			c.parser_acordaos(path+'/pb_2_inst/'+arq, cursor, p)
		except Exception as e:
			print(arq)
			print(e)

	
	# cursor.execute('SELECT id,ementas from justica_estadual.jurisprudencia_pb where id > 37630 limit 10000000;')
	# lista_links = cursor.fetchall()
	# for i,l in lista_links:
	# 	try:
	# 		c.download_acordao_pb(str(i),l)
	# 	except Exception as e:
	# 		print(e,i)
	

	# print('comecei ',c.__class__.__name__)
	# try:
	# 	for a in c.lista_anos:
	# 		for m in range(len(c.lista_meses)):
	# 			c.download_tj('01'+c.lista_meses[m]+a,'14'+c.lista_meses[m]+a)
	# 			c.download_tj('15'+c.lista_meses[m]+a,'28'+c.lista_meses[m]+a)
	# except Exception as e:
	# 	print('finalizei com erro ',e)

if __name__ == '__main__':
	main()