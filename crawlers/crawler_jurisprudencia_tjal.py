import sys, re, os, urllib.request, time, subprocess
from common.download_path import path
from crawler_jurisprudencia_tj import crawler_jurisprudencia_tj
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class crawler_jurisprudencia_tjal(crawler_jurisprudencia_tj):
	"""Crawler especializado em retornar textos da jurisprudência de segunda instância de Alagoas"""
	def __init__(self):
		crawler_jurisprudencia_tj.__init__(self)
		self.link_inicial = 'https://www2.tjal.jus.br/cjsg/consultaCompleta.do'
		self.pesquisa_livre = '//*[@id="iddados.buscaInteiroTeor"]'
		self.data_julgamento_inicialXP = '//*[@id="iddados.dtJulgamentoInicio"]'
		self.data_julgamento_finalXP = '//*[@id="iddados.dtJulgamentoFim"]'
		self.botao_pesquisar = '//*[@id="pbSubmit"]'
		self.botao_proximo_ini = '//*[@id="paginacaoSuperior-A"]/table/tbody/tr[1]/td[2]/div/a[5]'
		self.botao_proximo = '//*[@id="paginacaoSuperior-A"]/table/tbody/tr[1]/td[2]/div/a[6]'
		self.tabela_colunas = 'justica_estadual.jurisprudencia_al (ementas)'

	def download_1_inst(self):
		botao_proximo_ini = 2
		botao_proximo = '//*[@id="pn_%s"]'
		botao_xpath = '//*[@id="corpo_texto"]/div/div/div/form/button'
		driver = webdriver.Chrome(self.chromedriver)
		link = 'http://www.tjal.jus.br/corregedoria/?pag=sentencas'
		re_href = r'http\://www.intranet.tjal.jus.br/bancodesentencas/arquivos/'
		texto_xpath = '//*[@id="corpo_texto"]/div/div/div/form/input'
		driver.get(link)
		driver.find_element_by_xpath(texto_xpath).send_keys('a ou não a')
		driver.find_element_by_xpath(botao_xpath).click()
		time.sleep(1)
		contador = 0
		loop_counter = 0
		while True:
			try:
				soup = BeautifulSoup(driver.page_source,'html.parser')
				for l in soup.find_all('a', href=True):
					if re.search(re_href,l['href']):
						urllib.request.urlretrieve(l['href'],'TJAL_1_inst_%s.pdf' % str(contador))
						subprocess.Popen('mv TJAL_1_inst_*.pdf %s/al_1_inst' % (path,), shell=True)
						contador += 1
				try:
					driver.find_element_by_xpath(botao_proximo % str(botao_proximo_ini)).click()
				except:
					botao_proximo_ini += 1
					driver.find_element_by_xpath(botao_proximo % str(botao_proximo_ini)).click()
				loop_counter = 0
			except Exception as e:
				if loop_counter > 2:
					break
				loop_counter += 1
				print(e)


def main():
	c = crawler_jurisprudencia_tjal()
	c.download_1_inst()
	# print('comecei ',c.__class__.__name__)
	# for l in c.lista_anos:
	# 	try:
	# 		print(l,'\n')
	# 		crawler_jurisprudencia_tj.download_tj_ESAJ_recaptcha(c,crawler_jurisprudencia_tj,'01/01/'+l,'31/12/'+l)
	# 	except Exception as e:
	# 		print('finalizei o ano ',l)
	# 		print(e)

if __name__ == '__main__':
	main()