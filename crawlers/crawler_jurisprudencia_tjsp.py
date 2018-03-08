import sys, re, os, time, subprocess
from bs4 import BeautifulSoup
from common.conexao_local import cursorConexao
from common.download_path import path
from common.image_to_txt import image_to_txt
from common_nlp.pdf_to_text import pdf_to_text
from crawler_jurisprudencia_tj import crawler_jurisprudencia_tj
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from common_nlp.textNormalization import textNormalization

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
		self.tabela_colunas_1_inst = 'justica_estadual.jurisprudencia_sp_1_inst (sentencas)'
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
		except Exception as e:
			print(e)
			return False
	
	def download_1_inst(self,data_ini, data_fim, termo = 'a'):
		botao_proximo = '//*[@id="resultados"]/table[1]/tbody/tr[1]/td[2]/div/a[6]'
		botao_proximo_ini = '//*[@id="resultados"]/table[1]/tbody/tr[1]/td[2]/div/a[5]'
		data_ini_xpath = '//*[@id="iddadosConsulta.dtInicio"]'
		data_fim_xpath = '//*[@id="iddadosConsulta.dtFim"]'
		link = 'https://esaj.tjsp.jus.br/cjpg/pesquisar.do'
		pesquisa_xpath = '//*[@id="iddadosConsulta.pesquisaLivre"]'
		cursor = cursorConexao()
		driver = webdriver.Chrome(self.chromedriver)
		driver.get(link)
		driver.find_element_by_xpath(pesquisa_xpath).send_keys('a')
		driver.find_element_by_xpath(data_ini_xpath).send_keys(data_ini)
		driver.find_element_by_xpath(data_fim_xpath).send_keys(data_fim)
		driver.find_element_by_xpath(self.botao_pesquisar).click()
		time.sleep(1)
		texto = crawler_jurisprudencia_tj.extrai_texto_html(self,(driver.page_source)).replace('"','')
		cursor.execute('INSERT INTO %s value ("%s");' % (self.tabela_colunas_1_inst,texto))
		driver.find_element_by_xpath(botao_proximo_ini).click()
		time.sleep(1)
		texto = crawler_jurisprudencia_tj.extrai_texto_html(self,(driver.page_source)).replace('"','')
		cursor.execute('INSERT INTO %s value ("%s");' % (self.tabela_colunas_1_inst,texto))
		contador = 3
		while contador:
			try:
				driver.find_element_by_xpath(botao_proximo).click()
				time.sleep(1)
				texto = crawler_jurisprudencia_tj.extrai_texto_html(self,(driver.page_source)).replace('"','')
				cursor.execute('INSERT INTO %s value ("%s");' % (self.tabela_colunas_1_inst,texto))
				contador = 3
			except:
				time.sleep(2)
				contador -= 1
		driver.close()

	def download_acordao_sp(self,dados_baixar):
		crawler_jurisprudencia_tj.download_pdf_acordao_captcha_image(self,dados_baixar,'//*[@id="valorCaptcha"]','//*[@id="pbEnviar"]',self.capture_image)
		subprocess.Popen('mv %s/sp_2_inst_*.pdf %s/sp_2_inst' % (path,path), shell=True)

	def parse_sp_dados_1_inst(self,texto):
		inicio = False
		texto_sentenca = ''
		for line in texto.split('\n'):
			line += '\n'
			if inicio:
				if re.search(r'^\s*?\d+\s*?\-\s*?$',line):
					# Novo início, finalizar o anterior
					try:
						dados_re = r'\s*?{}\:.*?\n(.*?)\n'
						assunto = re.search(dados_re.format('Assunto'), texto_sentenca)
						assunto = assunto.group(1)
						classe = re.search(dados_re.format('Classe'), texto_sentenca)
						classe = classe.group(1)
						comarca = re.search(dados_re.format('Comarca'), texto_sentenca)
						comarca = comarca.group(1)
						data_disponibilizacao = re.search(r'\s*?Data de Disponibilização\:.*?\n(.*?)\n', texto_sentenca)
						data_disponibilizacao = data_disponibilizacao.group(1)
						foro = re.search(dados_re.format('Foro'), texto_sentenca)
						foro = foro.group(1)
						juiz = re.search(dados_re.format('Magistrad.'), texto_sentenca)
						juiz = juiz.group(1)
						numero = re.search(r'\d{7}\-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}', texto_sentenca, re.DOTALL)
						numero = numero.group(0)
						requerente = re.search(r'\s*?Requerent.*?\:.*?\n.*?\n(.*?)\n', texto_sentenca)
						requerente = requerente.group(1)
						requerido = re.search(r'\s*?Requerid.*?\:.*?\n.*?\n(.*?)\n', texto_sentenca)
						requerido = requerido.group(1)
						if re.search(r'Justiça Gratuita',texto_sentenca,re.I):
							justica_gratuita = '1'
						else:
							justica_gratuita = '0'
						# FALTA:
							# PROCEDÊNCIA;
							# PARTES DO TEXTO (relatório, fundamentação e dispositivo)
						print(assunto.strip(),classe.strip(),comarca.strip(),data_disponibilizacao.strip(),foro.strip(),juiz.strip(),numero.strip(),requerente.strip(),requerido.strip(),print(justica_gratuita))
						# INSERIR NA BASE DE DADOS
					except Exception as e:
						print(e)
					texto_sentenca = ''
				else:
					texto_sentenca += line
			else:
				if re.search(r'^\s*?\d+\s*?\-\s*?$',line):
					inicio = True

	def parse_sp_pdf(self,lista_arquivos = None):
		if not lista_arquivos:
			lista_arquivos = os.listdir(path+'/sp_2_inst')
		p = pdf_to_text()
		dados = []
		for arq in lista_arquivos:
			try:
				if re.search(r'\.pdf',arq):
					id_arq = arq.split('sp_2_inst_')
					id_arq = id_arq[1][:-4]
					texto = p.convert_pdfminer(path+'/sp_2_inst/'+arq)
					# numero,data_julgamento = self.parse_sp_dados_1_inst(texto)
					dados.append(texto,numero,data_julgamento)
			except Exception as e:
				print(arq)
				print(e)
		return dados

def main():
	c = crawler_jurisprudencia_tjsp()

	# arq = open('ex.txt','r')
	# for line in arq:
	# 	texto.append(line)
	c.parse_sp_dados_1_inst(texto)


	# print('comecei ',c.__class__.__name__)
	# try:
	# 	for l in range(len(c.lista_anos)):
	# 		print(c.lista_anos[l],'\n')
	# 		for m in range(len(c.lista_meses)):
	# 			try:
	# 				c.download_1_inst('01'+c.lista_meses[m]+c.lista_anos[l],'28'+c.lista_meses[m]+c.lista_anos[l])
	# 			except Exception as e:
	# 				print(e)
	# except Exception as e:
	# 	print(e)

	# cursor = cursorConexao()
	# cursor.execute('SELECT id,ementas from justica_estadual.jurisprudencia_sp limit 10;')
	# lista_links = cursor.fetchall()
	# c.download_acordao_sp(lista_links)

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