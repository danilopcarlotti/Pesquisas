import re, time, urllib.request, ssl, logging, subprocess, os, pyautogui, datetime, sys
from bs4 import BeautifulSoup
from common.download_path import path
from common.download_path_diarios import path as path_diarios
from crawlerJus import crawlerJus
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

ssl._create_default_https_context = ssl._create_unverified_context

class publicacoes_diarios_oficiais(crawlerJus):
	def __init__(self, data=None):
		options = Options()
		options.headless = True
		crawlerJus.__init__(self)
		logging.basicConfig(filename=self.cwd+self.dia+self.mes+self.ano+'.log',level=logging.INFO)
		self.diarios_a_baixar = [self.baixa_stf,self.baixa_ro,self.baixa_rr,self.baixa_pa,self.baixa_ma,self.baixa_to,self.baixa_pi,self.baixa_stj,self.baixa_trf1,
		self.baixa_trf5,self.baixa_go,self.baixa_rs,self.baixa_ac,self.baixa_trf4,self.baixa_df,self.baixa_sc,self.baixa_rn,self.baixa_trf3,self.baixa_pe,
		self.baixa_sp,self.baixa_ce,self.baixa_al,self.baixa_ms,self.baixa_am,self.baixa_pr,self.baixa_trt,self.baixa_es,self.baixa_ap,self.baixa_pb,self.baixa_se,
		self.baixa_mt,self.baixa_trf2]		
		hoje = datetime.date.today().strftime("%Y%m%d")
		self.ano = hoje[:4]
		self.mes = hoje[4:6]
		self.dia = hoje[6:]
		if len(self.dia)==1:
		    self.dia = "0" + self.dia
		self.data = data
		if self.data:
			self.ano_pesquisar = self.data[:4]
			self.mes_pesquisar = self.data[4:6]
			self.dia_pesquisar = self.data[6:]

		# FALTA MG, RJ, BA

	def baixaEsaj(self,inicio, fim, pag):
		XPathInicial = "//*[@id=\"cadernosCad\"]/option["
		XPathFinal = "]"
		for i in range(inicio,fim):
			driver = webdriver.Chrome(self.chromedriver)
			driver.get(pag)
			driver.find_element_by_xpath(XPathInicial+str(int(i))+XPathFinal).click()   
			driver.find_element_by_xpath("//*[@id=\"download\"]").click()
			driver.close()
			time.sleep(1)

	def baixa_ac(self, todos=None):
		driver = webdriver.Chrome(self.chromedriver)
		ac_dje = "http://diario.tjac.jus.br/edicoes.php"
		if todos:
			# https://diario.tjac.jus.br/edicoes.php?Ano=2018&Mes=1
			counter = 36
			driver.get(ac_dje)
			aux = True
			while aux:
				aux = int(input('Escolha mes e ano na página ou digite 0 para sair'))
				pag_ac = driver.page_source
				pag_ac_bs = BeautifulSoup(pag_ac,'html.parser')
				link_ac_i = pag_ac_bs.findAll('a',attrs={'title':'Baixar'})
				for l in link_ac_i:
					link_ac_f = "http://diario.tjac.jus.br"+str(l['href'])
					self.baixa_html_pdf(link_ac_f,'TJAC_'+str(counter))
					subprocess.Popen('mv %s/%s.pdf "%s/Diarios_ac/dir_005/%s.pdf"' % (os.getcwd(),'TJAC_'+str(counter),path_diarios,'TJAC_'+str(counter)), shell=True)
					counter += 1
		else:
			pag_ac = self.baixa_pag(ac_dje)
			pag_ac_bs = BeautifulSoup(pag_ac,'html.parser')
			link_ac_i = pag_ac_bs.find('a',attrs={'title':'Baixar'})
			link_ac_f = "http://diario.tjac.jus.br"+str(link_ac_i['href'])
			driver.get(link_ac_f)
			time.sleep(5)
			subprocess.Popen('cp %s/*.pdf %s/%s.pdf' % (path,path_diarios,'TJAC_'+str(self.dia)+str(self.mes)+str(self.ano)), shell=True)
			subprocess.Popen('rm %s/*.pdf' % (path), shell=True)

	def baixa_al(self):
		if self.data:
			from crawler_jurisprudencia_tjal import crawler_jurisprudencia_tjal
			c = crawler_jurisprudencia_tjal()
			c.download_diario_retroativo(data_especifica=self.dia_pesquisar+'/'+self.mes_pesquisar+'/'+self.ano_pesquisar)
		else:
			pag_al = "http://www2.tjal.jus.br/cdje/index.do"
			self.baixaEsaj(1,3,pag_al)
			subprocess.Popen('mv %s/*.pdf %s/TJAL_%s.pdf' % (path,path_diarios,self.dia+self.mes+self.ano), shell=True)

	def baixa_am(self):
		if self.data:
			from crawler_jurisprudencia_tjam import crawler_jurisprudencia_tjam
			c = crawler_jurisprudencia_tjam()
			c.download_diario_retroativo(data_especifica=self.dia_pesquisar+'/'+self.mes_pesquisar+'/'+self.ano_pesquisar)
		else:
			pag_am = "http://consultasaj.tjam.jus.br/cdje/index.do"
			baixaEsaj(2,5,pag_am)
			subprocess.Popen('mv %s/*.pdf %s/TJCE_%s.pdf' % (path,path_diarios,self.dia+self.mes+self.ano), shell=True)

	def baixa_ap(self, ultimo_download=2765):
		driver = webdriver.Chrome(self.chromedriver)
		driver.get('http://tucujuris.tjap.jus.br/tucujuris/pages/consultar-dje/consultar-dje.html')
		time.sleep(5)
		driver.execute_script("document.getElementById('dje-%s').click()" % (str(ultimo_download+1),))
		print(driver.execute_script("document.getElementById('dje-%s')" % (str(ultimo_download+1),)))
		driver.execute_script("%s.download" % (str(ultimo_download+1),))
		time.sleep(5)
		# atualizar ultimo_download!!!
	
	def baixa_ba(self, primeiro=1207, ultimo=2502):
		from crawler_jurisprudencia_tjba import crawler_jurisprudencia_tjba
		c = crawler_jurisprudencia_tjba()
		c.download_diario_retroativo(path_diarios, primeiro=primeiro, ultimo=ultimo)

	def baixa_ce(self):
		if self.data:
			from crawler_jurisprudencia_tjce import crawler_jurisprudencia_tjce
			c = crawler_jurisprudencia_tjce()
			c.download_diario_retroativo(data_especifica=self.dia_pesquisar+'/'+self.mes_pesquisar+'/'+self.ano_pesquisar)
		else:
			pag_ce = "http://esaj.tjce.jus.br/cdje/index.do"
			baixaEsaj(2,3,pag_ce)
			subprocess.Popen('mv %s/*.pdf %s/TJCE_%s.pdf' % (path,path_diarios,self.dia+self.mes+self.ano), shell=True)

	def baixa_df(self):
		driver = webdriver.Chrome(self.chromedriver)
		df_dje = "https://dje.tjdft.jus.br/dje/djeletronico?visaoId=tjdf.djeletronico.comum.internet.apresentacao.VisaoDiarioEletronicoInternetPorData"
		pag_df = self.baixa_pag(df_dje)
		pag_df_bs = BeautifulSoup(pag_df,'html.parser')
		link_df_i = pag_df_bs.find('a',href=re.compile('https://dje.tjdft.jus.br/dje/jsp/dje/DownloadDeDiario.jsp'))
		link_df_f = str(link_df_i['href'])
		driver.get(link_df_f)
		time.sleep(15)
		subprocess.Popen('mv %s/*.PDF %s/TJDF_%s.pdf' % (path,path_diarios,str(self.dia)+str(self.mes)+str(self.ano)), shell=True)

	def baixa_es(self):
		diario_es = open(self.dia+self.mes+self.ano+"es.txt","a",encoding='utf-8')
		dje_es = "https://sistemas.tjes.jus.br/ediario/"
		pag_es = self.baixa_pag(dje_es)
		pag_es_bs = BeautifulSoup(pag_es,'html.parser')
		link_es_i = pag_es_bs.find_all('a')
		link_es_f = []
		re_links_es = re.compile(r"/ediario/index.php/component.+")
		for l in link_es_i:
			aux_link = re.search(re_links_es,l['href'])
			if aux_link != None:
				link_es_f.append("https://sistemas.tjes.jus.br"+aux_link.group(0))
		for l in link_es_f:
			try:
				pag_aux = self.baixa_pag(l)
				soup = BeautifulSoup(pag_aux, 'html.parser')
				texto_es_i = soup.get_text()
				texto_es_f = re.search(r"Versão revista(.*?)O e-diário \(Diário da Justiça Eletrônico",texto_es_i,re.DOTALL)
				if texto_es_f != None:
					texto_es_ff = re.sub(r"Versão revista","",texto_es_f.group(0))
					texto_es_ff = re.sub(r"O e-diário \(Diário da Justiça Eletrônico","",texto_es_ff)
					diario_es.write(texto_es_ff)
					diario_es.write("}}")
			except:
				pass
		diario_es.close()
		subprocess.Popen('mv %s/%s*.pdf %s' % (os.getcwd(),self.dia+self.mes+self.ano+"es.txt",path_diarios), shell=True)

	def baixa_go(self):
		pastas = ['6235'] # 2018 e 2019 (nov)
		go_dje = "http://tjdocs.tjgo.jus.br/pastas/"
		for pasta in pastas:
			print('Pasta ',pasta)
			pag_go = self.baixa_pag(go_dje+pasta)
			pag_go_bs = BeautifulSoup(pag_go, 'html.parser')
			link_go_i = pag_go_bs.find_all('a',href=re.compile(r'/pastas/\d+'))
			links_diarios_GO =[]
			for i in link_go_i:
				links_diarios_GO.append(str(i['href']))
			links_diarios_GO = list(set(links_diarios_GO[1:]))
			for link in links_diarios_GO:
				for j in range(1,4):
					pag_diarios_mes = self.baixa_pag('http://tjdocs.tjgo.jus.br%s?page=%s' % (link,str(j)))
					pag_diarios_mes_bs = BeautifulSoup(pag_diarios_mes, 'html.parser')
					links_diarios = pag_diarios_mes_bs.find_all('a',href=re.compile(r'/documentos/\d+'))
					for link_d in links_diarios:
						link_final = 'http://tjdocs.tjgo.jus.br'+link_d['href']+'/download'
						driver = webdriver.Chrome(self.chromedriver)
						driver.get(link_final)
						time.sleep(10)
						driver.close()
						subprocess.Popen('mv %s/*.pdf "%s/Diarios_go/"' % (path,path_diarios), shell=True)

	def baixa_ma(self):
		# if self.data:
		# 	from crawler_jurisprudencia_tjma import crawler_jurisprudencia_tjma
		# 	c = crawler_jurisprudencia_tjma()
		# 	c.download_diario_retroativo(data_especifica=self.dia_pesquisar+self.mes_pesquisar+self.ano_pesquisar)
		# 	return
		ma_dje = "http://www.tjma.jus.br/inicio/diario"
		driver = webdriver.Chrome(self.chromedriver)
		driver.get(ma_dje)
		driver.find_element_by_xpath('//*[@id="btnConsultar"]').click()
		driver.find_element_by_xpath('//*[@id="table1"]/tbody/tr[2]/td[3]/a[1]').click()
		time.sleep(3)
		driver.switch_to.window(driver.window_handles[-1])
		url = driver.current_url
		driver.close()
		print(url)
		response = urllib.request.urlopen(url,timeout=15)
		file = open(str(self.dia+self.mes+self.ano)+"MA.pdf", 'wb')
		time.sleep(1)
		file.write(response.read())
		file.close()

	def baixa_mg(self):
		pass

	def baixa_mt(self):
		dje_mt = "http://www.tjmt.jus.br/dje"
		pag_mt = self.baixa_pag(dje_mt)
		pag_mt_bs = BeautifulSoup(pag_mt,'html.parser')
		link_mt_i = pag_mt_bs.find_all('div', attrs={"class":"cadernos-ultima-edicao"})
		link_mt_f = re.findall(r'href="(.*?)"',str(link_mt_i))
		for l in range(1,len(link_mt_f)):
			link_mt_f[l] = re.sub(r' ','%20',link_mt_f[l])
			link_mt_f[l] = re.sub(r'ç','%C3%A7',link_mt_f[l])
			link_mt_f[l] = re.sub(r'â','%C3%A2',link_mt_f[l])
			link_mt_f[l] = re.sub(r'ª','%C2%AA',link_mt_f[l])
			response = urllib.request.urlopen(link_mt_f[l],timeout=30)
			filename = 'TJMT_'+str(l)+'_'+self.dia+self.mes+self.ano+".pdf"
			file = open(filename, 'wb')
			file.write(response.read())
			file.close()
			time.sleep(5)
			subprocess.Popen('mv %s/*.pdf %s/%s.pdf' % (os.getcwd(),path_diarios,filename), shell=True)

	def baixa_ms(self):
		if self.data:
			from crawler_jurisprudencia_tjms import crawler_jurisprudencia_tjms
			c = crawler_jurisprudencia_tjms()
			c.download_diario_retroativo(data_especifica=self.dia_pesquisar+'/'+self.mes_pesquisar+'/'+self.ano_pesquisar)
		else:
			pag_ms = "https://www.tjms.jus.br/cdje/index.do"
			self.baixaEsaj(3,5,pag_ms)
			subprocess.Popen('mv %s/*.pdf %s/TJCE_%s.pdf' % (path,path_diarios,self.dia+self.mes+self.ano), shell=True)

	def baixa_pa(self):
		pa_dje = "http://dje.tjpa.jus.br/"
		driver = webdriver.Chrome(self.chromedriver)
		driver.get(pa_dje)
		time.sleep(4)
		driver.find_element_by_css_selector("a[ng-click='abrirPDFGrid(urlUltimoDiario)']").click()
		time.sleep(7)
		driver.close()	

	def baixa_pb(self):
		pb_dje = "https://app.tjpb.jus.br/dje/paginas/diario_justica/publico/buscas.jsf"
		driver = webdriver.Chrome(self.chromedriver)
		driver.get(pb_dje)
		driver.find_element_by_xpath("//*[@id=\"dje-pdf-recentes\"]/li[1]/a").click()
		time.sleep(15)
		subprocess.Popen('mv %s/*.pdf %s/TJPB_%s.pdf' % (path,path_diarios,self.dia+self.mes+self.ano), shell=True)

	def baixa_pe(self):
		driver = webdriver.Chrome(self.chromedriver)
		pe_dje = "https://www.tjpe.jus.br/dje/djeletronico?visaoId=tjdf.djeletronico.comum.internet.apresentacao.VisaoDiarioEletronicoInternetPorData"
		pag_pe = self.baixa_pag(pe_dje)
		pag_pe_bs = BeautifulSoup(pag_pe,'html.parser')
		link_pe_i = pag_pe_bs.find('a',attrs={"class":"downloadPdf"})
		link_pe_f = str(link_pe_i['href'])
		driver.get(link_pe_f)
		time.sleep(15)
		subprocess.Popen('mv %s/*.PDF %s/TJPE_%s.pdf' % (path,path_diarios,str(self.dia)+str(self.mes)+str(self.ano)), shell=True)

	def baixa_pi(self):
		if self.data:
			from crawler_jurisprudencia_tjpi import crawler_jurisprudencia_tjpi
			c = crawler_jurisprudencia_tjpi()
			c.download_diario_retroativo(data_especifica=self.dia_pesquisar+self.mes_pesquisar+self.ano_pesquisar)
			return
		pi_dje = "http://www.tjpi.jus.br/site/modules/diario/Init.mtw"
		pag_pi = self.baixa_pag(pi_dje)
		pag_pi_bs = BeautifulSoup(pag_pi,'html.parser')
		link_pi_i = pag_pi_bs.find('a',href=re.compile(r'http://www\.tjpi\.jus\.br/diarioeletronico/public.+'))
		link_pi_f = str(link_pi_i['href'])
		response = urllib.request.urlopen(link_pi_f,timeout=30)
		file7 = open(self.dia+self.mes+self.ano+"PI.pdf", 'wb')
		time.sleep(2)
		file7.write(response.read())
		file7.close()

	def baixa_pr(self):
		pag_pr = "https://portal.tjpr.jus.br/e-dj/publico/diario/pesquisar/filtro.do"
		driver = webdriver.Chrome(self.chromedriver)
		driver.get(pag_pr)
		if self.data:
			driver.find_element_by_name("dataVeiculacao").send_keys(self.dia_pesquisar+'/'+self.mes_pesquisar+'/'+self.ano_pesquisar)
		else:
			driver.find_element_by_name("dataVeiculacao").send_keys(self.dia+'/'+self.mes+'/'+self.ano)
		driver.find_element_by_xpath("//*[@id=\"searchButton\"]").click()
		driver.find_element_by_xpath("//*[@id=\"diarioPesquisaForm\"]/fieldset/table[3]/tbody/tr/td[3]/a").click()
		time.sleep(5)
		if self.data:
			subprocess.Popen('mv %s/*.pdf %s/TJPR_%s.pdf' % (path,path_diarios,self.dia_pesquisar+self.mes_pesquisar+self.ano_pesquisar), shell=True)
		else:
			subprocess.Popen('mv %s/*.pdf %s/TJPR_%s.pdf' % (path,path_diarios,self.dia+self.mes+self.ano), shell=True)

	def baixa_rj(self):
		pass

	def baixa_rn(self):
		if self.data:
			ano = self.ano_pesquisar
			mes = self.mes_pesquisar
			dia = self.dia_pesquisar 
		else:
			ano = self.ano
			mes = self.mes
			dia = self.dia
		tri = "1tri"
		if int(mes)>=4 and int(mes)<=6:
			tri="2tri"
		elif int(mes)>=7 and int(mes)<=9:
			tri="3tri"
		elif int(mes)>=10 and int(mes)<=12:
			tri="4tri"
		rn_dje = "https://www.diario.tjrn.jus.br/"
		driver = webdriver.Chrome(self.chromedriver)
		driver.get(rn_dje)
		driver.find_element_by_xpath("/html/body/table/tbody/tr/td/table/tbody/tr[4]/td/table[2]/tbody/tr/td/div/a").click()
		driver.find_element_by_xpath("//*[@id=\"menu:formMenu:_id16\"]").click()
		driver.find_element_by_xpath("//*[@id=\"pesquisarEdicaoCompletaBean:pesquisa_:_id45\"]").click()
		time.sleep(3)
		link_rn_f = "https://www.diario.tjrn.jus.br/djonline/pages/repositoriopdfs/"+ano+"/"+tri+"/"+ano+mes+dia+"/"+ano+mes+dia+"_JUD.pdf"
		driver.switch_to.window(driver.window_handles[-1])
		driver.get(link_rn_f)
		time.sleep(5)

	def baixa_ro(self):
		response = urllib.request.urlopen('https://portal.tjro.jus.br/diario-api/ultimo-diario.php',timeout=5)
		file = open(self.dia+self.mes+self.ano+"RO.pdf", 'wb')
		time.sleep(1)
		file.write(response.read())
		file.close()
		
	def baixa_rr(self):
		if self.data:
			link_final_rr = "http://diario.tjrr.jus.br/dpj/dpj-"+self.ano_pesquisar+self.mes_pesquisar+self.dia_pesquisar+".pdf"
			file5 = open(self.dia_pesquisar+self.mes_pesquisar+self.ano_pesquisar+"RR.pdf", 'wb')
		else:
			link_final_rr = "http://diario.tjrr.jus.br/dpj/dpj-"+self.ano+self.mes+self.dia+".pdf"
			file5 = open(self.dia+self.mes+self.ano+"RR.pdf", 'wb')
		response = urllib.request.urlopen(link_final_rr,timeout=1)
		time.sleep(1)
		file5.write(response.read())
		file5.close()

	def baixa_rs(self):
		driver = webdriver.Chrome(self.chromedriver)
		rs_dje = "http://www3.tjrs.jus.br/servicos/diario_justica/dj.php"
		pag_rs = self.baixa_pag(rs_dje)
		pag_rs_bs = BeautifulSoup(pag_rs,'html.parser')
		n_edicao_rs = pag_rs_bs.find('select', attrs={"name":"publicacao_edicao"})
		n_edicao_rs_i = re.findall(r'Ed\. \d+',str(n_edicao_rs))
		n_edicao_rs_f = str(n_edicao_rs_i[0][4:])
		lista_rs = ['5','6','7','8']
		for i in lista_rs:
			driver.get("http://www3.tjrs.jus.br/servicos/diario_justica/download_edicao.php?tp="+i+"&ed="+n_edicao_rs_f)
			time.sleep(8)
			subprocess.Popen('mv %s/*.pdf %s/%s.pdf' % (path,path_diarios,i+'_TJRS_'+str(self.dia)+str(self.mes)+str(self.ano)), shell=True)

	def baixa_sc(self):
		sc_dje = "http://busca.tjsc.jus.br/dje-consulta/#/main"
		driver = webdriver.Chrome(self.chromedriver)
		driver.get(sc_dje)
		time.sleep(1)
		driver.find_element_by_xpath("//*[@id=\"div_diarios_publicados\"]/span[2]/span/div/ul/li/span/a").click()
		time.sleep(5)
		driver.switch_to.window(driver.window_handles[-1])
		response = urllib.request.urlopen(driver.current_url,timeout=1)
		file = open('TJSC_'+self.dia+self.mes+self.ano+".pdf", 'wb')
		file.write(response.read())
		file.close()
		subprocess.Popen('mv %s/*.pdf %s' % (os.getcwd(),path_diarios), shell=True)

	def baixa_se(self):
		dje_se = "http://www.diario.tjse.jus.br/diario/internet/pesquisar.wsp?tmp.origem=EXTERNA"
		pag_se = self.baixa_pag(dje_se)
		pag_se_bs = BeautifulSoup(pag_se,'html.parser')
		link_se_i = pag_se_bs.find_all('a', attrs={"href":"#"})
		link_se_f = "http://www.diario.tjse.jus.br/diario/diarios/"+link_se_i[-1].text.split("(")[0]+".pdf"
		response = urllib.request.urlopen(link_se_f.replace('\n',''),timeout=30)
		file = open(self.dia+self.mes+self.ano+"SE.pdf", 'wb')
		time.sleep(5)
		file.write(response.read())
		file.close()
		subprocess.Popen('mv %s/*.pdf %s/TJSE_%s.pdf' % (os.getcwd(),path_diarios,self.dia+self.mes+self.ano), shell=True)

	def baixa_sp(self):
		if self.data:
			from crawler_jurisprudencia_tjsp import crawler_jurisprudencia_tjsp
			c = crawler_jurisprudencia_tjsp()
			c.download_diario_retroativo(data_especifica=self.dia_pesquisar+'/'+self.mes_pesquisar+'/'+self.ano_pesquisar)
		else:
			pag_sp = "http://www.dje.tjsp.jus.br/cdje/index.do"
			self.baixaEsaj(2,7,pag_sp)
			subprocess.Popen('mv %s/*.pdf %s/TJSP_%s.pdf' % (path,path_diarios,self.dia+self.mes+self.ano), shell=True)

	def baixa_stf(self,ultimo_download=191):
		if self.data:
			# PROBLEMA! VERIFICAR SE O DOWNLOAD FOI FEITO. SE ELE FOI, ENTÃO ATUALIZAR ÚLTIMO DOWNLOAD
			link_final_stf = ("https://www.stf.jus.br/arquivo/djEletronico/DJE_%s_%s.pdf" % (self.ano_pesquisar+self.mes_pesquisar+self.dia_pesquisar,ultimo_download))
			response = urllib.request.urlopen(link_final_stf,timeout=15)
			file = open(self.dia_pesquisar+self.mes_pesquisar+self.ano_pesquisar+"STF.pdf", 'wb')
			time.sleep(1)
			file.write(response.read())
			file.close()
		else:
			stf_dje = "http://www.stf.jus.br/portal/diarioJustica/verDiarioAtual.asp"
			pag_stf = self.baixa_pag(stf_dje)
			pag_stf_bs = BeautifulSoup(pag_stf, 'html.parser')
			pag_stf_bs_f = pag_stf_bs.find('th',text=re.compile(r"DJ Nr. \d+"))
			n_diario_stf_i = str(pag_stf_bs_f.text)
			n_diario_stf_f = re.findall(r"\d+",n_diario_stf_i)
			link_final_stf = ("https://www.stf.jus.br/arquivo/djEletronico/DJE_%s_%s.pdf" % (self.ano+self.mes+self.dia,n_diario_stf_f[0]))
			response = urllib.request.urlopen(link_final_stf,timeout=1)
			file = open(self.dia+self.mes+self.ano+"STF.pdf", 'wb')
			time.sleep(1)
			file.write(response.read())
			file.close()

	def baixa_stj(self):
		if self.data:
			link_stj_f = "https://ww2.stj.jus.br/docs_internet/processo/dje/zip/stj_dje_%s.zip" % (self.data,)
			file = open(self.dia_pesquisar+self.mes_pesquisar+self.ano_pesquisar+"STJ.zip", 'wb')
		else:
			link_stj_f = "https://ww2.stj.jus.br/docs_internet/processo/dje/zip/stj_dje_%s.zip" % (self.ano+self.mes+self.dia,)
			file = open(self.dia+self.mes+self.ano+"STJ.zip", 'wb')
		response = urllib.request.urlopen(link_stj_f,timeout=300)
		time.sleep(2)
		file.write(response.read())
		file.close()

	def baixa_to(self):
		link_diario_TO_f = []
		to_dje = "https://wwa.tjto.jus.br/diario/pesquisa"
		pag_to = self.baixa_pag(to_dje)
		pag_to_bs = BeautifulSoup(pag_to,'html.parser')
		link_to_i = pag_to_bs.find('a',href=re.compile('http://wwa\.tjto\.jus\.br/diario/diariopublicado/.+'))
		link_to_f = str(link_to_i['href'])
		link_diario_TO_f.append(link_to_f)
		cont_to = 0
		for lk in link_diario_TO_f: 
			response = urllib.request.urlopen(lk,timeout=5)
			file1 = open(self.dia+self.mes+self.ano+str(cont_to)+"TO.pdf", 'wb')
			time.sleep(1)
			file1.write(response.read())
			file1.close()
			cont_to += 1

	def baixa_trf1(self):
		pag_trf1 = "https://edj.trf1.jus.br/edj/"
		pag_trf1_ini = self.baixa_pag(pag_trf1)
		pag_trf1_ini_bs = BeautifulSoup(pag_trf1_ini,'html.parser')
		links_trf1_i = pag_trf1_ini_bs.find_all('a',href=re.compile(r"/edj/handle/123/.+"))
		links_trf1_i2 = []
		links_trf1_f = []
		for ltrf1 in links_trf1_i[4:]:
			links_trf1_i2.append("https://edj.trf1.jus.br"+str(ltrf1['href']))
		for ltrf1_2 in links_trf1_i2:
			aux_link_trf1 = self.baixa_pag(ltrf1_2)
			aux_link_trf1_bs = BeautifulSoup(aux_link_trf1,'html.parser')
			links_trf1_aux = aux_link_trf1_bs.find('a',href=re.compile(r'/edj/bitstream/handle/123.+'))
			links_trf1_f.append("https://edj.trf1.jus.br"+str(links_trf1_aux['href']))
			cont = 0
		for lk in links_trf1_f: 
			response = urllib.request.urlopen(lk,timeout=5)
			file = open(str(cont)+self.dia+self.mes+self.ano+"TRF1.pdf", 'wb')
			time.sleep(5)
			file.write(response.read())
			file.close()
			cont += 1

	def baixa_trf2(self):
		trf2_dje = "http://dje.trf2.jus.br/DJE/Paginas/Externas/inicial.aspx"
		driver = webdriver.Chrome(self.chromedriver)
		driver.get(trf2_dje)
		driver.find_element_by_xpath("//*[@id=\"ctl00_ContentPlaceHolder_ctrInicial_ctrCadernosPorAreaJudicial_lkbCadJudTRF\"]").click()
		driver.find_element_by_xpath("//*[@id=\"ctl00_ContentPlaceHolder_ctrInicial_ctrCadernosPorAreaJudicial_lkbCadJudSJRJ\"]").click()
		driver.find_element_by_xpath("//*[@id=\"ctl00_ContentPlaceHolder_ctrInicial_ctrCadernosPorAreaJudicial_lkbCadJudSJES\"]").click()
		time.sleep(15)
		subprocess.Popen('mv %s/*.pdf %s' % (path,path_diarios), shell=True)
		
	def baixa_trf3(self):
		trf3_dje = "http://web.trf3.jus.br/diario/Consulta"
		driver = webdriver.Chrome(self.chromedriver)
		driver.get(trf3_dje)
		for i in range(2,3):
			driver.find_element_by_xpath("//*[@id=\"botao-ultima\"]/a").click()
			driver.find_element_by_xpath("//*[@id=\"ultimaEdicao\"]/li["+str(i)+"]/a").click()
			time.sleep(17)
			subprocess.Popen('mv %s/*.pdf %s/TRF3_%s.pdf' % (path,path_diarios,str(i)+self.ano+self.mes+self.dia), shell=True)
		for i in range(3,10):
			driver.find_element_by_xpath("//*[@id=\"botao-ultima\"]/a").click()
			driver.find_element_by_xpath("//*[@id=\"ultimaEdicao\"]/li["+str(i)+"]/a").click()
			time.sleep(10)
			subprocess.Popen('mv %s/*.pdf %s/TRF3_%s.pdf' % (path,path_diarios,str(i)+self.ano+self.mes+self.dia), shell=True)
		driver.close()

	def baixa_trf4(self):
		if self.data:
			ano = self.ano_pesquisar
			mes = self.mes_pesquisar
			dia = self.dia_pesquisar
		else:
			ano = self.ano
			mes = self.mes
			dia = self.dia
		try:
			link_inicial = 'https://www2.trf4.jus.br/trf4/diario/download.php?arquivo=%2Fvar%2Fwww%2Fhtml%2Fdiario%2Fdocsa%2Fde_jud_{}1645{}_{}_a.pdf'
			marcador = {'2018' : '01', '2017' : '01', '2016' : '02', '2015' : '02', '2014' : '02', '2013' : '01', '2012' : '06', '2011' : '01'}
			response = urllib.request.urlopen(link_inicial.format(ano+mes+dia, marcador[ano],ano+'_'+mes+'_'+dia),timeout=5)
			file = open(dia+mes+ano+'.pdf', 'wb')
			file.write(response.read())
			file.close()
			subprocess.Popen('mv %s/*.pdf %s/TRF4_%s' % (os.getcwd(),path_diarios,dia+mes+ano), shell=True)
		except Exception as e:
			print(e)

	def baixa_trf5(self):
		from selenium.webdriver.support.ui import Select
		orgaos_trf5 = ['TRIBUNAL REGIONAL FEDERAL DA 5ª REGIÃO','Seção Judiciária de Alagoas','Seção Judiciária do Ceará','Seção Judiciária da Paraíba','Seção Judiciária de Pernambuco',\
		'Seção Judiciária do Rio Grande do Norte','Seção Judiciária do sergipe']
		def trf5_baixa_diarios(orgao):  
			driver = webdriver.Chrome(self.chromedriver)
			trf5_dje = "https://www4.trf5.jus.br/diarioeletinternet/"
			driver.get(trf5_dje)
			org_trf5 = Select(driver.find_element_by_id("frmVisao:orgao"))
			edicao_trf5_opt = Select(driver.find_element_by_id("frmVisao:edicao"))
			ano_trf5_opt = Select(driver.find_element_by_id("frmVisao:periodo"))
			org_trf5.select_by_visible_text(orgao)
			edicao_trf5_opt.select_by_visible_text('Judicial')
			ano_trf5_opt.select_by_visible_text(self.ano)
			time.sleep(1)
			driver.find_element_by_xpath("//*[@id=\"frmVisao:j_id48\"]").click()
			time.sleep(1)
			driver.execute_script("return oamSubmitForm('frmPesquisa','frmPesquisa:tDiarios:0:j_id67','_blank',[]);")
			time.sleep(3)
			driver.close()
		for o in orgaos_trf5:
			try:
				trf5_baixa_diarios(o)
				subprocess.Popen('mv %s/Diário.pdf "%s/%s.pdf"' % (path,path_diarios,o.replace(' ','')+str(self.dia)+str(self.mes)+str(self.ano)), shell=True)
			except Exception as e:
				print(e)

	def baixa_trt(self):
		dje_trt = 'https://aplicacao.jt.jus.br/dejt.html'
		links_trt = [
		'https://aplicacao.jt.jus.br/Diario_J_TST.pdf',
		'https://aplicacao.jt.jus.br/Diario_J_01.pdf',
		'https://aplicacao.jt.jus.br/Diario_J_02.pdf',
		'https://aplicacao.jt.jus.br/Diario_J_03.pdf',
		'https://aplicacao.jt.jus.br/Diario_J_04.pdf',
		'https://aplicacao.jt.jus.br/Diario_J_05.pdf',
		'https://aplicacao.jt.jus.br/Diario_J_06.pdf',
		'https://aplicacao.jt.jus.br/Diario_J_07.pdf',
		'https://aplicacao.jt.jus.br/Diario_J_08.pdf',
		'https://aplicacao.jt.jus.br/Diario_J_09.pdf',
		'https://aplicacao.jt.jus.br/Diario_J_10.pdf',
		'https://aplicacao.jt.jus.br/Diario_J_11.pdf',
		'https://aplicacao.jt.jus.br/Diario_J_12.pdf',
		'https://aplicacao.jt.jus.br/Diario_J_13.pdf',
		'https://aplicacao.jt.jus.br/Diario_J_14.pdf',
		'https://aplicacao.jt.jus.br/Diario_J_15.pdf',
		'https://aplicacao.jt.jus.br/Diario_J_16.pdf',
		'https://aplicacao.jt.jus.br/Diario_J_17.pdf',
		'https://aplicacao.jt.jus.br/Diario_J_18.pdf',
		'https://aplicacao.jt.jus.br/Diario_J_19.pdf',
		'https://aplicacao.jt.jus.br/Diario_J_20.pdf',
		'https://aplicacao.jt.jus.br/Diario_J_21.pdf',
		'https://aplicacao.jt.jus.br/Diario_J_22.pdf',
		'https://aplicacao.jt.jus.br/Diario_J_23.pdf',
		'https://aplicacao.jt.jus.br/Diario_J_24.pdf'
		]
		response = urllib.request.urlopen(links_trt[0],timeout=1)
		file = open('Diario_TST_%s.pdf' % (self.dia+self.mes+self.ano,), 'wb')
		file.write(response.read())
		file.close()
		subprocess.Popen('mv %s/*.pdf %s/%s' % (os.getcwd(),path_diarios,'Diario_TST_%s.pdf' % (self.dia+self.mes+self.ano,)), shell=True)
		for l in range(1,len(links_trt)):
			response = urllib.request.urlopen(links_trt[l],timeout=1)
			filename = 'TRT_%s.pdf' % (str(l)+'_'+self.dia+self.mes+self.ano,)
			file = open(filename, 'wb')
			file.write(response.read())
			file.close()
			subprocess.Popen('mv %s/*.pdf %s/%s' % (os.getcwd(),path_diarios,filename), shell=True)


if __name__ == '__main__':
	# publicacoes = publicacoes_diarios_oficiais(data='20190902')
	
	# publicacoes = publicacoes_diarios_oficiais()
	
	# publicacoes.baixa_ac(todos=True)
	
	# for d in publicacoes.diarios_a_baixar:
	# 	d()

	# pub = publicacoes_diarios_oficiais()
	# pub.baixa_go()

	chromedriver = os.getcwd()+"/chromedriver"
	datas_p = []
	for i in range(1,32):
		dia = str(i)
		if len(dia) == 1:
			dia = '0'+str(i)
		for j in range(1,13):
			mes = str(j)
			if len(mes) == 1:
				mes = '0'+str(j)
			for k in range(2018,2020):
				datas_p.append(dia+'/'+mes+'/'+str(k))
	for data_p in datas_p[3:]:
		driver = webdriver.Chrome(chromedriver)
		driver.get('https://esaj.tjms.jus.br/cdje/index.do')
		for i in range(2,4):
			driver.execute_script("popup('/cdje/downloadCaderno.do?dtDiario=%s'+'&cdCaderno=%s&tpDownload=D','cadernoDownload');" % (data_p, str(i)))
			time.sleep(8)
			nome_pasta = data_p.replace('/','')
			subprocess.Popen('mkdir "%s/Diarios_ms/%s"' % (path_diarios,nome_pasta), shell=True) 
			subprocess.Popen('mv %s/*.pdf "%s/Diarios_ms/%s/"' % (path,path_diarios,nome_pasta), shell=True)
		driver.quit()