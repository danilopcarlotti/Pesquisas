from bs4 import BeautifulSoup
from common.conexao_local import cursorConexao
from common.download_path import path
from crawler_jurisprudencia_tj import crawler_jurisprudencia_tj
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import sys, re, time, pyautogui,subprocess, urllib.request, os

sys.path.append(os.path.dirname(os.getcwd()))
from common_nlp.parse_texto import busca
from common_nlp.pdf_to_text import pdf_to_text

class crawler_jurisprudencia_tjba():
	"""Crawler especializado em retornar textos da jurisprudência de segunda instância da Bahia"""
	def __init__(self):
		crawler_jurisprudencia_tj.__init__(self)
		self.link_inicial = 'https://www2.tjba.jus.br/erp-portal/publico/jurisprudencia/consultaJurisprudencia.xhtml'
		self.pesquisa_livre = 'palavrasChaveId'
		self.botao_pesquisar = 'j_idt143'
		self.data_julgamento_inicialID = 'dtJulgamentoInicialId_input'
		self.data_julgamento_finalID = 'dtJulgamentoFinalId_input'
		self.botao_proximoXP = '//*[@id="jurisprudenciaGridId_paginator_top"]/span[5]/span'
		self.tabela_colunas = 'justica_estadual.jurisprudencia_ba (ementas)'

	def download_tj(self, termo='acordam'):
		driver = webdriver.Chrome(self.chromedriver)
		driver.get(self.link_inicial)
		driver.find_element_by_id(self.pesquisa_livre).send_keys(termo)
		driver.find_element_by_id(self.botao_pesquisar).click()
		time.sleep(15)
		loop_counter = 0
		contador = 10
		aux = 0
		while aux < 1427:
			try:
				driver.execute_script("return arguments[0].scrollIntoView();", driver.find_element_by_xpath(self.botao_proximoXP))
				driver.find_element_by_xpath(self.botao_proximoXP).click()
				aux += 1
				contador += 10
			except:
				time.sleep(1)
		while True:
			try:
				links_inteiro_teor = driver.find_elements_by_link_text('Inteiro Teor')
				for l in range(len(links_inteiro_teor)):
					try:
						driver.execute_script("return arguments[0].scrollIntoView();", links_inteiro_teor[l])
						time.sleep(0.5)
						links_inteiro_teor[l].click()
						contador += 1
					except Exception as e:
						print(e)
						continue
					driver.switch_to.window(driver.window_handles[-1])
					time.sleep(1)
					pyautogui.hotkey('ctrl','s')
					time.sleep(1)
					pyautogui.typewrite('ba_2_inst_'+str(contador))
					time.sleep(1)
					pyautogui.press('enter')
					time.sleep(1)
					pyautogui.hotkey('ctrl','w')
					driver.switch_to.window(driver.window_handles[0])
				subprocess.Popen('mv %s/ba_2_inst_*.pdf %s/ba_2_inst' % (path,path), shell=True)
				driver.switch_to.window(driver.window_handles[0])
				driver.execute_script("return arguments[0].scrollIntoView();", driver.find_element_by_xpath(self.botao_proximoXP))
				driver.find_element_by_xpath(self.botao_proximoXP).click()
				time.sleep(2)
			except Exception as e:
				print(e)
				loop_counter += 1
				time.sleep(5)
				if loop_counter > 5:
					driver.close()
					return

	def download_1_inst(self):
		link_1_inst = 'http://www5.tjba.jus.br/unicorp/index.php/publicacoes/banco-de-sentencas/19-publicacoes/banco-de-sentencas/95-banco-de-sentencas-tjba'
		driver = webdriver.Chrome(self.chromedriver)
		driver.get(link_1_inst)
		pag = BeautifulSoup(driver.page_source,'lxml')
		contador = 0
		for l in pag.find_all('a', href=True):
			if re.search(r'/unicorp/images/.*?pdf',l['href']):
				try:
					urllib.request.urlretrieve('http://www5.tjba.jus.br'+l['href'],'TJBA_1_inst_%s.pdf' % str(contador))
					subprocess.Popen('mv TJBA_1_inst_*.pdf %s/ba_1_inst' % (path,), shell=True)
					contador += 1
				except Exception as e:
					print(e)
		driver.close()
	
	def parser_acordaos(self, arquivo, cursor, pdf_class):
		texto = pdf_class.convert_pdfminer(arquivo).replace('\\','').replace('/','').replace('"','')
		numero = busca(r'\nClasse\s*?\:\s*?\w+\s*?nº (.{1,40})', texto)
		julgador = busca(r'\nRelator\s*?\:(.*?)\n', texto)
		assunto = busca(r'\nAssunto\s*?\:(.*?)\n', texto)
		data_decisao = busca(r'\n\s*?Sala das Sessões\,(.*?)\.', texto)
		orgao_julgador = busca(r'\s*?PODER JUDICIÁRIO DO ESTADO DA BAHIA\nTRIBUNAL DE JUSTIÇA\n(.*?)\n', texto)
		try:
			cursor.execute('INSERT INTO jurisprudencia_2_inst.jurisprudencia_2_inst (tribunal, numero, assunto, data_decisao, orgao_julgador, julgador, texto_decisao) values ("%s","%s","%s","%s","%s","%s","%s");' % ('ba',numero, assunto, data_decisao, orgao_julgador, julgador, texto))
		except:
			pass

def main():
	c = crawler_jurisprudencia_tjba()
	
	cursor = cursorConexao()
	p = pdf_to_text()
	for arq in os.listdir(path+'/ba_2_inst'):
		c.parser_acordaos(path+'/ba_2_inst/'+arq, cursor, p)


	# c.download_1_inst()

	# print('comecei ',c.__class__.__name__)
	# try:
	# 	c.download_tj()
	# except Exception as e:
	# 	print('finalizei com erro ',e)

if __name__ == '__main__':
	main()