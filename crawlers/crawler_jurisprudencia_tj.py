import time, os, common.download_path, re, subprocess, pyautogui
from bs4 import BeautifulSoup
from common.audio_monitor import audio_monitor
from common.conexao_local import cursorConexao
from crawlerJus import crawlerJus
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from common.transcrever_audio import transcrever_audio

class crawler_jurisprudencia_tj(crawlerJus):
	"""Generic class with methods for crawler_jurisprudencia_tj's"""
	def __init__(self):
		crawlerJus.__init__(self)
		self.lista_anos = [str(i) for i in range(2011,date.today().year+1)]
		self.lista_meses = ['0'+str(i) for i in range(1,10)]
		self.lista_meses += ['10','11','12']

	def captcha(self, path=None):
		t = transcrever_audio()
		if path:
			return t.transcrever(path)
		for file in os.listdir(common.download_path.path+'/'):
			if re.search(r'wav',file):
				return t.transcrever(audio=common.download_path.path+'/'+file)

	def delete_audios(self):
		for file in os.listdir(common.download_path.path+'/'):
			if re.search(r'wav',file):
				os.remove(common.download_path.path+'/'+file)

	def download_pdf_acordao_captcha_audio(self,link,input_captcha_xpath,ouvir_captch_xpath,send_captcha,id_acordao):
		binary = FirefoxBinary(common.download_path.path+'/firefox/firefox')
		profile = webdriver.FirefoxProfile()
		profile.set_preference("plugin.state.flash", 2)
		driver = webdriver.Firefox(profile,firefox_binary=binary,executable_path=common.download_path.path+'/geckodriver')
		driver.get(link)
		try:
			driver.find_element_by_xpath(input_captcha_xpath).send_keys('')
			captcha_on = True
		except:
			captcha_on = False
		while captcha_on:
			command = 'pacat --record -d %s | sox -t raw -r 44100 -s -L -b 16 -c 2 - "audio.wav" trim 0 6' % audio_monitor
			proc = subprocess.Popen(command, shell=True)
			time.sleep(1)
			driver.find_element_by_xpath(ouvir_captch_xpath).click()
			time.sleep(6)
			try:
				outs, errs = proc.communicate(timeout=7)
			except TimeoutExpired:
				proc.kill()
				outs, errs = proc.communicate()
			driver.find_element_by_xpath(input_captcha_xpath).send_keys(self.captcha(path='audio.wav'))
			driver.find_element_by_xpath(send_captcha).click()
			time.sleep(2)
			try:
				driver.find_element_by_xpath(input_captcha_xpath).send_keys('')
			except:
				captcha_on = False
		time.sleep(1)
		pyautogui.hotkey('ctrl','s')
		time.sleep(1)
		pyautogui.typewrite(id_acordao)
		time.sleep(1)
		pyautogui.press('enter')
		time.sleep(1)
		driver.close()

	def download_pdf_acordao_sem_captcha(self,link,id_acordao):
		driver = webdriver.Chrome(self.chromedriver)
		driver.get(link)
		time.sleep(1)
		pyautogui.hotkey('ctrl','s')
		time.sleep(1)
		pyautogui.typewrite(id_acordao)
		time.sleep(1)
		pyautogui.press('enter')
		time.sleep(1)
		driver.close()

	def download_jurisprudencia(self,driver,pesquisa_livre,data_julg_iniXP,data_julg_ini,data_julg_fimXP,data_julg_fim,botao_pesquisar,termo):
		driver.find_element_by_xpath(pesquisa_livre).send_keys(termo)
		driver.find_element_by_xpath(data_julg_iniXP).send_keys(data_julg_ini)
		driver.find_element_by_xpath(data_julg_fimXP).send_keys(data_julg_fim)
		driver.find_element_by_xpath(botao_pesquisar).click()

	def download_tj_ESAJ(self,superC,data_julg_ini,data_julg_fim,termo='acordam'):
		cursor = cursorConexao()
		driver = webdriver.Chrome(self.chromedriver)
		def insert_links(pagina):
			pag = BeautifulSoup(pagina,'html.parser')
			links = pag.find_all('a', attrs={'title':'Visualizar Inteiro Teor'})
			for l in links:
				texto = self.link_esaj % (l.attrs['cdacordao'],l.attrs['cdforo'])
				cursor.execute('INSERT INTO %s value ("%s");' % (self.tabela_colunas,texto))
		driver.get(self.link_inicial)
		superC.download_jurisprudencia(self,driver,self.pesquisa_livre,self.data_julgamento_inicialXP,data_julg_ini,self.data_julgamento_finalXP,data_julg_fim,self.botao_pesquisar,termo=termo)
		time.sleep(2)
		insert_links(driver.page_source)
		driver.find_element_by_xpath(self.botao_proximo_ini).click()
		time.sleep(2)
		insert_links(driver.page_source)
		contador = 0
		while True:
			try:
				driver.find_element_by_xpath(self.botao_proximo).click()
				time.sleep(3)
				insert_links(driver.page_source)
				contador = 0
			except Exception as e:
				time.sleep(3)
				print(e)
				contador +=1
				if contador > 2:
					break
		driver.close()

	def extrai_texto_html(self,pagina):
		return crawlerJus.extrai_texto_html(self,pagina)

# create_statement_ESAJ = '''
# use justica_estadual;
# CREATE TABLE `jurisprudencia_am` (
#   `id` int(11) NOT NULL AUTO_INCREMENT,
#   `ementas` longtext,
#   PRIMARY KEY (`id`)
# ) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;
# '''