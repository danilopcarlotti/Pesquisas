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
				texto = crawlerJus.baixa_pag(self,link)
				cursor.execute('INSERT INTO %s value ("%s");' % (self.tabela_colunas,texto))
			except Exception as e:
				print(e)
			


if __name__ == '__main__':
	c = crawler_jurisprudencia_tjdf()
	print('comecei ',c.__class__.__name__)
	try:
		c.download_tj(39973) #número atualizado em dez 2017
	except Exception as e:
		print(e)