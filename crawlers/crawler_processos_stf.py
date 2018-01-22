import re, os, sys, time, datetime, urllib.request, ssl,logging, click
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from crawlerJus import crawlerJus
from common.conexao_local import cursorConexao


class processosSTF(crawlerJus):
	"""Classe para download de informações sobre processos do STJ"""
	def __init__(self):
		super().__init__()
		ssl._create_default_https_context = ssl._create_unverified_context 
		self.link_base = 'http://www.stf.jus.br/portal/processo/verProcessoAndamento.asp?incidente='
		self.numero_final = 6000000 #Este é o último número estimado de um processo válido no STF em 11/11/2017. Número deve ser atualizado
		self.numero_inicial = 4806730#1169086 até 3000000

		
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

	def baixarDocumentos(self):
		pass
		

# if __name__ == '__main__':
# 	pass

cursor = cursorConexao()
cursor.execute('SELECT id, link_dados from stf.dados_processo limit 1000000;')
links_pai = cursor.fetchall()
links_pai_d = {}
for id_p,link in links_pai:
	links_pai_d[int(link.split('incidente=')[1])] = int(id_p)

cursor.execute('SELECT id, link_pagina from stf.texto_decisoes limit 1000000;')
links = cursor.fetchall()
for id_l,link_pag in links:
	try:
		cursor.execute('UPDATE stf.texto_decisoes set id_processo = ("%s") where id = ("%s")' % (links_pai_d[int(link_pag.split('incidente=')[1])],id_l))
	except:
		pass