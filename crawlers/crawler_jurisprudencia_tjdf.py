import sys, re, os, time
from crawler_jurisprudencia_tj import crawler_jurisprudencia_tj
from bs4 import BeautifulSoup
from selenium import webdriver
from common.conexao_local import cursorConexao

class crawler_jurisprudencia_tjdf():
	"""Crawler especializado em retornar textos da jurisprudência de segunda instância do Distrito Federal"""
	def __init__(self):
		crawler_jurisprudencia_tj.__init__(self)
		self.link_inicial = 'https://pesquisajuris.tjdft.jus.br/IndexadorAcordaos-web/sistj?visaoId=tjdf.sistj.acordaoeletronico.buscaindexada.apresentacao.VisaoBuscaAcordao'
		self.pesquisa_livre = 'argumentoDePesquisa'
		self.data_julgamento_inicialID = 'dataInicio'
		self.data_julgamento_finalID = 'dataFim'
		self.botao_pesquisar = 'id_comando_pesquisar'
		self.botao_pesquisar_todosXP = '//*[@id="69ff9084675c6d7cd21768d56d517ab85aa46e39"]'
		self.botao_proximoID = 'btproximaPagina'
		self.texto_pesquisa = 'a'
		self.tabela_colunas = 'justica_estadual.jurisprudencia_df (ementas)'
		
	def download_tj(self,data_ini,data_fim):
		cursor = cursorConexao()
		driver = webdriver.Chrome(self.chromedriver)
		driver.get(self.link_inicial)
		driver.find_element_by_id(self.pesquisa_livre).send_keys(self.texto_pesquisa)
		driver.find_element_by_id(self.data_julgamento_inicialID).send_keys(data_ini)
		driver.find_element_by_id(self.data_julgamento_finalID).send_keys(data_fim)
		driver.find_element_by_id(self.botao_pesquisar).click()
		driver.find_element_by_xpath(self.botao_pesquisar_todosXP).click()
		loop_counter = 0
		while True:
			try:
				texto = crawler_jurisprudencia_tj.extrai_texto_html(self,(driver.page_source).replace('"',''))
				cursor.execute('INSERT INTO %s value ("%s");' % (self.tabela_colunas,texto))
				driver.find_element_by_id(self.botao_proximoID).click()
				time.sleep(2)
			except:
				loop_counter += 1
				time.sleep(5)
				if loop_counter > 3:
					break
		driver.close()

if __name__ == '__main__':
	c = crawler_jurisprudencia_tjdf()
	print('comecei ',c.__class__.__name__)
	for l in c.lista_anos:
		try:
			print(l,'\n')
			c.download_tj('01/01/'+l,'31/12/'+l)
		except:
			print('finalizei com erro\n')