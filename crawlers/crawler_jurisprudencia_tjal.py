import sys, re, os, urllib.request, time, subprocess
from common.download_path import path
from crawler_jurisprudencia_tj import crawler_jurisprudencia_tj
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class crawler_jurisprudencia_tjal(crawler_jurisprudencia_tj):
	"""Crawler especializado em retornar textos da jurisprudência de segunda instância de Alagoas"""
	def __init__(self):
		crawler_jurisprudencia_tj.__init__(self)
		self.link_inicial = 'https://www2.tjal.jus.br/cjsg/consultaCompleta.do'
		self.pesquisa_livre = '//*[@id="iddados.buscaInteiroTeor"]'
		self.data_julgamento_inicialXP = '//*[@id="iddados.dtJulgamentoInicio"]'
		self.data_julgamento_finalXP = '//*[@id="iddados.dtJulgamentoFim"]'
		self.botao_pesquisar = '//*[@id="pbSubmit"]'
		self.botao_proximo_ini = '//*[@id="paginacaoSuperior-A"]/table/tbody/tr[1]/td[2]/div/a[5]'
		self.botao_proximo = '//*[@id="paginacaoSuperior-A"]/table/tbody/tr[1]/td[2]/div/a[6]'
		self.tabela_colunas = 'justica_estadual.jurisprudencia_al (ementas)'

	def download_1_inst(self):
		botao_proximo_ini = 2
		botao_proximo = '//*[@id="pn_%s"]'
		botao_xpath = '//*[@id="corpo_texto"]/div/div/div/form/button'
		driver = webdriver.Chrome(self.chromedriver)
		link = 'http://www.tjal.jus.br/corregedoria/?pag=sentencas'
		re_href = r'http\://www.intranet.tjal.jus.br/bancodesentencas/arquivos/'
		texto_xpath = '//*[@id="corpo_texto"]/div/div/div/form/input'
		driver.get(link)
		driver.find_element_by_xpath(texto_xpath).send_keys('a ou não a')
		driver.find_element_by_xpath(botao_xpath).click()
		time.sleep(1)
		contador = 0
		loop_counter = 0
		while True:
			try:
				soup = BeautifulSoup(driver.page_source,'html.parser')
				for l in soup.find_all('a', href=True):
					if re.search(re_href,l['href']):
						urllib.request.urlretrieve(l['href'],'TJAL_1_inst_%s.pdf' % str(contador))
						subprocess.Popen('mv TJAL_1_inst_*.pdf %s/al_1_inst' % (path,), shell=True)
						contador += 1
				try:
					driver.find_element_by_xpath(botao_proximo % str(botao_proximo_ini)).click()
				except:
					botao_proximo_ini += 1
					driver.find_element_by_xpath(botao_proximo % str(botao_proximo_ini)).click()
				loop_counter = 0
			except Exception as e:
				if loop_counter > 2:
					break
				loop_counter += 1
				print(e)

	def parser_acordao(self,texto):
		classe = False
		inicio = False
		numero = False
		dados_decisao = {}
		ementa_txt = ''
		re_classe = r'Classe/Assunto:' # linha seguinte
		re_ementa = r'^Ementa:' #depois de tudo o que já passou e até o próximo início
		re_inicio = r'^\d*?\s*?\-\s*?$'
		re_numero = r'^\s*?(\d{7}\-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4})\s*?$'
		re_dados_ementa = r'\((.*?\(.*?)\(' # re.DOTALL
		re_comarca = r'Comarca:(.*?);'
		re_data_julgamento = r'Data do julgamento: (.*?);'
		re_orgao_julgador = r'Órgão julgador:(.*?);'
		re_relator = r'Relator \(a\)\:(.*?);'
		for line in texto:
			if re.search(re_inicio,line):
				# fazer algo sobre decisão anterior
				dados_decisao = {}
				classe = False
				inicio = True
				numero = False
				continue
			if inicio:
				if numero:
					if classe:
						if 'classe' not in dados_decisao:
							if line != ':'
								dados_decisao['classe'] = line
					else:
						if re.search(re_classe,line):
							texto_ementa = re.search(r'.*?\(',ementa_txt)
							dados_ementa = re.search(re_dados_ementa,ementa_txt)
							if dados_ementa:
								dados_ementa = dados_ementa.group(0)
								comarca = re.search(re_comarca,dados_ementa).group(0)
								data_julgamento = re.search(re_data_julgamento,dados_ementa).group(0)
								orgao_julgador = re.search(re_orgao_julgador,dados_ementa).group(0)
								relator = re.search(re_relator,dados_ementa).group(0)
							dados_decisao['ementa'] = texto_ementa.group(0)
							dados_decisao['comarca'] = comarca
							dados_decisao['data_julgamento'] = data_julgamento
							dados_decisao['orgao_julgador'] = orgao_julgador
							dados_decisao['relator'] = relator
							ementa_txt = ''
							classe = True
						else:
							ementa_txt += line
				else:
					numero_txt = re.search(re_numero,line)
					if numero_txt:
						dados_decisao['numero'] = numero_txt.group(0)
					numero = True

def main():
	c = crawler_jurisprudencia_tjal()
	c.download_1_inst()
	# print('comecei ',c.__class__.__name__)
	# for l in c.lista_anos:
	# 	try:
	# 		print(l,'\n')
	# 		crawler_jurisprudencia_tj.download_tj_ESAJ_recaptcha(c,crawler_jurisprudencia_tj,'01/01/'+l,'31/12/'+l)
	# 	except Exception as e:
	# 		print('finalizei o ano ',l)
	# 		print(e)

if __name__ == '__main__':
	main()