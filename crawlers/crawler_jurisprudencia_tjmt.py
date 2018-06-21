from bs4 import BeautifulSoup
from crawler_jurisprudencia_tj import crawler_jurisprudencia_tj
from common.conexao_local import cursorConexao
from common.download_path import path
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sys, re, time, os, pyautogui

sys.path.append(os.path.dirname(os.getcwd()))
from common_nlp.parse_texto import busca
from common_nlp.pdf_to_text import pdf_to_text

contador = 0

class crawler_jurisprudencia_tjmt():
	"""Crawler especializado em retornar textos da jurisprudência de segunda instância do Mato Grosso"""
	def __init__(self):
		crawler_jurisprudencia_tj.__init__(self)
		self.link_inicial = 'http://jurisprudencia.tjmt.jus.br/'
		self.pesquisa_livre = '//*[@id="FiltroBasico"]'
		self.botao_pesquisar = '//*[@id="BotaoConsulta"]' 
		self.botao_proximo_XP = '//*[@id="AcordaoPagination"]/ul/li[%s]/a'  
		self.tabela_colunas = 'justica_estadual.jurisprudencia_mt (ementas)' 

	def download_tj(self, termo='a'):
		global contador
		driver = webdriver.Chrome(self.chromedriver)
		driver.get(self.link_inicial)
		driver.find_element_by_xpath(self.pesquisa_livre).send_keys(termo)
		driver.find_element_by_xpath(self.botao_pesquisar).click()
		time.sleep(5)
		botao_prox = self.botao_proximo_XP % '10'
		driver.find_element_by_xpath(botao_prox).click()
		contador_proximo = 2
		loop_counter = 0
		while True:
			try:
				time.sleep(3)
				for i in range(1,11):
					try:
						driver.find_element_by_xpath('//*[@id="divDetalhesConsultaAcordao"]/div[%s]/div/table/thead[1]/tr/td[2]/button[1]' % str(i)).click()
						driver.switch_to.window(driver.window_handles[-1])
						contador += 1
						time.sleep(1)
						pyautogui.hotkey('ctrl','s')
						time.sleep(1)
						pyautogui.typewrite('Acordao_MT_'+str(contador))
						time.sleep(1)
						pyautogui.press('enter')
						time.sleep(1)
						pyautogui.hotkey('ctrl','w')
						driver.switch_to.window(driver.window_handles[0])
					except Exception as e:
						continue
				driver.switch_to.window(driver.window_handles[0])
				if contador_proximo < 4:
					contador_proximo += 1
				elif contador_proximo < 6:
					botao_prox = self.botao_proximo_XP % str(contador_proximo + 7)
					contador_proximo += 1
				else:
					botao_prox = self.botao_proximo_XP % '13'
				driver.find_element_by_xpath(botao_prox).click()
			except Exception as e:
				print(e)
				loop_counter += 1
				if loop_counter > 5:
					break
		driver.close()

	def parser_acordaos(self, arquivo, cursor, pdf_class):
		texto = pdf_class.convert_pdfminer(arquivo).replace('\\','').replace('/','').replace('"','')
		numero = busca(r'\n.*?N. (.*?) - CLASSE CNJ', texto)
		julgador = busca(r'\n\s*?DESEMBARGADOR[A]?(.*?)- RELATOR', texto)		
		data_decisao = busca(r'\n\s*?Data de Julgamento\:(.*?)\n', texto)
		cursor.execute('INSERT INTO jurisprudencia_2_inst.jurisprudencia_2_inst (tribunal, numero, data_decisao, julgador, texto_decisao) values ("%s","%s","%s","%s","%s");' % ('mt',numero, data_decisao, julgador, texto))

if __name__ == '__main__':
	c = crawler_jurisprudencia_tjmt()
	
	cursor = cursorConexao()
	p = pdf_to_text()
	for arq in os.listdir(path+'/mt_2_inst'):
		try:
			c.parser_acordaos(path+'/mt_2_inst/'+arq, cursor, p)
		except Exception as e:
			print(e)

	# print('comecei ',c.__class__.__name__)
	# try:
	# 	c.download_tj()
	# except Exception as e:
	# 	print(e)
	# 	print('finalizei com erro\n')