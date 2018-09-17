from bs4 import BeautifulSoup
from common.download_path import path
from crawler_jurisprudencia_tj import crawler_jurisprudencia_tj
from crawlerJus import crawlerJus
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from common.conexao_local import cursorConexao
import sys, re, time, os, urllib.request, subprocess

sys.path.append(os.path.dirname(os.getcwd()))
from common_nlp.parse_texto import busca

class crawler_jurisprudencia_tjrs():
	"""Crawler especializado em retornar textos da jurisprudência de segunda instância do Rio Grande do Sul"""
	def __init__(self):
		crawler_jurisprudencia_tj.__init__(self)
		self.link_inicial = 'http://www.tjrs.jus.br/busca/?tb=jurisnova&partialfields=tribunal%3ATribunal%2520de%2520Justi%25C3%25A7a%2520do%2520RS.(TipoDecisao%3Aac%25C3%25B3rd%25C3%25A3o|TipoDecisao%3Amonocr%25C3%25A1tica|TipoDecisao:null)&t=s&pesq=ementario.#main_res_juris'
		self.pesquisa_livre = '//*[@id="q"]'
		self.botao_pesquisar = '//*[@id="conteudo"]/form/div[1]/div/div/input'
		self.botao_proximo_iniXP = '//*[@id="main_res_juris"]/div/div[2]/span[1]/a'
		self.botao_proximoXP = '//*[@id="main_res_juris"]/div/div[2]/span[3]/a'
		self.data_iniXP = '//*[@id="%s1"]'
		self.data_fimXP = '//*[@id="%s2"]'
		self.tabela_colunas = 'justica_estadual.jurisprudencia_rs (ementas)'

	def download_diario_retroativo(self):
		link_inicial = 'http://www3.tjrs.jus.br/servicos/diario_justica/download_edicao.php?tp=%s&ed=%s'
		edicoes = ['0','5','7','6']
		for i in range(6298,0,-1):
			for e in edicoes:
				try:
					print(link_inicial % (e,str(i)))
					response = urllib.request.urlopen(link_inicial % (e,str(i)),timeout=15)
					file = open(str(i)+'_'+e+'.pdf', 'wb')
					file.write(response.read())
					file.close()
					subprocess.Popen('mv %s/*.pdf %s/Diarios_rs' % (os.getcwd(),path), shell=True)
				except Exception as e:
					print(e)

	def download_tj(self,data_ini,data_fim, termo='a'):
		cursor = cursorConexao()
		driver = webdriver.Chrome(self.chromedriver)
		driver.get(self.link_inicial)
		time.sleep(1)
		driver.find_element_by_xpath(self.pesquisa_livre).send_keys(termo)
		driver.find_element_by_xpath(self.data_iniXP % 'dia').send_keys(data_ini[:2])
		driver.find_element_by_xpath(self.data_iniXP % 'mes').send_keys(data_ini[2:4])
		driver.find_element_by_xpath(self.data_iniXP % 'ano').send_keys(data_ini[4:])
		driver.find_element_by_xpath(self.data_fimXP % 'dia').send_keys(data_fim[:2])
		driver.find_element_by_xpath(self.data_fimXP % 'mes').send_keys(data_fim[2:4])
		driver.find_element_by_xpath(self.data_fimXP % 'ano').send_keys(data_fim[4:])
		time.sleep(1)
		driver.find_element_by_xpath(self.botao_pesquisar).click()
		links_inteiro_teor = driver.find_elements_by_link_text('html')
		for l in links_inteiro_teor:
			try:
				texto = l.get_attribute('href')
				cursor.execute('INSERT INTO %s value ("%s");' % (self.tabela_colunas,texto))		
			except:
				driver.close()
				return
		try:
			driver.find_element_by_xpath(self.botao_proximo_iniXP).click()
		except:
			driver.close()
			return
		while True:
			time.sleep(1)
			links_inteiro_teor = driver.find_elements_by_link_text('html')
			for l in links_inteiro_teor:
				try:
					texto = l.get_attribute('href')
					cursor.execute('INSERT INTO %s value ("%s");' % (self.tabela_colunas,texto))		
				except:
					pass
			try:
				driver.find_element_by_xpath(self.botao_proximoXP).click()
			except:
				driver.close()
				return

	def parser_acordaos(self,links):
		cursor = cursorConexao()
		crawler = crawlerJus()
		contador = 1
		for id_p, link in links:
			try:
				texto = crawler.baixa_texto_html(link).strip().replace('\\','').replace('/','').replace('"','')
				if texto != '':
					numero = busca(r'\n?Nº\s*?(.*?)\n', texto)
					cursor.execute('INSERT INTO jurisprudencia_2_inst.jurisprudencia_2_inst (numero, texto_decisao) values ("%s","%s");' % (numero, texto))
				print(contador)
				contador += 1
			except Exception as e:
				print(id_p,e)

if __name__ == '__main__':
	c = crawler_jurisprudencia_tjrs()

	# c.download_diario_retroativo()

	# print('comecei ',c.__class__.__name__)
	# try:
	# 	for l in range(len(c.lista_anos)):
	# 		print(c.lista_anos[l],'\n')
	# 		for m in range(len(c.lista_meses)):
	# 			for i in range(1,8):
	# 				try:
	# 					c.download_tj('0'+str(i)+c.lista_meses[m]+c.lista_anos[l],'0'+str(i+1)+c.lista_meses[m]+c.lista_anos[l])
	# 				except Exception as e:
	# 					print(e)		
	# 			for i in range(10,30):
	# 				try:
	# 					c.download_tj(str(i)+c.lista_meses[m]+c.lista_anos[l],str(i+1)+c.lista_meses[m]+c.lista_anos[l])
	# 				except Exception as e:
	# 					print(e)
	# except Exception as e:
	# 	print('finalizei o ano com erro ',e)

	cursor = cursorConexao()

	cursor.execute('SELECT id, ementas from justica_estadual.jurisprudencia_rs;')
	links = cursor.fetchall()
	c.parser_acordaos(links)

		

