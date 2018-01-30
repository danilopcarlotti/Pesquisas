import re, os, sys, time, datetime, urllib.request, ssl,logging, click
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from crawlerJus import crawlerJus
from common.conexao_local import cursorConexao
from common.login_stf import USER,SENHA


class crawler_jurisprudencia_stf(crawlerJus):
	"""Classe para download de informações sobre processos do STJ"""
	def __init__(self):
		super().__init__()
		ssl._create_default_https_context = ssl._create_unverified_context 
		self.link_base = 'http://www.stf.jus.br/portal/processo/verProcessoAndamento.asp?incidente='
		self.numero_final = 6000000 #Este é o último número estimado de um processo válido no STF em 11/11/2017. Número deve ser atualizado
		self.numero_inicial = 2000000

	def baixarDadosProcesso(self):
		pass

	def baixarVotos(self,link):
		pagina = self.baixa_pag(link)
		if pagina != '':
			pagina = BeautifulSoup(pagina,'lxml')
			validade = pagina.find("div", {"id": "detalheProcesso"})
			if validade:
				jurisprudencia = pagina.find('a', href=re.compile(r'.+/jurisprudencia/listarConso.+'))
				if jurisprudencia:
					link_jurisprudencia = 'http://www.stf.jus.br/portal'+jurisprudencia['href'][2:]
					pagina_jurisprudencia = self.baixa_pag(link_jurisprudencia)
					if pagina_jurisprudencia != '':
						pagina = BeautifulSoup(pagina_jurisprudencia,'lxml')
						link_texto_jurisprudencia = pagina.find('a',href=re.compile(r'listarJurisprudencia\.asp\?.+'))
						if link_texto_jurisprudencia:
							link_texto = "http://www.stf.jus.br/portal/jurisprudencia/"+link_texto_jurisprudencia['href']
							pagina_texto = self.baixa_pag(link_texto)
							pagina = BeautifulSoup(pagina_texto,'lxml')
							div_texto = pagina.find('div',{'id':'divImpressao'})
							if div_texto:
								texto_final = div_texto.get_text().replace('\"','')
								if texto_final:
									cursor = cursorConexao()
									cursor.execute('INSERT INTO processos_stf.texto_decisoes (link_pagina, texto_decisao) values("%s","%s");' % (link,texto_final))

	def baixa_decisoes_proc(self):
		contador = 0
		for i in range(self.numero_inicial,self.numero_final):
			self.baixarVotos(self.link_base+str(i))
			if i % 1000 == 0:
				print(i)

	def baixar_documentos_stf(self):
		print('**FAZENDO DOWNLOAD DOS DOCUMENTOS DE PROCESSOS DO STF**')
		driver = self.login_stf()
		link_mensagem_link = '//*[@id="example"]/tbody/tr/td[2]/span/a'
		link_download = '//*[@id="idModalVisualizacaoConteudoComunicacao"]/div/div/div[2]/div/div/h4/div/p[2]/a'
		time.sleep(5)
		while True:
			try:
				driver.find_element_by_xpath(link_mensagem_link).click()
				time.sleep(1)
				driver.find_element_by_xpath(link_download).click()
				time.sleep(1)
				driver.switch_to.window(driver.window_handles[0])
				driver.find_element_by_xpath('/html/body/a').click()
				time.sleep(1)
			except:
				driver.refresh()
				time.sleep(5)

	def login_stf(self):
		driver = webdriver.Chrome(self.chromedriver)
		link = 'https://sistemas.stf.jus.br/peticionamento/'
		driver.get(link)
		try:
			senha_xpath = '//*[@id="password"]'
			submit_login_xpath = '//*[@id="fm1"]/div[3]/div[2]/input'
			username_xpath = '//*[@id="username"]'
			driver.find_element_by_xpath(username_xpath).send_keys(USER)
			driver.find_element_by_xpath(senha_xpath).send_keys(SENHA)
			driver.find_element_by_xpath(submit_login_xpath).click()
		except:
			pass
		return driver

	def solicitar_link_download_documentos(self,ids_doc):
		driver = self.login_stf()
		aba_pecas_xpath = '//*[@id="abaPecas"]'
		download_todas_pecas_xpath = '//*[@id="pecas"]/processo-pecas/div/div/div/div/div/button[3]'
		processo_interesse_xpath = '//*[@id="txt-pesquisa-processo"]'
		submit_processo_interesse_xpath = '//*[@id="container"]/div[3]/div[1]/div[2]/div[2]/div/div/div[4]/div/div[1]/div/span/button'
		ver_mais_processo_interesse_xpath = '//*[@id="container"]/div[3]/div[1]/div[2]/div[2]/div/div/div[4]/div/div[2]/div/div/a'
		time.sleep(2)
		for i in ids_doc:
			driver.find_element_by_xpath(processo_interesse_xpath).send_keys(i)
			driver.find_element_by_xpath(submit_processo_interesse_xpath).click()
			time.sleep(1)
			driver.find_element_by_xpath(ver_mais_processo_interesse_xpath).click()
			while True:
				try:
					driver.switch_to.window(driver.window_handles[1])
					time.sleep(1)
					driver.find_element_by_xpath(aba_pecas_xpath).click()
					driver.find_element_by_xpath(download_todas_pecas_xpath).click()
					break
				except:
					time.sleep(1)
			driver.switch_to.window(driver.window_handles[0])
		driver.close()

if __name__ == '__main__':
	c = crawler_jurisprudencia_stf()

# cursor = cursorConexao()
# cursor.execute('SELECT id, link_dados from stf.dados_processo limit 1000000;')
# links_pai = cursor.fetchall()
# links_pai_d = {}
# for id_p,link in links_pai:
# 	links_pai_d[int(link.split('incidente=')[1])] = int(id_p)

# cursor.execute('SELECT id, link_pagina from stf.texto_decisoes limit 1000000;')
# links = cursor.fetchall()
# for id_l,link_pag in links:
# 	try:
# 		cursor.execute('UPDATE stf.texto_decisoes set id_processo = ("%s") where id = ("%s")' % (links_pai_d[int(link_pag.split('incidente=')[1])],id_l))
# 	except:
# 		pass