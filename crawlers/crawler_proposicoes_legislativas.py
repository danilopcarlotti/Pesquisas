import time, datetime, urllib.request, os, re, ssl, pymysql, pandas as pd
from bs4 import BeautifulSoup
from common.conexao_local import cursorConexao
from common.download_path import path
from common_nlp.topicModelling import topicModelling
from selenium import webdriver

class crawler_proposicoes_legislativas():
	
	def __init__(self):
		data = datetime.date.today().strftime("%Y%m%d")
		ano = data[:4]
		mes = data[4:6]
		dia = data[6:]
		if len(dia)==1:
			dia = "0" + dia
		self.data = dia+'/'+mes+'/'+ano
		self.link_inicial = 'https://www.camara.leg.br/buscaProposicoesWeb/resultadoPesquisa?data={}&page=true&emtramitacao=Sim&regime=Urg%C3%AAncia'.format(self.data)
		self.chromedriver = os.getcwd()+"/chromedriver"
		os.environ["webdriver.chrome.driver"] = self.chromedriver
		ssl._create_default_https_context = ssl._create_unverified_context

	def download_csv(self):
		driver = webdriver.Chrome(self.chromedriver)
		driver.get(self.link_inicial)
		driver.find_element_by_xpath('//*[@id="content"]/div[1]/form/ul[1]/li[4]/div/input').click()
		time.sleep(1)
		driver.find_element_by_xpath('//*[@id="id4"]/a').click()
		time.sleep(4)


	def topic_modelling_proposicoes(self):
		cursor = cursorConexao()
		tp = topicModelling()
		cursor.execute('SELECT ementa FROM governo_federal.proposicoes_legislativas_urg;')
		textos = [ementa[0] for ementa in cursor.fetchall()]
		topicos = tp.lda_Model(textos,num_words=30)
		tp.topic_to_txt(topicos)

	def upload_proposicoes(self):
		cursor = cursorConexao()
		df = pd.read_csv(path+'/relatorioPesquisa.csv',skiprows=2,encoding='latin-1',error_bad_lines=True,sep=';')
		for index, row in df.iterrows():
			cursor.execute('INSERT INTO governo_federal.proposicoes_legislativas_urg (proposicoes, ementa, explicacao, autor, uf, partido, apresentacao, situacao, link) values ("%s","%s","%s","%s","%s","%s","%s","%s","%s");' % (str(row['Proposições']).replace('"',''),str(row['Ementa']).replace('"',''),str(row['Explicação ']).replace('"',''),str(row['Autor']).replace('"',''),str(row['UF']).replace('"','')[:45],str(row['Partido'])[:45].replace('"',''),str(row['Apresentaç']).replace('"','')[:45],str(row['Situação']).replace('"',''),str(row['Link ']).replace('"','')))

if __name__ == '__main__':
	c = crawler_proposicoes_legislativas()
	# c.download_csv()
	# c.upload_proposicoes()
	c.topic_modelling_proposicoes()