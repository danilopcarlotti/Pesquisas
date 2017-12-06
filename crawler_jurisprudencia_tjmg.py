import sys, re, time, download_path, os
from crawler_jurisprudencia_tj import crawler_jurisprudencia_tj
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from conexao_local import cursorConexao

class crawler_jurisprudencia_tjmg():
	"""Crawler especializado em retornar textos da jurisprudência de segunda instância de Minas Gerais"""
	def __init__(self):
		crawler_jurisprudencia_tj.__init__(self)
		self.link_inicial = 'http://www5.tjmg.jus.br/jurisprudencia/formEspelhoAcordao.do'
		self.pesquisa_livre = '//*[@id="palavras"]'
		self.inteiro_teor = '//*[@id="pesqAcordao"]'
		self.botao_pesquisar = '//*[@id="pesquisaLivre"]'
		self.link_captcha = '//*[@id="captcha_text"]'
		self.data_julgamento_inicialXP = '//*[@id="dataJulgamentoInicial"]'
		self.data_julgamento_finalXP = '//*[@id="dataJulgamentoFinal"]'
		self.link_download_captcha = '/html/body/table/tbody/tr[3]/td/table/tbody/tr[3]/td/a[2]'
		self.tabela_colunas = 'justica_estadual.jurisprudencia_mg (ementas)'

	def delete_audios(self):
		for file in os.listdir(download_path.path+'/'):
			if re.search(r'wav',file):
				os.remove(download_path.path+'/'+file)

	def captcha(self):
		from transcrever_audio import transcrever_audio
		t = transcrever_audio()
		for file in os.listdir(download_path.path+'/'):
			if re.search(r'wav',file):
				return t.transcrever(audio=download_path.path+'/'+file)

	def download_tj(self,data_ini,data_fim):
		self.delete_audios()
		cursor = cursorConexao()
		driver = webdriver.Chrome(self.chromedriver)
		driver.get(self.link_inicial)
		driver.find_element_by_xpath(self.pesquisa_livre).send_keys('direito')
		driver.find_element_by_xpath(self.data_julgamento_inicialXP).send_keys(data_ini)
		driver.find_element_by_xpath(self.data_julgamento_finalXP).send_keys(data_fim)
		driver.find_element_by_xpath(self.botao_pesquisar).click()
		time.sleep(5)
		driver.find_element_by_xpath(self.link_download_captcha).click()
		time.sleep(5)
		driver.find_element_by_xpath(self.link_captcha).send_keys(self.captcha())
		time.sleep(100)
		self.delete_audios()
		# driver.close()

if __name__ == '__main__':
	c = crawler_jurisprudencia_tjmg()
	# rodar pesquisa mês a mês
	c.download_tj('01012017','01022017')
	# print('comecei ',c.__class__.__name__)
	# try:
	# 	for a in c.lista_anos:
	# 		for m in range(len(lista_meses)-1):
	# 			c.download_tj('01'+lista_meses[m]+a,'01'+lista_meses[m+1]+a)

	# 	c.download_tj(1,2)
	# except:
	# 	print('finalizei com erro\n')