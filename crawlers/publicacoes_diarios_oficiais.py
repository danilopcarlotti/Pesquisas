import re, os, sys, time, datetime, urllib.request, ssl
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from crawlerJus import crawlerJus

ssl._create_default_https_context = ssl._create_unverified_context

links_diarios = []

class publicacoes_diarios_oficiais(crawlerJus):
    """docstring for ClassName"""
    def __init__(self):
        crawlerJus.__init__(self)
        logging.basicConfig(filename=self.cwd+'/publicacoes_'+self.dia+self.mes+self.ano+'.log',level=logging.INFO)
        self.diarios_a_baixar = [self.baixa_stf,self.baixa_ro,self.baixa_rr,self.baixa_pa,self.baixa_ma,self.baixa_to,self.baixa_pi,self.baixa_stj,self.baixa_trf1,\
        self.baixa_trf5,self.baixa_go,self.baixa_rs,self.baixa_ac,self.baixa_trf4,self.baixa_df,self.baixa_sc,self.baixa_rn,self.baixa_trf3,self.baixa_pe,\
        self.baixa_sp,self.baixa_ce,self.baixa_al,self.baixa_ms,self.baixa_am,self.baixa_pr,self.baixa_trt,self.baixa_es,self.baixa_ap,self.baixa_pb,self.baixa_se,\
        self.baixa_mt,self.baixa_trf2]        

    def baixa_stf(self):
        stf_dje = "http://www.stf.jus.br/portal/diarioJustica/verDiarioAtual.asp"
        pag_stf = self.baixa_pag(stf_dje)
        pag_stf_bs = BeautifulSoup(pag_stf, 'html.parser')
        pag_stf_bs_f = pag_stf_bs.find('th',text=re.compile(r"DJ Nr. \d+"))
        n_diario_stf_i = str(pag_stf_bs_f.text)
        n_diario_stf_f = re.findall(r"\d+",n_diario_stf_i)
        link_final_stf = ("https://www.stf.jus.br/arquivo/djEletronico/DJE_%s_%s.pdf" % (self.ano+self.mes+self.dia,n_diario_stf_f[0]))
        response = urllib.request.urlopen(link_final_stf,timeout=1)
        file1 = open(self.dia+self.mes+self.ano+"STF.pdf", 'wb')
        time.sleep(1)
        file1.write(response.read())
        file1.close()

    def baixa_ro(self):
        ro_dje = "https://www.tjro.jus.br/novodiario/"
        pag_ro = self.baixa_pag(ro_dje)
        pag_ro_bs = BeautifulSoup(pag_ro,'html.parser')
        find_ro = ano+"/"+self.ano+self.mes+self.dia
        link_final_ro_i = pag_ro_bs.find('a',href=re.compile(find_ro))
        link_final_ro_f = "https://www.tjro.jus.br/novodiario/"+str(link_final_ro_i['href'])
        response = urllib.request.urlopen(link_final_ro_f,timeout=1)
        file4 = open(self.dia+self.mes+self.ano+"RO.pdf", 'wb')
        time.sleep(1)
        file4.write(response.read())
        file4.close()
        
    def baixa_rr(self):
        link_final_rr = "http://diario.tjrr.jus.br/dpj/dpj-"+self.ano+self.mes+self.dia+".pdf"
        response = urllib.request.urlopen(link_final_rr,timeout=1)
        file5 = open(self.dia+self.mes+self.ano+"RR.pdf", 'wb')
        time.sleep(1)
        file5.write(response.read())
        file5.close()

    def baixa_pa(self):
        pa_dje = "http://dje.tjpa.jus.br/"
        pag_pa = self.baixa_pag(pa_dje)
        pag_pa_bs = BeautifulSoup(pag_pa,'html.parser')
        link_pa_i = pag_pa_bs.find('a',href=re.compile('.+DownloadDeDiario\.jsp.+'))
        link_pa_f = str(link_pa_i['href'])
        response = urllib.request.urlopen(link_pa_f,timeout=1)
        file9 = open(self.dia+self.mes+self.ano+"PA.pdf", 'wb')
        time.sleep(1)
        file9.write(response.read())
        file9.close()

    def baixa_ma(self):
        ma_dje = "http://www.tjma.jus.br/inicio/diario"
        driver = webdriver.Chrome(self.chromedriver)
        driver.get(ma_dje)
        driver.find_element_by_xpath('//*[@id="btnConsultar"]').click()
        driver.find_element_by_xpath('//*[@id="table1"]/tbody/tr[2]/td[3]/a[1]').click()
        time.sleep(1)

    def baixa_to(self):
        link_diario_TO_f = []
        to_dje = "http://wwa.tjto.jus.br/consultadiario/Inicio_lista.aspx"
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

    def baixa_pi(self):
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

    def baixa_stj(self):
        link_stj_f = "http://dj.stj.jus.br/"+self.ano+self.mes+self.dia+".pdf"
        response = urllib.request.urlopen(link_stj_f,timeout=30)
        file2 = open(self.dia+self.mes+self.ano+"STJ.pdf", 'wb')
        time.sleep(2)
        file2.write(response.read())
        file2.close()

    def baixa_trf1(self):
        pag_trf1 = "https://edj.trf1.jus.br/edj/handle/123/471"
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
            file1 = open(str(cont)+self.dia+self.mes+self.ano+"TRF1.pdf", 'wb')
            time.sleep(5)
            file1.write(response.read())
            file1.close()
            cont += 1

    def baixa_trf5(self):
        from selenium.webdriver.support.ui import Select
        orgaos_trf5 = ['TRIBUNAL REGIONAL FEDERAL DA 5ª REGIÃO','Seção Judiciária de Alagoas','Seção Judiciária do Ceará','Seção Judiciária da Paraíba','Seção Judiciária de Pernambuco',\
        'Seção Judiciária do Rio Grande do Norte','Seção Judiciária do sergipe']
        def trf5_baixa_diarios(orgao):  
            driver = webdriver.Chrome(self.chromedriver)
            trf5_dje = "https://www.trf5.jus.br/diarioeletinternet/"
            driver.get(trf5_dje)
            org_trf5 = Select(driver.find_element_by_id("frmVisao:orgao"))
            edicao_trf5_opt = Select(driver.find_element_by_id("frmVisao:edicao"))
            ano_trf5_opt = Select(driver.find_element_by_id("frmVisao:periodo"))
            org_trf5.select_by_visible_text(orgao)
            edicao_trf5_opt.select_by_visible_text('Judicial')
            ano_trf5_opt.select_by_visible_text(self.ano)
            time.sleep(1)
            mes_trf5_lista = []
            mes_trf5_opt = Select(driver.find_element_by_id("frmVisao:meses"))
            for i in mes_trf5_opt.options:
                mes_trf5_lista.append(i.text)
                mes_trf5 = mes_trf5_lista[int(mes)]
                mes_trf5_opt.select_by_visible_text(mes_trf5)
                driver.find_element_by_xpath("//*[@id=\"frmVisao:j_id48\"]").click()
                time.sleep(1)
                driver.find_element_by_xpath("//*[@id=\"frmPesquisa:tDiarios:0:j_id64\"]/a/img").click()
                time.sleep(1)
            driver.close()
        for o in orgaos_trf5:
            try:
                trf5_baixa_diarios(o)
            except:
                pass

    def baixa_go(self):
        go_dje = "http://www.tjgo.jus.br/index.php/tribunal/tribunal-servicos/tribunal-servicos-djeletronico"
        pag_go = self.baixa_pag(go_dje)
        pag_go_bs = BeautifulSoup(pag_go, 'html.parser')
        link_go_i = pag_go_bs.find_all('a',href=re.compile(r'https://www\.tjgo\.jus\.br/docs/servicos/diariodajustica/.+'))
        links_diarios_GO =[]
        for i in link_go_i:
            links_diarios_GO.append(str(i['href']))
        cont = 0
        for lk in links_diarios_GO:
            response = urllib.request.urlopen(lk,timeout=5)
            file1 = open(str(cont)+self.dia+self.mes+self.ano+"GO.pdf", 'wb')
            time.sleep(1)
            file1.write(response.read())
            file1.close()
            cont += 1

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

    def baixa_ac(self):
        driver = webdriver.Chrome(self.chromedriver)
        ac_dje = "http://diario.tjac.jus.br/edicoes.php"
        pag_ac = self.baixa_pag(ac_dje)
        pag_ac_bs = BeautifulSoup(pag_ac,'html.parser')
        link_ac_i = pag_ac_bs.find('a',attrs={'title':'Baixar'})
        link_ac_f = "http://diario.tjac.jus.br"+str(link_ac_i['href'])
        driver.get(link_ac_f)

    def baixa_trf4(self):
        driver = webdriver.Chrome(self.chromedriver)
        trf4_dje = "http://www2.trf4.jus.br/trf4/diario/consulta_diario.php"
        pag_trf4 = self.baixa_pag(trf4_dje)
        pag_trf4_bs = BeautifulSoup(pag_trf4,'html.parser')
        link_trf4_i = pag_trf4_bs.find_all('td',attrs={"width":"48%"})
        link_trf4_i_2 = re.findall(r"href=.+\.pdf\"",str(link_trf4_i[0]),re.DOTALL)
        link_trf4_f = "http://www2.trf4.jus.br/trf4/diario/"+link_trf4_i_2[0][6:len(link_trf4_i_2[0])-1]
        driver.get(link_trf4_f)

    def baixa_df(self):
        driver = webdriver.Chrome(self.chromedriver)
        df_dje = "https://tjdf199.tjdft.jus.br/dje/djeletronico?visaoId=tjdf.djeletronico.comum.internet.apresentacao.VisaoDiarioEletronicoInternetPorData"
        pag_df = self.baixa_pag(df_dje)
        pag_df_bs = BeautifulSoup(pag_df,'html.parser')
        link_df_i = pag_df_bs.find('a',href=re.compile('http://tjdf11\.tjdft\.jus\.br:.+'))
        link_df_f = str(link_df_i['href'])
        driver.get(link_df_f)

    def baixa_pe(self):
        driver = webdriver.Chrome(self.chromedriver)
        pe_dje = "https://www.tjpe.jus.br/dje/djeletronico?visaoId=tjdf.djeletronico.comum.internet.apresentacao.VisaoDiarioEletronicoInternetPorData"
        pag_pe = self.baixa_pag(pe_dje)
        pag_pe_bs = BeautifulSoup(pag_pe,'html.parser')
        link_pe_i = pag_pe_bs.find('a',attrs={"class":"downloadPdf"})
        link_pe_f = str(link_pe_i['href'])
        driver.get(link_pe_f)

    def baixa_sc(self):
        sc_dje = "http://busca.tjsc.jus.br/dje-consulta/#/main"
        driver = webdriver.Chrome(self.chromedriver)
        driver.get(sc_dje)
        time.sleep(1)
        driver.find_element_by_xpath("//*[@id=\"div_diarios_publicados\"]/span[2]/span/div/ul/li/span/a").click()
        time.sleep(1)

    def baixa_rn(self):
        tri = "1tri"
        if int(mes)>=4 and int(mes)<=6:
            tri="2tri"
        elif int(mes)>=7 and int(mes)<=9:
            tri="3tri"
        elif int(mes)>=10 and int(mes)<=12:
            tri="4tri"
        link_rn_f = "https://www.diario.tjrn.jus.br/djonline/pages/repositoriopdfs/"+self.ano+"/"+tri+"/"+self.ano+self.mes+self.dia+"/"+self.ano+self.mes+self.dia+"_JUD.pdf"
        rn_dje = "https://www.diario.tjrn.jus.br/"
        driver = webdriver.Chrome(self.chromedriver)
        driver.get(rn_dje)
        driver.find_element_by_xpath("/html/body/table/tbody/tr/td/table/tbody/tr[4]/td/table[2]/tbody/tr/td/div/a").click()
        driver.find_element_by_xpath("//*[@id=\"menu:formMenu:_id16\"]").click()
        driver.find_element_by_xpath("//*[@id=\"pesquisarEdicaoCompletaBean:pesquisa_:_id45\"]").click()
        time.sleep(1)
        driver.get(link_rn_f)
        response3 = urllib.request.urlopen(link_rn_f,timeout=1)
        file3 = open(self.dia+self.mes+self.ano+"RN.pdf", 'wb')
        time.sleep(1)
        file3.write(response3.read())
        file3.close()

    def baixa_trf3(self):
        trf3_dje = "http://web.trf3.jus.br/diario/Consulta"
        driver = webdriver.Chrome(self.chromedriver)
        driver.get(trf3_dje)
        for i in range(2,10):
            driver.find_element_by_xpath("//*[@id=\"botao-ultima\"]/a").click()
            driver.find_element_by_xpath("//*[@id=\"ultimaEdicao\"]/li["+str(i)+"]/a").click()
            time.sleep(5)
        driver.close()

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

    def baixa_al(self):
        pag_al = "http://www2.tjal.jus.br/cdje/index.do"
        baixaEsaj(1,3,pag_al)

    def baixa_sp(self):
        pag_sp = "http://www.dje.tjsp.jus.br/cdje/index.do"
        baixaEsaj(2,7,pag_sp)
        
    def baixa_ce(self):
        pag_ce = "http://esaj.tjce.jus.br/cdje/index.do"
        baixaEsaj(2,3,pag_ce)

    def baixa_ms(self):
        pag_ms = "https://www.tjms.jus.br/cdje/index.do"
        baixaEsaj(3,5,pag_ms)

    def baixa_am(self):
        pag_am = "http://consultasaj.tjam.jus.br/cdje/index.do"
        baixaEsaj(2,5,pag_am)

    def baixa_pr(self):
        pag_pr = "https://portal.tjpr.jus.br/e-dj/publico/diario/pesquisar/filtro.do"
        driver = webdriver.Chrome(self.chromedriver)
        driver.get(pag_pr)
        driver.find_element_by_name("dataVeiculacao").send_keys("09/08/2016")
        driver.find_element_by_xpath("//*[@id=\"searchButton\"]").click()
        driver.find_element_by_xpath("//*[@id=\"diarioPesquisaForm\"]/fieldset/table[3]/tbody/tr/td[3]/a").click()
        time.sleep(15)

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
        file = open('Diario_TST.pdf', 'wb')
        file.write(response.read())
        file.close()
        for l in range(1,len(links_trt)):
            response = urllib.request.urlopen(links_trt[l],timeout=1)
            file = open('Diario_J_'+str(l)+"_TRT.pdf", 'wb')
            file.write(response.read())
            file.close()

    def baixa_ap(self):
        ap_dje = "http://app.tjap.jus.br/tucujuris/publico/dje/"
        driver = webdriver.Chrome(self.chromedriver)
        driver.get(ap_dje)
        driver.find_element_by_xpath("//*[@id=\"formLista\"]/table/tbody/tr[1]/td[3]/a").click()
        time.sleep(5)

    def baixa_pb(self):
        pb_dje = "https://app.tjpb.jus.br/dje/paginas/diario_justica/publico/buscas.jsf"
        driver = webdriver.Chrome(self.chromedriver)
        driver.get(pb_dje)
        driver.find_element_by_xpath("//*[@id=\"dje-pdf-recentes\"]/li[1]/a").click()
        time.sleep(5)

    def baixa_se(self):
        dje_se = "http://www.diario.tjse.jus.br/diario/internet/pesquisar.wsp?tmp.origem=EXTERNA"
        pag_se = self.baixa_pag(dje_se)
        pag_se_bs = BeautifulSoup(pag_se,'html.parser')
        link_se_i = pag_se_bs.find_all('a', attrs={"href":"#"})
        link_se_f = "http://www.diario.tjse.jus.br/diario/diarios/"+link_se_i[-1].text.split("(")[0]+".pdf"
        response4 = urllib.request.urlopen(link_se_f,timeout=30)
        file4 = open(self.dia+self.mes+self.ano+"SE.pdf", 'wb')
        time.sleep(5)
        file4.write(response4.read())
        file4.close()

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
            response4 = urllib.request.urlopen(link_mt_f[l],timeout=30)
            file4 = open(str(l)+self.dia+self.mes+self.ano+"MT.pdf", 'wb')
            time.sleep(15)
            file4.write(response4.read())
            file4.close()

    def baixa_trf2(self):
        trf2_dje = "http://dje.trf2.jus.br/DJE/Paginas/Externas/inicial.aspx"
        driver = webdriver.Chrome(self.chromedriver)
        driver.get(trf2_dje)
        driver.find_element_by_xpath("//*[@id=\"ctl00_ContentPlaceHolder_ctrInicial_ctrCadernosPorAreaJudicial_lkbCadJudTRF\"]").click()
        driver.find_element_by_xpath("//*[@id=\"ctl00_ContentPlaceHolder_ctrInicial_ctrCadernosPorAreaJudicial_lkbCadJudSJRJ\"]").click()
        driver.find_element_by_xpath("//*[@id=\"ctl00_ContentPlaceHolder_ctrInicial_ctrCadernosPorAreaJudicial_lkbCadJudSJES\"]").click()
        time.sleep(15)

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

    def baixa_ba(self):
        pass

    # FALTA MG, RJ, BA

if __name__ == '__main__':
    publicacoes = publicacoes_diarios_oficiais()
    for d in publicacoes.diarios_a_baixar:
        publicacoes.baixa_diario(d)