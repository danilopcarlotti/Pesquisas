import sys, re, os, time
from crawler_jurisprudencia_tj import crawler_jurisprudencia_tj
from crawlerJus import crawlerJus
from bs4 import BeautifulSoup
from selenium import webdriver
from common.conexao_local import cursorConexao

class crawler_jurisprudencia_tjdf(crawler_jurisprudencia_tj):
	"""Crawler especializado em retornar textos da jurisprudência de segunda instância do Distrito Federal"""
	def __init__(self):
		crawler_jurisprudencia_tj.__init__(self)
		self.link_inicial = 'https://pesquisajuris.tjdft.jus.br/IndexadorAcordaos-web/sistj?visaoId=tjdf.sistj.acordaoeletronico.buscaindexada.apresentacao.VisaoBuscaAcordao&nomeDaPagina=buscaLivre2&buscaPorQuery=1&baseSelecionada=BASE_ACORDAOS&ramoJuridico=&baseDados=[BASE_ACORDAOS,%%20TURMAS_RECURSAIS]&argumentoDePesquisa=a&filtroSegredoDeJustica=false&desembargador=&indexacao=&tipoDeNumero=NumAcordao&tipoDeRelator=TODOS&camposSelecionados=[ESPELHO]&numero=&tipoDeData=DataPublicacao&dataFim=&dataInicio=&ementa=&orgaoJulgador=&filtroAcordaosPublicos=false&legislacao=&numeroDaPaginaAtual=%s&quantidadeDeRegistros=20&totalHits=799443'
		self.tabela_colunas = 'justica_estadual.jurisprudencia_df (ementas)'
		
	def download_tj(self,ultima_pag):
		cursor = cursorConexao()
		for i in range(1,ultima_pag):
			try:
				link = (self.link_inicial % str(i))
				driver = webdriver.Chrome(self.chromedriver)
				driver.get(link)
				lista_acordaos = driver.find_elements_by_id('id_link_abrir_dados_acordao')
				for link_ac in lista_acordaos:
					link_ac.click()
					divs_com_rotulo = driver.find_elements_by_class_name("conteudoComRotulo")
					links_inteiro_teor = divs_com_rotulo[9].find_elements_by_tag_name('span')
					links_inteiro_teor[0].click()
					time.sleep(1)
					driver.find_element_by_id('id_comando_voltar_supra').click()
					return
			except Exception as e:
				print(e)
				return
			


if __name__ == '__main__':
	c = crawler_jurisprudencia_tjdf()
	print('comecei ',c.__class__.__name__)
	try:
		c.download_tj(39973) #número atualizado em dez 2017
	except Exception as e:
		print(e)