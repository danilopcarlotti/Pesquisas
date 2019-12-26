from crawlerJus import crawlerJus
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib.request, json, pandas as pd, time, pyautogui, ssl, sys, pickle

PATH_EXCEL_OCS = '/media/danilo/Seagate Expansion Drive/Dados Compras Públicas/df_ocs_nao_baixadas.xlsx'
PATH_DOWNLOAD = '/home/danilo/Downloads/BEC_json/'

class crawlers_bec(crawlerJus):
	def __init__(self):
		super().__init__()
		ssl._create_default_https_context = ssl._create_unverified_context 

	def crawler_api_bec_editais(self,path_excel=PATH_EXCEL_OCS,contador=0):
		ocs_nao_baixadas = []
		url = 'https://www.bec.sp.gov.br/BEC_API/API/pregao_encerrado/OC_encerrada/20090101/20181008/%s'
		df = pd.read_excel(path_excel,skiprows=(1,10))
		for _, row in df.iterrows():
			try:
				req = urllib.request.Request(url % (row['Numero da OC'],))
				r = urllib.request.urlopen(req,timeout=3).read()
				json_oc = json.loads(r.decode('utf-8'))
				self.crawler_editais_bec(list_urls=[json_oc])
				time.sleep(0.5)
				contador_aux += 1
			except Exception as e:
				print(e)
				ocs_nao_baixadas.append(row['Numero da OC'])
		return ocs_nao_baixadas

	def crawler_api_bec(self,path_excel=PATH_EXCEL_OCS,contador=0):
		ocs_nao_baixadas = []
		url = 'https://www.bec.sp.gov.br/BEC_API/API/pregao_encerrado/OC_encerrada/20090101/20181008/%s'
		df = pd.read_excel(path_excel)
		contador_aux = 0
		for _, row in df.iterrows():
			# if contador_aux > contador:
			# 	break
			try:
				req = urllib.request.Request(url % (row['Numero da OC'],))
				r = urllib.request.urlopen(req,timeout=3).read()
				filejson = open(PATH_DOWNLOAD+'dados_bec_sp_%s.json' % (row['Numero da OC'],), 'w')
				json.dump(json.loads(r.decode('utf-8')), filejson, ensure_ascii=False)
				time.sleep(0.5)
				contador_aux += 1
			except Exception as e:
				print(e)
				ocs_nao_baixadas.append(row['Numero da OC'])
		return ocs_nao_baixadas

	def crawler_editais_bec(self, list_urls=[], url_oc='https://www.bec.sp.gov.br/BECSP/aspx/ConsultaOCLinkExterno.aspx?OC=%s&OC=%s'):
		if len(list_urls):
			for u in list_urls:
				try:
					driver = webdriver.Chrome(self.chromedriver)
					driver.get(u)
					driver.execute_script("__doPostBack('ctl00$conteudo$WUC_Documento1$dgDocumento$ctl02$ctl00','')")
					time.sleep(1)
					driver.close()
				except:
					time.sleep(15)
		else:
			df = pd.read_excel(PATH_EXCEL_OCS)
			for _, row in df.iterrows():
				driver.get(url_oc % (row['Numero da OC'],row['Numero da OC']))
				driver.execute_script("__doPostBack('dgDocumento$ctl03$ctl00','')")
				time.sleep(1)
				pyautogui.press('enter')

if __name__ == '__main__':
	c = crawlers_bec()
	ocs_nao_baixadas = c.crawler_api_bec_editais()
	pickle.dump(ocs_nao_baixadas,open('ocs_bec_nao_baixadas.pickle','wb'))