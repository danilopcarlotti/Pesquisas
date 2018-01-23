import sys, re, time, pyautogui
from crawler_jurisprudencia_tj import crawler_jurisprudencia_tj
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

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

	def download_tj(self,data_ini,data_fim):
		driver = webdriver.Chrome(self.chromedriver)
		driver.get(self.link_inicial)
		driver.find_element_by_id(self.pesquisa_livre).send_keys('acordam')
		driver.find_element_by_id(self.data_julgamento_inicialID).send_keys(data_ini)
		driver.find_element_by_id(self.data_julgamento_finalID).send_keys(data_fim)
		driver.find_element_by_id(self.botao_pesquisar).click()
		time.sleep(15)
		loop_counter = 0
		while True:
			try:
				links_inteiro_teor = driver.find_elements_by_link_text('Inteiro Teor')
				for l in range(len(links_inteiro_teor)):
					try:
						links_inteiro_teor[l].click()
					except:
						continue
					driver.switch_to.window(driver.window_handles[-1])
					time.sleep(1)
					pyautogui.hotkey('ctrl','s')
					pyautogui.press('enter')
					time.sleep(1)
					driver.switch_to.window(driver.window_handles[0])
				driver.switch_to.window(driver.window_handles[0])
				driver.find_element_by_xpath(self.botao_proximoXP).click()
				time.sleep(2)
			except Exception as e:
				print(e)
				loop_counter += 1
				time.sleep(5)
				if loop_counter > 5:
					driver.close()
					return

if __name__ == '__main__':
	c = crawler_jurisprudencia_tjba()
	print('comecei ',c.__class__.__name__)
	for l in c.lista_anos:
		try:
			print(l,'\n')
			c.download_tj('01/01/'+l,'31/12/'+l)
		except Exception as e:
			print('finalizei com erro ',e)