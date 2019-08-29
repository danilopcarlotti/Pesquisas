import sys, re, time, os, subprocess, pyautogui
from bs4 import BeautifulSoup
from common.conexao_local import cursorConexao
from common.download_path import path, path_hd
from crawler_jurisprudencia_tj import crawler_jurisprudencia_tj
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select

sys.path.append(os.path.dirname(os.getcwd()))
from common_nlp.parse_texto import busca

class crawler_jurisprudencia_tst():
	"""Crawler especializado em retornar textos da jurisprudência de segunda instância do Piauí"""
	def __init__(self):
		crawler_jurisprudencia_tj.__init__(self)
		self.link_inicial = 'https://jurisprudencia.tst.jus.br/'
		self.botao_pesquisar = '//*[@id="root"]/div/div[2]/form/div/div[1]/div[2]/div[2]/div/button[1]'
		self.botao_fechar = '/html/body/div[2]/div[2]/div/div[3]/button'
		self.file_links = open('/media/danilo/Seagate Expansion Drive/Links_tst/lista_links.txt','a')
		self.botao_proximo_xp = '/html/body/div/div/main/header/div[2]/div[1]/div[3]/div/div[3]/button[2]'

	def download_tst(self, pular_n=0):
		driver = webdriver.Chrome(self.chromedriver)
		driver.get(self.link_inicial)
		time.sleep(1)
		target = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[3]/button')
		driver.execute_script('arguments[0].scrollIntoView(true);', target)
		time.sleep(1)
		driver.find_element_by_xpath(self.botao_fechar).click()
		time.sleep(1)
		driver.find_element_by_xpath(self.botao_pesquisar).click()
		# time.sleep(10)
		if input('Aguardando loading'):
			pass
		contador = pular_n
		while contador:
			try:
				target = driver.find_element_by_xpath(self.botao_proximo_xp)
				driver.execute_script('arguments[0].scrollIntoView(true);', target)
				driver.find_element_by_xpath(self.botao_proximo_xp).click()
				time.sleep(2)
				contador -= 1
			except:
				time.sleep(10)
		print('Terminei de andar para frente')
		time.sleep(25)
		while True:
			try:
				html_source = driver.page_source
				pag_jur = BeautifulSoup(html_source,'html.parser')
				links = pag_jur.find_all('a')
				for l in links:
					if l.get('href')[0] == '#':
						self.file_links.write(l.get('href')+'\n')
				target = driver.find_element_by_xpath(self.botao_proximo_xp)
				driver.execute_script('arguments[0].scrollIntoView(true);', target)
				driver.find_element_by_xpath(self.botao_proximo_xp).click()
				time.sleep(6)
			except:
				aux = False
				while not aux:
					try:
						target = driver.find_element_by_xpath(self.botao_proximo_xp)
						driver.execute_script('arguments[0].scrollIntoView(true);', target)
						driver.find_element_by_xpath(self.botao_proximo_xp).click()
						time.sleep(10)
						aux = True
					except:
						time.sleep(10)
		driver.close()

	def parser_acordaos(self,texto,cursor):
		pass


if __name__ == '__main__':
	c = crawler_jurisprudencia_tst()
	print('comecei ',c.__class__.__name__)
	try:
		c.download_tst(pular_n=71180)
	except Exception as e:
		print(e)
		print('finalizei com erro\n')
