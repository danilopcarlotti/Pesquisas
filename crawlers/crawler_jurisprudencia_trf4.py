import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from crawler_jurisprudencia_tj import crawler_jurisprudencia_tj
from common.conexao_local import cursorConexao

class crawler_jurisprudencia_trf4():
	"""Crawler especializado em retornar textos da jurisprudência do tribunal regional federal da quarta região"""
	def __init__(self):
		crawler_jurisprudencia_tj.__init__(self)
		self.link_inicial = 'https://jurisprudencia.trf4.jus.br/pesquisa/pesquisa.php'
		self.botao_pesquisar = '//*[@id="frmPesquisar"]/table/tbody/tr[13]/td[2]/table/tbody/tr/td/input[1]'
		self.botao_prox = '//*[@id="sbmProximaPagina"]'
		self.data_inicial_xpath = '//*[@id="dataIni"]'
		self.data_final_xpath = '//*[@id="dataFim"]'
		self.link_resultado_xpath = '//*[@id="parcial"]'
		self.pesquisa_livre = '//*[@id="textoPesqLivre"]'
		self.tabela_colunas = 'justica_federal.jurisprudencia_trf4 (ementas)'

	def download_trf4(self, data_ini, data_fim, termo = 'recurso'):
		cursor = cursorConexao()
		driver = webdriver.Chrome(self.chromedriver)
		driver.get(self.link_inicial)
		time.sleep(1)
		driver.find_element_by_xpath(self.pesquisa_livre).send_keys(termo)
		driver.find_element_by_xpath(self.data_inicial_xpath).send_keys(data_ini)
		driver.find_element_by_xpath(self.data_final_xpath).send_keys(data_fim)
		driver.find_element_by_xpath(self.botao_pesquisar).click()
		time.sleep(1)
		try:
			driver.find_element_by_xpath(self.link_resultado_xpath).click()
			time.sleep(1)
		except:
			pass
		time.sleep(1)
		texto = crawler_jurisprudencia_tj.extrai_texto_html(self,(driver.page_source)).replace('"','')
		cursor.execute('INSERT INTO %s value ("%s");' % (self.tabela_colunas,texto))
		try:
			driver.find_element_by_xpath(self.botao_prox)
		except:
			driver.close()
			return
		contador = 0
		while True:
			try:
				time.sleep(1)
				texto = crawler_jurisprudencia_tj.extrai_texto_html(self,(driver.page_source)).replace('"','')
				cursor.execute('INSERT INTO %s value ("%s");' % (self.tabela_colunas,texto))
				driver.find_element_by_xpath(self.botao_prox % self.botao_prox_outros)
				contador = 0
			except Exception as e:
				print(e)
				contador += 1
				time.sleep(5)
				if contador > 3:
					driver.close()
					break
		driver.close()

if __name__ == '__main__':
	c = crawler_jurisprudencia_trf4()
	try:
		for l in range(len(c.lista_anos)):
			print(c.lista_anos[l],'\n')
			for m in range(len(c.lista_meses)):
				for i in range(1,9):
					try:
						c.download_trf4('0'+str(i)+c.lista_meses[m]+c.lista_anos[l],'0'+str(i+1)+c.lista_meses[m]+c.lista_anos[l])
					except Exception as e:
						print(e)		
				for i in range(10,27):
					try:
						c.download_trf4(str(i)+c.lista_meses[m]+c.lista_anos[l],str(i+1)+c.lista_meses[m]+c.lista_anos[l])
					except Exception as e:
						print(e)
	except Exception as e:
		print(e)