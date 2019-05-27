import urllib.request, json, pandas as pd, time, pyautogui, ssl
from crawlerJus import crawlerJus
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class crawlers_bec(crawlerJus):
	def __init__(self):
		super().__init__()
		ssl._create_default_https_context = ssl._create_unverified_context 
		
	def crawler_api_bec(self,contador=0):
		url = 'https://www.bec.sp.gov.br/BEC_API/API/pregao_encerrado/OC_encerrada/20090101/20181008/%s'
		df = pd.read_excel('/home/danilo/Downloads/OCs_para query Pregoeiros.xlsx')
		contador_aux = 0
		for index, row in df.iterrows():
			# if contador_aux > contador:
			# 	break
			try:
				req = urllib.request.Request(url % (row['Numero da OC'],))
				r = urllib.request.urlopen(req,timeout=3).read()
				filejson = open('/home/danilo/Downloads/BEC_json_exemplos/dados_bec_sp_%s.json' % (row['Numero da OC'],), 'w')
				json.dump(json.loads(r.decode('utf-8')), filejson, ensure_ascii=False)
				time.sleep(0.5)
				contador_aux += 1
			except Exception as e:
				print(e)
				print(row['Numero da OC'])

	def crawler_editais_bec(self):
		url = 'https://www.bec.sp.gov.br/BECSP/aspx/ConsultaOCLinkExterno.aspx?OC=%s&OC=%s'
		driver = webdriver.Chrome(self.chromedriver)
		df = pd.read_excel('/home/danilo/Downloads/OCs_para query Pregoeiros.xlsx')
		for index, row in df.iterrows():
			driver.get(url % (row['Numero da OC'],row['Numero da OC']))
			driver.execute_script("__doPostBack('dgDocumento$ctl03$ctl00','')")
			time.sleep(1)
			pyautogui.press('enter')

if __name__ == '__main__':
	#ENDEREÇO DA DF COM NÚMERO DE OC'S
	c = crawlers_bec()
	c.crawler_editais_bec()