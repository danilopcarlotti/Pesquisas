import sys, re, urllib.request, subprocess, os
from bs4 import BeautifulSoup
from common.download_path import path, path_hd
from crawler_jurisprudencia_tj import crawler_jurisprudencia_tj
from crawlerJus import crawlerJus

class crawler_jurisprudencia_tjpe(crawler_jurisprudencia_tj):
	"""Crawler especializado em retornar textos da jurisprudência de segunda instância de Rio Grande do Norte"""
	def __init__(self):
		crawler_jurisprudencia_tj.__init__(self)
		self.link_inicial = 'http://www.tjpe.jus.br/consultajurisprudenciaweb/xhtml/consulta/consulta.xhtml'
		self.pesquisa_livre = '//*[@id="formPesquisaJurisprudencia:inputBuscaSimples"]'
		self.data_julgamento_inicial = '//*[@id="formPesquisaJurisprudencia:j_id59InputDate"]'
		self.data_julgamento_final = '//*[@id="formPesquisaJurisprudencia:j_id61InputDate"]'
		self.botao_pesquisar = '//*[@id="formPesquisaJurisprudencia"]/div[5]/div/a[1]'

	def download_diario_retroativo(self):
		link_inicial = 'http://www.tjpe.jus.br/dje/DownloadServlet?dj=DJ%s_%s-ASSINADO.PDF&statusDoDiario=ASSINADO'
		for l in range(len(self.lista_anos)):
			for i in range(240,0,-1):
				try:
					response = urllib.request.urlopen(link_inicial % (str(i),self.lista_anos[l]),timeout=15)
					file = open(str(i)+self.lista_anos[l]+'.pdf', 'wb')
					file.write(response.read())
					file.close()
					subprocess.Popen('mv %s/*.pdf "%s/Diarios_pe"' % (os.getcwd(),path_hd), shell=True)
				except Exception as e:
					print(e)

if __name__ == '__main__':
	c = crawler_jurisprudencia_tjpe()
	c.download_diario_retroativo()