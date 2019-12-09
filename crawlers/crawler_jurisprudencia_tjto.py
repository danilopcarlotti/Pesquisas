from crawler_jurisprudencia_tj import crawler_jurisprudencia_tj
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from common.conexao_local import cursorConexao
from common.download_path import path, path_hd
import time, datetime, urllib.request,logging, click, os, sys, re, subprocess, pyautogui

class crawler_jurisprudencia_tjto():
	"""Crawler especializado em retornar textos da jurisprudência de segunda instância do Tocantins"""
	def __init__(self):
		crawler_jurisprudencia_tj.__init__(self)
		self.link_inicial = 'http://jurisprudencia.tjto.jus.br/consulta?q=a&start=%s&rows=20'
		self.tabela_colunas = 'justica_estadual.jurisprudencia_to (ementas)'

	def download_tj(self):
		cursor = cursorConexao()
		for i in range(0,65501,20): #jun 2018
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
		subprocess.Popen('mv %s/to_2_inst_* %s/to_2_inst' % (path,path), shell=True)

	def download_diario_retroativo(self):
		# último número do diário em 04.07.2018
		for i in range(4635,3253,-1):
			try:
				print('http://wwa.tjto.jus.br/diario/diariopublicado/%s.pdf' % str(i))
				response = urllib.request.urlopen('http://wwa.tjto.jus.br/diario/diariopublicado/%s.pdf' % str(i),timeout=15)
				file = open(str(i)+".pdf", 'wb')
				time.sleep(1)
				file.write(response.read())
				file.close()
				subprocess.Popen('mkdir "%s/Diarios_to/%s"' % (path_hd,str(i)), shell=True) 
				subprocess.Popen('mv %s/*.pdf "%s/Diarios_to/%s"' % (os.getcwd(),path_hd,str(i)), shell=True)
			except Exception as e:
				print(e)

	def parser_acordaos(self):
		p = pdf_to_text()
		cursor = cursorConexao()
		for arquivo in os.listdir(path+'/to_2_inst'):
			texto = p.convert_pdfminer(path+'/to_2_inst/'+arquivo).replace('\\','').replace('/','').replace('"','')
			numero = busca(r'\d{7}\-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}', texto)
			orgao_julgador = busca(r'\n\s*?Origem\:(.*?)\n', texto)
			julgador = busca(r'\n\s*?Relator.*?\:(.*?)\n', texto)
			data_decisao = busca(r'\n\s*?Palmas, (.*?)\.', texto)
			cursor.execute('INSERT INTO jurisprudencia_2_inst.jurisprudencia_2_inst (tribunal, numero, data_decisao, orgao_julgador, julgador, texto_decisao) values ("%s","%s","%s","%s","%s","%s");' % ('rj',numero, data_decisao, orgao_julgador, julgador, texto))

def main():
	c = crawler_jurisprudencia_tjto()

	c.download_diario_retroativo()

	# cursor = cursorConexao()
	# cursor.execute('SELECT id,ementas from justica_estadual.jurisprudencia_to where id > 67164 limit 10000000;')
	# lista_links = cursor.fetchall()
	# for i,l in lista_links:
	# 	try:
	# 		c.download_acordao_to(str(i),l)
	# 	except Exception as e:
	# 		print(e,i)
	# print('comecei ',c.__class__.__name__)
	# try:
	# 	c.download_tj()
	# except Exception as e:
	# 	print('finalizei com erro ',e)

if __name__ == '__main__':
	main()