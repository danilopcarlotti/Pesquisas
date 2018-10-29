import re, os, sys, time, datetime, ssl
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from crawlerJus import crawlerJus
from common.conexao_local import cursorConexao

class crawler_jurisprudencia_carf(crawlerJus):
	"""Classe para download de informações sobre processos do STJ"""
	def __init__(self):
		super().__init__()
		ssl._create_default_https_context = ssl._create_unverified_context 
		self.link_base = 'https://carf.fazenda.gov.br/sincon/public/pages/ConsultarJurisprudencia/consultarJurisprudenciaCarf.jsf'
		self.data_ini_xp = '//*[@id="dataInicialInputDate"]'
		self.input_pesquisa_xp = '//*[@id="valor_pesquisa3"]'
		self.botao_pesquisar_xp = '//*[@id="botaoPesquisarCarf"]'
		self.botao_proximo_xp = '//*[@id="dataScroller_1_table"]/tbody/tr/td[5]/div'

	def baixar_jurisprudencia_carf(self,termo='a ou não a'):
		cursor = cursorConexao()
		driver = webdriver.Chrome(self.chromedriver)
		driver.get(self.link_base)
		driver.find_element_by_xpath(self.data_ini_xp).clear()
		driver.find_element_by_xpath(self.data_ini_xp).send_keys('01/1990')
		driver.find_element_by_xpath(self.input_pesquisa_xp).send_keys(termo)
		driver.find_element_by_xpath(self.botao_pesquisar_xp).click()
		time.sleep(5)
		while True:
			try:
				driver.find_element_by_xpath(self.botao_proximo_xp)
				break
			except:
				time.sleep(1)
		while True:
			try:
				driver.execute_script("document.getElementById('conteudo_principal').style.display='inline-block';")
				time.sleep(1)
				texto = driver.page_source
				pag = BeautifulSoup(texto,'html.parser')
				if len(pag.find_all('div', {'id': re.compile(r'tblJurisprudencia\:\d{,3}\:j_')})):
					self.parsear_html(texto)
				else:
					print(texto)
					return
				# cursor.execute('insert into jurisprudencia_carf.html_decisoes (html_decisoes) values ("%s")' % (driver.page_source.replace('"',''),))
				driver.find_element_by_xpath(self.botao_proximo_xp).click()
				while driver.page_source == texto:
					time.sleep(1)
			except Exception as e:
				print(e)
				return

	def parsear_html(self, html):
		cursor = cursorConexao()
		pag = BeautifulSoup(html,'html.parser')
		numeros = []
		for div in pag.find_all('div', {'id': re.compile(r'tblJurisprudencia\:\d{,3}\:j_')}):
			for script in div(["script", "style"]):
				script.extract()
			texto_parseado = div.get_text().replace('\t','')
			acordao = re.search(r'Acórdão\:(.*)Número do Processo\:', texto_parseado, flags=re.DOTALL).group(1).strip()
			numero_processo = re.search(r'Número do Processo\:(.*)Data de Publicação\:', texto_parseado, flags=re.DOTALL).group(1).strip()
			data_publicacao = re.search(r'Data de Publicação\:(.*)Contribuinte\:', texto_parseado, flags=re.DOTALL).group(1).strip()
			contribuinte = re.search(r'Contribuinte\:(.*)Relator\(a\)\:', texto_parseado, flags=re.DOTALL).group(1).strip()
			relator = re.search(r'Relator\(a\)\:(.*)Ementa\:', texto_parseado, flags=re.DOTALL).group(1).strip()
			ementa = re.search(r'Ementa\:(.*?)Decisão', texto_parseado, flags=re.DOTALL).group(1).strip()
			decisao = re.search(r'Decisão\:(.*?)$', texto_parseado, flags=re.DOTALL).group(1).strip()
			if numero_processo not in numeros:
				numeros.append(numero_processo)
				cursor.execute('INSERT INTO jurisprudencia_carf.decisoes_carf (acordao, numero_processo, data_publicacao, contribuinte, relator, ementa, decisao) values ("%s","%s","%s","%s","%s","%s","%s")' % (acordao, numero_processo, data_publicacao, contribuinte.replace('"','').replace('\\','').replace('\n',' '), relator.replace('"','').replace('\\','').replace('\n',' '), ementa.replace('"','').replace('\\','').replace('\n',' '), decisao.replace('"','').replace('\\','').replace('\n',' ')))

def main():
	c = crawler_jurisprudencia_carf()
	c.baixar_jurisprudencia_carf()
	# cursor = cursorConexao()
	# cursor.execute('select id, html_decisoes FROM jurisprudencia_carf.html_decisoes;')
	# counter = 0
	# for id_p, html in cursor.fetchall():
	# 	c.parsear_html(html)

if __name__ == '__main__':
	main()