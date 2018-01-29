from crawlerJus import crawlerJus
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from common.conexao_local import cursorConexao
from datetime import date
import time, os, common.download_path, re, subprocess

class crawler_jurisprudencia_tj():
	"""Generic class with methods for crawler_jurisprudencia_tj's"""
	def __init__(self):
		crawlerJus.__init__(self)
		self.lista_anos = [str(i) for i in range(2011,date.today().year+1)]
		self.lista_meses = ['0'+str(i) for i in range(1,10)]
		self.lista_meses += ['10','11','12']

	def captcha(self, path=None):
		from common.transcrever_audio import transcrever_audio
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

	def download_pdf_acordao(self,link,input_captcha_xpath,ouvir_captch_xpath,id_acordao):
		driver = webdriver.Chrome(self.chromedriver)
		driver.get_link(link)
		try:
			driver.find_element_by_xpath(input_captcha_xpath).click() #VERIFICAR SE ESTE É UM TESTE POSSÍVEL E/OU BOM
			self.delete_audios()
			# alterar o identificador do monitor de stereo
			# https://www.funwithelectronics.com/?id=95
			command = 'pacat --record -d alsa_output.pci-0000XXX.monitor | sox -t raw -r 44100 -s -L -b 16 -c 2 - "audio.wav" trim 0 5'
			proc = subprocess.Popen(command, shell=True)
			driver.find_element_by_xpath(ouvir_captch_xpath).click()
			try:
				outs, errs = proc.communicate(timeout=6)
			except TimeoutExpired:
				proc.kill()
				outs, errs = proc.communicate()
			driver.find_element_by_xpath(input_captcha_xpath).send_keys(self.captcha())
			self.delete_audios()
		except:
			pass
		pyautogui.hotkey('ctrl','s')
		time.sleep(1)
		pyautogui.typewrite('Acordao_'+id_acordao)
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
			pag = BeautifulSoup(pagina,'lxml')
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