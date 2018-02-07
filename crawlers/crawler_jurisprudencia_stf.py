import re, os, sys, time, datetime, urllib.request, ssl,logging, pyautogui
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

	def baixarDadosProcesso(self,link_processos):
		cursor = cursorConexao()
		id_processo_stf = ''
		for id_p, link in link_processos:
			try:
				relator = ''
				pag = self.baixa_pag(link)
				soup = BeautifulSoup(pag,'html.parser')
				div_andamento = [x for x in soup.find('div',{'id':'detalheProcesso'}).get_text().split('\n') if x != '']
				for i in range(len(div_andamento)-1):
					if div_andamento[i] == 'Relator atual':
						relator = div_andamento[i+1]
				link = link.replace('Andamento','Detalhe')
				pag = self.baixa_pag(link)
				soup = BeautifulSoup(pag,'html.parser')
				div_detalhe = [x for x in soup.find('div',{'id':'conteudoAbasAcompanhamento'}).get_text().split('\n') if x != '']
				id_processo_stf = soup.find('h3').text.split('-')[0].strip()
				assunto = ''
				autuacao = ''
				numero_origem = ''
				polo_ativo = ''
				polo_passivo = ''
				ramo_direito = ''
				tribunal_origem = ''
				for i in range(len(div_detalhe)-1):
					if div_detalhe[i] == 'Orgão de Origem:':
						tribunal_origem = div_detalhe[i+1].replace(')','').replace('(','').replace('\\','').replace('"','').replace('/','')
					elif div_detalhe[i] == 'Números de Origem:':
						numero_origem = div_detalhe[i+1].replace(')','').replace('(','').replace('\\','').replace('"','').replace('/','')
					elif div_detalhe[i] == 'Ramo do Direito':
						if div_detalhe[i+1] != 'Assunto':
						 	ramo_direito = div_detalhe[i+1].replace(')','').replace('(','').replace('\\','').replace('"','').replace('/','')
					elif div_detalhe[i] == 'Assunto':
						assunto = div_detalhe[i+1].replace(')','').replace('(','').replace('\\','').replace('"','').replace('/','')
					elif div_detalhe[i] == 'Data de Protocolo':
						autuacao = div_detalhe[i+1].replace(')','').replace('(','').replace('\\','').replace('"','').replace('/','')
					elif re.search(r'TE\.\(S\)',div_detalhe[i]):
						polo_ativo = div_detalhe[i+1].replace(')','').replace('(','').replace('\\','').replace('"','').replace('/','')
					elif re.search(r'DO\.\(A/S\)',div_detalhe[i]):
						polo_passivo = div_detalhe[i+1].replace(')','').replace('(','').replace('\\','').replace('"','').replace('/','')
				cursor.execute('INSERT INTO stf.dados_processo (processo, polo_ativo, polo_passivo, autuacao, numero_origem, relator, ramo_direito, assunto, tribunal_origem, link_dados) values ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' % (id_processo_stf, polo_ativo, polo_passivo, autuacao, numero_origem, relator, ramo_direito, assunto, tribunal_origem, link))
			except Exception as e:
				print(e)

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
									cursor.execute('INSERT INTO stf.texto_decisoes (link_pagina, texto_decisao) values("%s","%s");' % (link,texto_final))

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
		time.sleep(3)
		for i in ids_doc:
			try:
				driver.refresh()
				while True:
					try:
						driver.find_element_by_xpath(processo_interesse_xpath).send_keys(i)
						time.sleep(10)
						driver.find_element_by_xpath(submit_processo_interesse_xpath).click()
						time.sleep(2)
						driver.find_element_by_xpath(ver_mais_processo_interesse_xpath).click()
						break
					except:
						time.sleep(1)
				while True:
					try:
						time.sleep(2)
						driver.switch_to.window(driver.window_handles[1])
						time.sleep(1)
						driver.find_element_by_xpath(aba_pecas_xpath).click()
						driver.find_element_by_xpath(download_todas_pecas_xpath).click()
						time.sleep(2)
						pyautogui.hotkey('ctrl','w')
						break
					except:
						time.sleep(1)
				time.sleep(1)
				driver.switch_to.window(driver.window_handles[0])
			except:
				if len(driver.window_handles) > 1:
					driver.switch_to.window(driver.window_handles[-1])
					pyautogui.hotkey('ctrl','w')
				driver.switch_to.window(driver.window_handles[0])
		driver.close()

if __name__ == '__main__':
	cursor = cursorConexao()
	c = crawler_jurisprudencia_stf()

	# lista_ids = []
	# lista_ids = str(set(lista_ids)).replace('[','').replace(']','')
	# cursor.execute('SELECT processo from stf.dados_processo where id in (%s);' % lista_ids)
	
	# cursor.execute('SELECT processo from stf.dados_processo where limit 1000000;')
	# links_d = cursor.fetchall()
	# c.solicitar_link_download_documentos(links_d)

	cursor.execute('SELECT processo from stf.dados_processo limit 1000000;')
	ids_doc = cursor.fetchall()
	c.solicitar_link_download_documentos(ids_doc)
	c.baixar_documentos_stf()
	
	# cursor.execute('SELECT id, link_pagina from stf.decisoes limit 1000000;')
	# link_decisoes = cursor.fetchall()
	# c.baixarDadosProcesso(link_decisoes)



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