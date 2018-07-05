from bs4 import BeautifulSoup
from common.conexao_local import cursorConexao
from crawler_jurisprudencia_tj import crawler_jurisprudencia_tj
from crawlerJus import crawlerJus
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sys, re, time

sys.path.append(os.path.dirname(os.getcwd()))
from common_nlp.parse_texto import busca

class crawler_jurisprudencia_tjsc():
	"""Crawler especializado em retornar textos da jurisprudência de segunda instância de Santa Catarina"""
	def __init__(self):
		crawler_jurisprudencia_tj.__init__(self)
		self.link_inicial = 'http://busca.tjsc.jus.br/jurisprudencia/buscaForm.do'
		self.pesquisa_livre = '//*[@id="q"]'
		self.inteiro_teor = '//*[@id="busca_avancada"]/table[1]/tbody/tr/td[2]/span[1]]'
		self.botao_pesquisar = '//*[@id="busca_avancada"]/input[2]'
		self.tabela_colunas = 'justica_estadual.jurisprudencia_sc (ementas)'
		self.botao_proximo_iniXP = '//*[@id="paginacao"]/ul/li[7]/a'
		self.botao_proximoXP = '//*[@id="paginacao"]/ul/li[%s]/a'
		self.data_inicialXP = '//*[@id="dtini"]'
		self.data_finalXP = '//*[@id="dtfim"]'

	def download_diario_retroativo(self):
		link_inicial = 'http://busca.tjsc.jus.br/dje-consulta/rest/diario/caderno?edicao=%s&cdCaderno=%s'
		cadernos = ['1','2','3']
		for i in range(2853,0,-1):
			for e in cadernos:
				try:
					print(link_inicial % (str(i),e))
					response = urllib.request.urlopen(link_inicial % (str(i),e),timeout=15)
					file = open(str(i)+'_'+e'.pdf', 'wb')
					file.write(response.read())
					file.close()
					subprocess.Popen('mv %s/*.pdf %s/Diarios_sc' % (os.getcwd(),path), shell=True)
				except Exception as e:
					print(e)

	def download_tj(self,data_ini,data_fim, termo='processo'):
		cursor = cursorConexao()
		driver = webdriver.Chrome(self.chromedriver)
		driver.get(self.link_inicial)
		driver.find_element_by_xpath(self.pesquisa_livre).send_keys(termo)
		driver.find_element_by_xpath(self.data_inicialXP).send_keys(data_ini)
		driver.find_element_by_xpath('//*[@id="busca_avancada"]/table[1]/tbody/tr/td[1]/span[1]').click()
		driver.find_element_by_xpath(self.data_finalXP).send_keys(data_fim)
		driver.find_element_by_xpath('//*[@id="busca_avancada"]/table[1]/tbody/tr/td[1]/span[1]').click()
		time.sleep(1)
		driver.find_element_by_xpath(self.botao_pesquisar).click()
		time.sleep(1)
		links_inteiro_teor = driver.find_elements_by_partial_link_text('')
		for l in links_inteiro_teor:
			try:
				if re.search(r'html\.do',l.get_attribute('href')):
					texto = l.get_attribute('href')
					cursor.execute('INSERT INTO %s value ("%s");' % (self.tabela_colunas,texto))	
			except:
				pass
		try:
			driver.find_element_by_xpath(self.botao_proximo_iniXP).click()
		except:
			driver.close()
			return
		loop_counter = 0
		while True:
			try:
				time.sleep(1)
				links_inteiro_teor = driver.find_elements_by_partial_link_text('')
				for l in links_inteiro_teor:
					try:
						if re.search(r'html\.do',l.get_attribute('href')):
							texto = l.get_attribute('href')
							cursor.execute('INSERT INTO %s value ("%s");' % (self.tabela_colunas,texto))
					except:
						pass
				try:
					driver.find_element_by_xpath(self.botao_proximoXP % '9').click()
				except:
					try:
						driver.find_element_by_xpath(self.botao_proximoXP % '8').click()
					except:
						driver.find_element_by_xpath(self.botao_proximoXP % '7').click()
			except Exception as e:
				driver.close()
				return
		driver.close()

	def download_acordao_sc(self,link, id_p, cursor):
		crawlerclass = crawlerJus()
		texto = crawlerclass.baixa_texto_html(link).replace('"','').replace('\\','').replace('/','')
		cursor.execute('UPDATE justica_estadual.jurisprudencia_sc set texto = "%s" where id = "%s"' % (texto, id_p))
		
	def parser_acordaos(self,texto,cursor):
		numero = busca(r'\d{4}\.\d{6}\-\d', texto,ngroup=0)
		classe = busca(r'Classe\:\s*?(.*?)\n', texto)
		julgador = busca(r'\n\s*?Juiz Prolator.*?\:(.*?)\n', texto)
		orgao_julgador = busca(r'\n.rgão Julgador\:(.*?)\n', texto)
		data_disponibilizacao = busca(r'\n\s*?Julgado em\s*?\:(.*?)\n', texto)
		origem = busca(r'\n\s*?Origem\s*?\:(.*?)\n', texto)
		cursor.execute('INSERT INTO jurisprudencia_2_inst.jurisprudencia_2_inst_sc (tribunal, numero, classe, data_decisao, orgao_julgador, julgador, origem, texto_decisao) values ("%s","%s","%s","%s","%s","%s","%s","%s");' % ('sc',numero, classe, data_disponibilizacao, orgao_julgador, julgador, origem, texto))

def main():
	c = crawler_jurisprudencia_tjsc()
	cursor = cursorConexao()

	# print('comecei ',c.__class__.__name__)
	# for a in c.lista_anos:
	# 	print(a)
	# 	for m in range(len(c.lista_meses)):
	# 		try:
	# 			c.download_tj('01/'+c.lista_meses[m]+'/'+a,'14/'+c.lista_meses[m]+'/'+a)
	# 		except Exception as e:
	# 			print(e,c.lista_meses[m])
	# 		try:
	# 			c.download_tj('15/'+c.lista_meses[m]+'/'+a,'28/'+c.lista_meses[m]+'/'+a)
	# 		except Exception as e:
	# 			print(e,c.lista_meses[m])

	# cursor.execute('SELECT id,ementas from justica_estadual.jurisprudencia_sc;')
	# lista_links = cursor.fetchall()
	# for i,l in lista_links:
	# 	c.download_acordao_sc(l, i, cursor)

	cursor.execute('SELECT texto from justica_estadual.jurisprudencia_sc;')
	dados = cursor.fetchall()
	for dado in dados:
		c.parser_acordaos(dado[0], cursor)



if __name__ == '__main__':
	main()