from bs4 import BeautifulSoup
from common.conexao_local import cursorConexao
from crawler_jurisprudencia_tj import crawler_jurisprudencia_tj
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from common.conexao_local import cursorConexao
import sys, re, time, os

sys.path.append(os.path.dirname(os.getcwd()))
from common_nlp.parse_texto import busca

class crawler_jurisprudencia_tjrn():
	"""Crawler especializado em retornar textos da jurisprudência de segunda instância de Rio Grande do Norte"""
	def __init__(self):
		crawler_jurisprudencia_tj.__init__(self)
		self.link_inicial = 'http://esaj.tjrn.jus.br/cjosg/'
		self.pesquisa_livre = '/html/body/table[4]/tbody/tr/td/table[2]/tbody/tr[1]/td/div/form/table/tbody/tr/td/table/tbody/tr[1]/td[3]/input'
		self.data_julgamento_inicialXP = '/html/body/table[4]/tbody/tr/td/table[2]/tbody/tr[1]/td/div/form/table/tbody/tr/td/table/tbody/tr[7]/td[3]/table/tbody/tr/td[1]/input'
		self.data_julgamento_finalXP = '/html/body/table[4]/tbody/tr/td/table[2]/tbody/tr[1]/td/div/form/table/tbody/tr/td/table/tbody/tr[7]/td[3]/table/tbody/tr/td[3]/input'
		self.botao_pesquisar = '/html/body/table[4]/tbody/tr/td/table[2]/tbody/tr[1]/td/div/form/table/tbody/tr/td/table/tbody/tr[9]/td[3]/input[1]'
		self.botao_proximo = '/html/body/table[4]/tbody/tr/td/table/tbody/tr/td/table[1]/tbody/tr/td/input[2]'
		self.tabela_colunas = 'justica_estadual.jurisprudencia_rn (ementas)'

	def download_diario_retroativo(self):
		# 240 diários por ano. Salvo 2018, que tem, atualmente 121

		link_inicial = 'https://diario.tjrn.jus.br/djonline/pages/repositoriopdfs/%s/%stri/%s/%s_JUD.pdf'
		datas = []
		for l in range(len(self.lista_anos)):
			for i in range(1,10):
				for j in range(1,10):
					datas.append(self.lista_anos[l]+'0'+str(i)+'0'+str(j))
				for j in range(10,32):
					datas.append(self.lista_anos[l]+'0'+str(i)+str(j))
			for i in range(11,13):
				for j in range(1,10):
					datas.append(self.lista_anos[l]+str(i)+'0'+str(j))
				for j in range(10,32):
					datas.append(self.lista_anos[l]+str(i)+str(j))
		for data in datas:
			ano = data[:4]
			mes = data[4:6]
			dia = data[6:]
			try:
				tri = '1'
				if int(mes) > 3 and int(mes) < 7:
					tri = '2'
				elif int(mes) > 6 and int(mes) < 10:
					tri = '3'
				elif int(mes) > 9:
					tri = '4'
				print(link_inicial % (ano,tri,data,data))
				response = urllib.request.urlopen(link_inicial % (ano,tri,data,data),timeout=15)
				file = open(data+'.pdf', 'wb')
				file.write(response.read())
				file.close()
				subprocess.Popen('mv %s/*.pdf %s/Diarios_rn' % (os.getcwd(),path), shell=True)
			except Exception as e:
				print(e)



	def download_tj(self,data_ini,data_fim,termo):
		cursor = cursorConexao()
		driver = webdriver.Chrome(self.chromedriver)
		driver.get(self.link_inicial)
		driver.find_element_by_xpath(self.pesquisa_livre).send_keys(termo)
		driver.find_element_by_xpath(self.data_julgamento_inicialXP).send_keys(data_ini)
		driver.find_element_by_xpath(self.data_julgamento_finalXP).send_keys(data_fim)
		driver.find_element_by_xpath(self.botao_pesquisar).click()
		time.sleep(4)
		links_inteiro_teor = driver.find_elements_by_partial_link_text('')
		for link in links_inteiro_teor:
			try:
				if re.search(r'pcjoDecisao.jsp\?',link.get_attribute('href')):
					link.click()
					driver.switch_to.window(driver.window_handles[1])
					break
			except:
				pass
		texto = crawler_jurisprudencia_tj.extrai_texto_html(self,(driver.page_source)).replace('"','')
		cursor.execute('INSERT INTO %s value ("%s");' % (self.tabela_colunas,texto))
		ult_pag = driver.current_url
		driver.find_element_by_xpath(self.botao_proximo).click()
		loop_counter = 0
		while True:
			try:
				if ult_pag == driver.current_url:
					break
				time.sleep(2)
				texto = crawler_jurisprudencia_tj.extrai_texto_html(self,(driver.page_source)).replace('"','')
				cursor.execute('INSERT INTO %s value ("%s");' % (self.tabela_colunas,texto))
				ult_pag = driver.current_url
				driver.find_element_by_xpath(self.botao_proximo).click()
			except Exception as e:
				print(e)
				loop_counter += 1
				if loop_counter > 2:
					driver.close()
					break
		driver.close()

	def parser_acordaos(self,texto_decisao,cursor):
		numero = busca(r'[\d\.\-]{11,28}', texto_decisao,ngroup=0)
		data_disponibilizacao = busca(r'\n\s*?Julgamento\:\n\s*?\n\s*?(\d{2}/\d{2}/\d{4})', texto_decisao)
		orgao_julgador = busca(r'\n\s*?.rgão julgador\:\n\s*?(.+)', texto_decisao)
		classe = busca(r'\n\s*?Classe\:\n\s*?(.+)', texto_decisao)
		decisao = busca(r'\n\s*?Processo\:(.+)', texto_decisao, args=re.DOTALL)
		julgador = busca(r'Relator.\s*?DESEMBARGADOR.([A-Z\s]{1,80})[a-z]', texto_decisao)		
		cursor.execute('INSERT INTO jurisprudencia_2_inst.jurisprudencia_2_inst (tribunal, numero, classe, data_decisao, orgao_julgador, julgador, texto_decisao) values ("%s","%s","%s","%s","%s","%s","%s");' % ('rn',numero, classe, data_disponibilizacao, orgao_julgador, julgador, texto_decisao))

if __name__ == '__main__':
	c = crawler_jurisprudencia_tjrn()
# 	print('comecei ',c.__class__.__name__)
# 	try:
# 		for l in range(len(c.lista_anos)):
# 			print(c.lista_anos[l],'\n')
# 			for m in range(len(c.lista_meses)):
# 				try:
# 					c.download_tj('01'+c.lista_meses[m]+c.lista_anos[l],'28'+c.lista_meses[m]+c.lista_anos[l])
# 				except Exception as e:
# 					print(e)
# 	except Exception as e:
# 		print('finalizei o ano com erro ',e)

	cursor = cursorConexao()
	cursor.execute('SELECT ementas from justica_estadual.jurisprudencia_rn limit 1000000')
	dados = cursor.fetchall()
	for dado in dados:
		c.parser_acordaos(dado[0], cursor)