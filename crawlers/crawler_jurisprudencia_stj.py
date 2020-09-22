import re, os, sys, time, datetime, urllib.request, ssl,logging, pyautogui, pandas as pd
from bs4 import BeautifulSoup
from common.download_path import path, path_hd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from crawlerJus import crawlerJus
from common.conexao_local import cursorConexao
from common.recursive_folders import recursive_folders

class crawler_jurisprudencia_stj(crawlerJus):
	"""Classe para download de informações sobre processos do STJ"""
	def __init__(self, contador=1):
		super().__init__()
		ssl._create_default_https_context = ssl._create_unverified_context 
		self.lista_span_dados = ['//*[@id="idProcessoDetalhesBloco1"]/div[1]/span[2]', 
		'//*[@id="idDetalhesPartesAdvogadosProcuradores"]/div[1]/span[2]/a',
		'//*[@id="idDetalhesPartesAdvogadosProcuradores"]/div[2]/span[2]/a',
		'//*[@id="idProcessoDetalhesBloco1"]/div[5]/span[2]',
		'//*[@id="idProcessoDetalhesBloco1"]/div[6]/span[2]/a',
		'//*[@id="idProcessoDetalhesBloco2"]/div[1]/span[2]',
		'//*[@id="idProcessoDetalhesBloco2"]/div[2]/span[2]',
		'//*[@id="idProcessoDetalhesBloco2"]/div[3]/span[2]',
		'//*[@id="idProcessoDetalhesBloco3"]/div[1]/span[2]',
		'//*[@id="idProcessoDetalhesBloco3"]/div[2]/span[2]'
		]
		self.contador = contador
		
	def baixarDadosProcesso(self, termo='a'):
		driver = webdriver.Chrome(self.chromedriver)
		link_pesquisa = 'http://www.stj.jus.br/SCON/'
		driver.get(link_pesquisa)
		driver.find_element_by_xpath('//*[@id="pesquisaLivre"]').send_keys(termo)
		driver.find_element_by_xpath('//*[@id="botoesPesquisa"]/input[1]').click()
		time.sleep(6)
		driver.find_elements_by_xpath('//*[@id="itemlistaresultados"]/span[2]/a')[2].click()
		time.sleep(6)
		driver.find_element_by_class_name('iconeProximaPagina').send_keys('\n')
		i = 1
		while i < self.contador:
			try:
				driver.find_element_by_class_name('iconeProximaPagina').send_keys('\n')
				i += 1
			except:
				driver.execute_script("window.history.go(-1)")
				driver.find_element_by_class_name('iconeProximaPagina').send_keys('\n')
		while self.contador < 62000: #jun 2018
			cursor = cursorConexao()
			try:
				acompanhamentos = driver.find_elements_by_xpath('//*[@id="acoesdocumento"]/a[2]')
				for a in acompanhamentos:
					a.click()
					try:
						driver.switch_to.window(driver.window_handles[1])
						try:
							driver.find_element_by_xpath('/html/body/a').click()
						except:
							time.sleep(0.5)
							driver.find_element_by_xpath('/html/body/a').click()
					except Exception as e:
						print(e)
					info = []
					for d in self.lista_span_dados:
						try:
							info.append(driver.find_element_by_xpath(d).text)
						except:
							pass
					if len(info) == 10:
						html = driver.page_source
						link_voto = re.findall(r'/processo/revista/documento/mediado/\?componente=ATC.*?tipo=\d+',html)
						if len(link_voto) > 0:
							votos = ''
							for decisao in link_voto:
								link_voto_download = 'https://ww2.stj.jus.br'+decisao+'&formato=html'
								link_voto_download = link_voto_download.replace('amp;','')
								votos += link_voto_download+','
							info.append(votos[:-1])
							cursor.execute('INSERT INTO stj.dados_processo_gisela (processo, recorrente, recorrido, autuacao, numero_unico, relator, ramo_direito, assunto, tribunal_origem, numeros_origem,link_voto) values ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")',(info[0],info[1],info[2],info[3],info[4],info[5],info[6],info[7],info[8],info[9],info[10]))
					driver.switch_to.window(driver.window_handles[0])
				try:
					driver.find_element_by_class_name('iconeProximaPagina').send_keys('\n')
					self.contador += 1
				except:
					time.sleep(5)
					driver.execute_script("window.history.go(-1)")
					driver.find_element_by_class_name('iconeProximaPagina').send_keys('\n')
			except Exception as e:
				print(e)
				try:
					time.sleep(5)
					driver.execute_script("window.history.go(-1)")
					driver.find_element_by_class_name('iconeProximaPagina').send_keys('\n')
				except Exception as e:
					print(e)
					print(str(self.contador))
					driver.close()
					self.baixarDadosProcesso()

	def baixarVotos(self):
		cursor = cursorConexao()
		crawler = crawlerJus()
		cursor.execute('SELECT id, link_voto from stj.dados_processo;')
		link_votos = cursor.fetchall()
		contador = 1
		for id_voto, link in link_votos:
			html_ini = crawler.baixa_pag(link.replace('\'',''))
			if html_ini == '':
				continue
			soup = BeautifulSoup(html_ini,'lxml')
			link_final = soup.find_all('a')[0]
			html_final = crawler.baixa_pag('https://ww2.stj.jus.br/'+link_final['href'])
			soup2 = BeautifulSoup(html_final,'html.parser')
			texto = soup2.get_text()
			cursor.execute('INSERT into stj.votos (id_processo,voto) values (%s,"%s")' % (str(id_voto),texto.replace('"','')))
			print(contador)
			contador += 1

	def download_diario_retroativo(self,path_download=''):
		datas = []
		lista_anos = [str(i) for i in range(2011,datetime.date.today().year+1)]
		for l in range(len(lista_anos)):
			for i in range(1,10):
				for j in range(1,10):
					datas.append('0'+str(j)+'0'+str(i)+''+lista_anos[l])
				for j in range(10,32):
					datas.append(str(j)+'0'+str(i)+lista_anos[l])
			for i in range(10,13):
				for j in range(1,10):
					datas.append('0'+str(j)+str(i)+lista_anos[l])
				for j in range(10,32):
					datas.append(str(j)+str(i)+lista_anos[l])
		log_datas_stj = open(path_download+'log_datas_stj.txt','a')
		for data in datas:
			log_datas_stj.write(data)
			try:
				link_stj_f = "https://ww2.stj.jus.br/docs_internet/processo/dje/zip/stj_dje_%s.zip" % (data,)
				file = open(path_download+data+"STJ.zip", 'wb')
				response = urllib.request.urlopen(link_stj_f,timeout=300)
				time.sleep(2)
				file.write(response.read())
				file.close()
			except Exception as e:
				print(e)

	def processar_arquivos_diarios(self, path_arquivos, path_csv_final='decisões_stj.csv'):
		r = recursive_folders()
		rows = []
		paths = [i for i in r.find_files(path_arquivos) if i[-4:] == '.txt']
		print('Arquivos sendo processados ',len(paths))
		for p in paths:
			text = open(p, 'r')
			rows.append({'nome_arquivo':p,'texto_publicacao':' '.join([line for line in text])})
		df = pd.DataFrame(rows,index=[i for i in range(len(rows))]) 
		df.to_csv(path_csv_final,index=False)


if __name__ == '__main__':
	c = crawler_jurisprudencia_stj()
	# c.baixarDadosProcesso()
	c.download_diario_retroativo()
	# c.processar_arquivos_diarios('/home/deathstar/Documents/Diarios_outros/STJ_diarios_2019',path_csv_final='decisões_stj_2019.csv')