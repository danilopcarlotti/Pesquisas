import time, datetime, urllib.request,logging, click, os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re

class crawlerJus(object):
	"""Classe contendo métodos auxiliares para cralwer"""
	def __init__(self):
		data = datetime.date.today().strftime("%Y%m%d")
		self.ano = data[:4]
		self.mes = data[4:6]
		self.dia = data[6:]
		if len(self.dia)==1:
		    self.dia = "0" + self.dia
		self.cwd = os.getcwd()
		logging.basicConfig(filename=self.cwd+'/publicacoes_'+self.dia+self.mes+self.ano+'.log',level=logging.INFO)
		self.chromedriver = self.cwd+"/chromedriver"
		os.environ["webdriver.chrome.driver"] = self.chromedriver

	def baixa_pag(self,link):
		for i in range(3):
			try:
				req = urllib.request.Request(link, headers={'User-Agent': 'Mozilla/5.0'})
				html = urllib.request.urlopen(req,timeout=5).read()
				return html
			except:
				pass
		return ''

	def baixa_diario(self,f):
	    cont = 0
	    while (cont < 4):
	        try:
	            f()
	            cont = 4
	        except:
	            cont += 1

	def baixa_texto_html(self,link):
		html = self.baixa_pag(link)
		soup = BeautifulSoup(html,'lxml')
		for script in soup(["script", "style"]):
			script.extract()
		return soup.get_text()

	def encontrar_links_html(self, link, links_baixar, re_href):
		pag = BeautifulSoup(self.baixa_pag(link),'lxml')
		for l in pag.find_all('a', href=True):
			if re.search(re_href,l['href']):
				links_baixar.append(l['href'])
	
	def executa_funcao(self,f,msg):
		for i in range(5):
			try:
				f()
				return True
			except:
				pass
		logging.info(msg+'\n')

	def baixa_html_pdf(self,link,nome_arq):
		response = urllib.request.urlopen(link,timeout=5)
		file = open(self.dia+self.mes+self.ano+'_'+nome_arq+".pdf", 'wb')
		file.write(response.read())
		time.sleep(5)
		file.close()

	def driver_open_xpath(self,link,lista_xpaths):
		driver = webdriver.Chrome(self.chromedriver)
		driver.get(link)
		for x in lista_xpaths:
			driver.find_element_by_xpath(x).click()
		time.sleep(5)
		driver.close()

	def baixaEsaj(self,inicio, fim, pag):
		xPath= "//*[@id=\"cadernosCad\"]/option[%s]"
		for i in range(inicio,fim):
			driver = webdriver.Chrome(self.chromedriver)
			driver.get(pag)
			driver.find_element_by_xpath(xPath % str(int(i))).click()	
			driver.find_element_by_xpath("//*[@id=\"download\"]").click()
			time.sleep(5)
			driver.close()

	def mes_nome_numero(self,texto):
		texto = texto.lower()
		if texto == 'janeiro':
			return '01'
		elif texto == 'fevereiro':
			return '02'
		elif texto == 'março':
			return '03'
		elif texto == 'abril':
			return '04'
		elif texto == 'maio':
			return '05'
		elif texto == 'junho':
			return '06'
		elif texto == 'julho':
			return '07'
		elif texto == 'agosto':
			return '08'
		elif texto == 'setembro':
			return '09'
		elif texto == 'outubro':
			return '10'
		elif texto == 'novembro':
			return '09'
		elif texto == 'dezembro':
			return '12'

#comandos: gera relatório, pesquisa tribunal específico

class object1():
	"""docstring for ClassName"""
	def __init__(self):
		crawlerJus.__init__(self)
		pass
		