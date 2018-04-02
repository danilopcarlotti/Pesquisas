from crawler_jurisprudencia_tj import crawler_jurisprudencia_tj
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from common.conexao_local import cursorConexao
from common.download_path import path
import time, datetime, urllib.request,logging, click, os, sys, re, subprocess, pyautogui

class crawler_jurisprudencia_tjto():
	"""Crawler especializado em retornar textos da jurisprudência de segunda instância do Tocantins"""
	def __init__(self):
		crawler_jurisprudencia_tj.__init__(self)
		self.link_inicial = 'http://jurisprudencia.tjto.jus.br/consulta?q=a&start=%s&rows=20'
		self.tabela_colunas = 'justica_estadual.jurisprudencia_to (ementas)'

	def download_tj(self):
		cursor = cursorConexao()
		for i in range(0,65501,20):
			try:
				link = self.link_inicial % str(i)
				driver = webdriver.Chrome(self.chromedriver)
				driver.get(link)
				time.sleep(1)
				links_inteiro_teor = driver.find_elements_by_link_text('Inteiro Teor')
				for l in links_inteiro_teor:
					try:
						cursor.execute('INSERT INTO %s value ("%s");' % (self.tabela_colunas,l.get_attribute('href')))
					except:
						pass
				driver.close()
			except Exception as e:
				print('erro com ',i,' ',e)

	def download_acordao_to(self,id_acordao,link):
		crawler_jurisprudencia_tj.download_pdf_acordao_sem_captcha(self,link,'to_2_inst_' + id_acordao)
		subprocess.Popen('mv %s/to_2_inst_* %s/acordaos_tj_to' % (path,path), shell=True)

	def parser_acordaos(self, texto, cursor, pdf_class):
		texto = pdf_class.convert_pdfminer(arquivo)
		numero = busca(r'\d{7}\-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}', texto)
		orgao_julgador = busca(r'\n\s*?Origem\:(.*?)\n', texto)
		julgador = busca(r'\n\s*?Relator.*?\:(.*?)\n', texto)
		data_decisao = busca(r'\n\s*?Palmas, (.*?)\.', texto)
		cursor.execute('INSERT INTO jurisprudencia_2_inst.jurisprudencia_2_inst (tribunal, numero, data_decisao, orgao_julgador, julgador, texto_decisao) values ("%s","%s","%s","%s","%s","%s");' % ('rj',numero, data_decisao, orgao_julgador, julgador, texto))

def main():
	c = crawler_jurisprudencia_tjto()
	cursor = cursorConexao()
	cursor.execute('SELECT id,ementas from justica_estadual.jurisprudencia_to where id > 67164 limit 10000000;')
	lista_links = cursor.fetchall()
	for i,l in lista_links:
		try:
			c.download_acordao_to(str(i),l)
		except Exception as e:
			print(e,i)
	# print('comecei ',c.__class__.__name__)
	# try:
	# 	c.download_tj()
	# except Exception as e:
	# 	print('finalizei com erro ',e)

if __name__ == '__main__':
	main()