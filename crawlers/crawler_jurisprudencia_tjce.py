import sys, re
from crawler_jurisprudencia_tj import crawler_jurisprudencia_tj
from bs4 import BeautifulSoup

class crawler_jurisprudencia_tjce():
	"""Crawler especializado em retornar textos da jurisprudência de segunda instância do Ceará"""
	def __init__(self):
		crawler_jurisprudencia_tj.__init__(self)
		self.link_inicial = 'http://www.tjce.jus.br/institucional/consulta-de-acordao/'
		self.pesquisa_livre = '//*[@id="iddados.buscaInteiroTeor"]'
		self.data_julgamento_inicialXP = '//*[@id="dtJulgamentoInicio"]/input'
		self.data_julgamento_finalXP = '//*[@id="dtJulgamentoFim"]/input'
		self.botao_pesquisar = '//*[@id="pbSubmit"]'
		self.botao_proximo_ini = '//*[@id="paginacaoSuperior-A"]/table/tbody/tr[1]/td[2]/div/a[5]'
		self.botao_proximo = '//*[@id="paginacaoSuperior-A"]/table/tbody/tr[1]/td[2]/div/a[6]'
		self.tabela_colunas = 'justica_estadual.jurisprudencia_ce (ementas)'

if __name__ == '__main__':
	c = crawler_jurisprudencia_tjce()
	print('comecei ',c.__class__.__name__)
	try:
		for l in range(len(c.lista_anos)):
			print(c.lista_anos[l],'\n')
			try:
				crawler_jurisprudencia_tj.download_tj_ESAJ_recaptcha(c,crawler_jurisprudencia_tj,'0101'+c.lista_anos[l],'3112'+c.lista_anos[l],termo='processo')
			except Exception as e:
				print(e)
	except Exception as e:
		print('finalizei o ano com erro ',e)