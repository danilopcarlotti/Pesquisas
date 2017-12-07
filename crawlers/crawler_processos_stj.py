import re, os, sys, time, datetime, urllib.request, ssl,logging, click
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from crawlerJus import crawlerJus
from common.conexao_local import cursorConexao


class processosSTJ(crawlerJus):
	"""Classe para download de informações sobre processos do STJ"""
	def __init__(self, contador):
		super().__init__()
		ssl._create_default_https_context = ssl._create_unverified_context 
		self.lista_span_dados = ['//*[@id="idProcessoDetalhesBloco1"]/div[1]/span[2]', 
		'//*[@id="idDetalhesPartesAdvogadosProcuradores"]/div[1]/span[2]/a',
		'//*[@id="idDetalhesPartesAdvogadosProcuradores"]/div[2]/span[2]/a',
		'//*[@id="idProcessoDetalhesBloco1"]/div[5]/span[2]',
		'//*[@id="idProcessoDetalhesBloco1"]/div[6]/span[2]/a',
		'//*[@id="idProcessoDetalhesBloco2"]/div[1]/span[2]',
		'//*[@id="idProcessoDetalhesBloco2"]/div[2]/span[2]',
		'//*[@id="idProcessoDetalhesBloco2"]/div[3]/span[2]',
		'//*[@id="idProcessoDetalhesBloco3"]/div[1]/span[2]',
		'//*[@id="idProcessoDetalhesBloco3"]/div[2]/span[2]'
		]
		self.contador = contador
		
	def baixarDadosProcesso(self):
		driver = webdriver.Chrome(self.chromedriver)
		link_pesquisa = 'http://www.stj.jus.br/SCON/'
		driver.get(link_pesquisa)
		driver.find_element_by_xpath('//*[@id="pesquisaLivre"]').send_keys('a')
		driver.find_element_by_xpath('//*[@id="botoesPesquisa"]/input[1]').click()
		driver.find_elements_by_xpath('//*[@id="itemlistaresultados"]/span[2]/a')[2].click()
		# driver.find_element_by_xpath('//*[@id="navegacao"]/a[2]').send_keys("\n")
		driver.find_element_by_class_name('iconeProximaPagina').send_keys('\n')
		i = 1
		while i < self.contador:
			try:
				driver.find_element_by_class_name('iconeProximaPagina').send_keys('\n')
				i += 1
			except:
				try:
					driver.back()
					driver.find_element_by_class_name('iconeProximaPagina').send_keys('\n')
				except:
					if input('ajude-me\n'):
						driver.find_element_by_class_name('iconeProximaPagina').send_keys('\n')
		while self.contador < 59314:
			cursor = cursorConexao()
			try:
				acompanhamentos = driver.find_elements_by_xpath('//*[@id="acoesdocumento"]/a[2]')
				for a in acompanhamentos:
					a.click()
					marcador = 0
					while marcador < 3:
						try:
							driver.switch_to.window(driver.window_handles[1])
							driver.find_element_by_xpath('/html/body/a').click()
							marcador = 3
						except:
							marcador += 1
					info = []
					for d in self.lista_span_dados:
						try:
							info.append(driver.find_element_by_xpath(d).text)
						except:
							time.sleep(1)
							try:
								info.append(driver.find_element_by_xpath(d).text)
							except:
								pass
					if len(info) == 10:
						html = driver.page_source
						link_voto = re.search(r'/processo/revista/documento/mediado/\?componente=ATC.*?tipo=\d+',html)
						if link_voto:
							link_voto_download = 'https://ww2.stj.jus.br'+link_voto.group(0)+'&formato=html'
							info.append(link_voto_download.replace('amp;',''))
							cursor.execute('INSERT INTO stj.dados_processo (processo, recorrente, recorrido, autuacao, numero_unico, relator, ramo_direito, assunto, tribunal_origem, numeros_origem,link_voto) 		values ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")',(info[0],info[1],info[2],info[3],info[4],info[5],info[6],info[7],info[8],info[9],info[10]))
					driver.switch_to.window(driver.window_handles[0])
				try:
					driver.find_element_by_class_name('iconeProximaPagina').send_keys('\n')
					self.contador += 1
				except:
					if input('ajude-me'):
						cursor = cursorConexao()
					else:
						print(str(self.contador))
						driver.close()
						self.baixarDadosProcesso()
			except:
				if input('ajude-me'):
					cursor = cursorConexao()
				else:
					print(str(self.contador))
					driver.close()
					self.baixarDadosProcesso()

p = processosSTJ(5272)
p.baixarDadosProcesso()