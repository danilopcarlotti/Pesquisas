import sys, re, os, time, urllib.request, subprocess
from bs4 import BeautifulSoup
from common.conexao_local import cursorConexao
from common.download_path import path
from crawler_jurisprudencia_tj import crawler_jurisprudencia_tj
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class crawler_jurisprudencia_tjac(crawler_jurisprudencia_tj):
	"""Crawler especializado em retornar textos da jurisprudência de segunda instância do Acre"""
	def __init__(self):
		crawler_jurisprudencia_tj.__init__(self)
		self.botao_pesquisar = '//*[@id="pbSubmit"]'
		self.botao_proximo_ini = '//*[@id="paginacaoSuperior-A"]/table/tbody/tr[1]/td[2]/div/a[5]'
		self.botao_proximo = '//*[@id="paginacaoSuperior-A"]/table/tbody/tr[1]/td[2]/div/a[6]'
		self.data_julgamento_inicialXP = '//*[@id="dtJulgamentoInicio"]/input'
		self.data_julgamento_finalXP = '//*[@id="dtJulgamentoFim"]/input'
		self.link_inicial = 'http://esaj.tjac.jus.br/cjsg/resultadoCompleta.do'
		self.link_1_inst = 'https://www.tjac.jus.br/tribunal/administrativo/coger/banco-de-sentencas/'
		self.pesquisa_livre = '//*[@id="iddados.buscaInteiroTeor"]'
		self.tabela_colunas = 'justica_estadual.jurisprudencia_ac (ementas)'

	def download_tj(self, termo = 'a'):
		cursor = cursorConexao()
		driver = webdriver.Chrome(self.chromedriver)
		driver.get(self.link_inicial)
		driver.find_element_by_xpath(self.pesquisa_livre).send_keys(termo)
		driver.find_element_by_xpath(self.botao_pesquisar).click()
		texto = crawler_jurisprudencia_tj.extrai_texto_html(self,(driver.page_source)).replace('"','')
		cursor.execute('INSERT INTO %s value ("%s");' % (self.tabela_colunas,texto))
		driver.find_element_by_xpath(self.botao_proximo_ini).click()
		contador = 0
		while True:
			try:
				time.sleep(1)
				texto = crawler_jurisprudencia_tj.extrai_texto_html(self,(driver.page_source)).replace('"','')
				cursor.execute('INSERT INTO %s value ("%s");' % (self.tabela_colunas,texto))
				driver.find_element_by_xpath(self.botao_proximo).click()
				contador = 0
			except Exception as e:
				print(e)
				contador += 1
				time.sleep(5)
				if contador > 3:
					driver.close()
					break

	def download_1_inst(self):
		req = urllib.request.Request(self.link_1_inst, headers={'User-Agent': 'Mozilla/5.0'})
		html = urllib.request.urlopen(req,timeout=30).read()
		pag = BeautifulSoup(html,'lxml')
		contador = 0
		for l in pag.find_all('a', href=True):
			if re.search(r'https\://www.tjac.jus.br/wp\-content/uploads',l['href']):
				try:
					urllib.request.urlretrieve(l['href'],'TJAC_1_inst_%s.pdf' % str(contador))
					subprocess.Popen('mv TJAC_1_inst_*.pdf %s/ac_1_inst' % (path,), shell=True)
					contador += 1
				except:
					pass

def main():
	c = crawler_jurisprudencia_tjac()

	c.download_1_inst()	

	# print('comecei ',c.__class__.__name__)
	# try:
	# 	c.download_tj()
	# except Exception as e:
	# 	print(e)

if __name__ == '__main__':
	main()