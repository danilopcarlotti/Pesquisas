import sys, re, time, common.download_path, os
from crawler_jurisprudencia_tj import crawler_jurisprudencia_tj
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from common.conexao_local import cursorConexao

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
		self.botao_proximo_XP = '//*[@id="sistema"]/div/table/tbody/tr/td/table/tbody/tr/td/div/table[11]/tbody/tr[2]/td/table[1]/tbody/tr/td[12]/a'
		self.link_download_captcha = '/html/body/table/tbody/tr[3]/td/table/tbody/tr[3]/td/a[2]'
		self.tabela_colunas = 'justica_estadual.jurisprudencia_mg (ementas)'

	def delete_audios(self):
		for file in os.listdir(common.download_path.path+'/'):
			if re.search(r'wav',file):
				os.remove(common.download_path.path+'/'+file)

	def captcha(self):
		from common.transcrever_audio import transcrever_audio
		t = transcrever_audio()
		for file in os.listdir(common.download_path.path+'/'):
			if re.search(r'wav',file):
				return t.transcrever(audio=common.download_path.path+'/'+file)

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
		self.delete_audios()
		while True:
			try:
				time.sleep(2)
				texto = crawler_jurisprudencia_tj.extrai_texto_html(self,(driver.page_source).replace('"',''))
				cursor.execute('INSERT INTO %s value ("%s");' % (self.tabela_colunas,texto))
				driver.find_element_by_xpath(self.botao_proximo_XP).click()
			except Exception as e:
				print(e)
				if input('ajude-me'):
					pass
		driver.close()

if __name__ == '__main__':
	c = crawler_jurisprudencia_tjmg()
	print('comecei ',c.__class__.__name__)
	try:
		for a in c.lista_anos:
			for m in range(len(c.lista_meses)):
				c.download_tj('01'+c.lista_meses[m]+a,'14'+c.lista_meses[m]+a)
				c.download_tj('15'+c.lista_meses[m]+a,'28'+c.lista_meses[m]+a)
	except:
		print('finalizei com erro\n')