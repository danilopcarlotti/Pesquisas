import sys, re, os, time, urllib.request,common.download_path
from bs4 import BeautifulSoup
from common.image_to_txt import image_to_txt
from crawler_jurisprudencia_tj import crawler_jurisprudencia_tj
from common.conexao_local import cursorConexao
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class crawler_jurisprudencia_tjsp(crawler_jurisprudencia_tj):
	"""Crawler especializado em retornar textos da jurisprudência de segunda instância de São Paulo"""
	def __init__(self):
		crawler_jurisprudencia_tj.__init__(self)
		self.link_inicial = 'https://esaj.tjsp.jus.br/cjsg/consultaCompleta.do'
		self.pesquisa_livre = '//*[@id="iddados.buscaInteiroTeor"]'
		self.data_julgamento_inicialXP = '//*[@id="iddados.dtJulgamentoInicio"]'
		self.data_julgamento_finalXP = '//*[@id="iddados.dtJulgamentoFim"]'
		self.botao_pesquisar = '//*[@id="pbSubmit"]'
		self.botao_proximo_ini = '//*[@id="paginacaoSuperior-A"]/table/tbody/tr[1]/td[2]/div/a[5]'
		self.botao_proximo = '//*[@id="paginacaoSuperior-A"]/table/tbody/tr[1]/td[2]/div/a[6]'
		self.tabela_colunas = 'justica_estadual.jurisprudencia_sp (ementas)'
		self.link_esaj = 'https://esaj.tjsp.jus.br/cjsg/getArquivo.do?cdAcordao=%s&cdForo=%s'

	def capture_image(self, driver):
		driver.get('https://esaj.tjsp.jus.br/cjsg/getArquivo.do?cdAcordao=5177907&cdForo=0')
		time.sleep(2)
		source = driver.page_source
		try:
			captcha_image = re.search(r'url\(&quot\;(.*?)&quot',source,re.I | re.DOTALL).group(1)
			urllib.request.urlretrieve(captcha_image,'imagem.png')
			i = image_to_txt()
			return i.captcha_image_to_txt()
		except:
			return False
		
	def download_acordao_sp(self,id_acordao,link):
		# crawler_jurisprudencia_tj.download_pdf_acordao_captcha_audio(self,link,'//*[@id="valorCaptcha"]','//*[@id="captchaInfo"]/ul/li[1]/a','//*[@id="pbEnviar"]','sp_2_inst_' + id_acordao)
		crawler_jurisprudencia_tj.download_pdf_acordao_captcha_image(self,link,'//*[@id="valorCaptcha"]','//*[@id="pbEnviar"]','sp_2_inst_teste' + id_acordao,self.capture_image)
		subprocess.Popen('mv %s/to_2_inst_* %s/acordaos_tj_to' % (path,path), shell=True)
	

def main():
	c = crawler_jurisprudencia_tjsp()
	cursor = cursorConexao()
	cursor.execute('SELECT id,ementas from justica_estadual.jurisprudencia_sp where id > 45079 limit 10000000;')
	lista_links = cursor.fetchall()
	for i,l in lista_links:
		c.download_acordao_sp(str(i),l)

	# print('comecei ',c.__class__.__name__)
	# try:
	# 	for l in range(len(c.lista_anos)):
	# 		print(c.lista_anos[l],'\n')
	# 		for m in range(len(c.lista_meses)):
	# 			try:
	# 				crawler_jurisprudencia_tj.download_tj_ESAJ(c,crawler_jurisprudencia_tj,'01'+c.lista_meses[m]+c.lista_anos[l],'28'+c.lista_meses[m]+c.lista_anos[l],termo='a')
	# 			except Exception as e:
	# 				print(e)
	# except Exception as e:
	# 	print('finalizei o ano com erro ',e)

if __name__ == '__main__':
	main()