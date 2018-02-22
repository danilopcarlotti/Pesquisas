import sys, re, time, pyautogui,subprocess
from crawler_jurisprudencia_tj import crawler_jurisprudencia_tj
from bs4 import BeautifulSoup
from common.download_path import path
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
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

	def download_tj(self):
		driver = webdriver.Chrome(self.chromedriver)
		driver.get(self.link_inicial)
		driver.find_element_by_id(self.pesquisa_livre).send_keys('acordam')
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

if __name__ == '__main__':
	c = crawler_jurisprudencia_tjba()
	print('comecei ',c.__class__.__name__)
	try:
		c.download_tj()
	except Exception as e:
		print('finalizei com erro ',e)