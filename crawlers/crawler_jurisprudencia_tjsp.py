import sys, re, os, time, subprocess, urllib.request
from bs4 import BeautifulSoup
from common.conexao_local import cursorConexao
from common.download_path import path, path_hd
from common.download_path_diarios import path as path_diarios
from crawler_jurisprudencia_tj import crawler_jurisprudencia_tj
from crawlerJus import crawlerJus
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

sys.path.append(os.path.dirname(os.getcwd()))
from common_nlp.parse_texto import busca
from common_nlp.pdf_to_text import pdf_to_text


class crawler_jurisprudencia_tjsp(crawler_jurisprudencia_tj):
    """Crawler especializado em retornar textos da jurisprudência de segunda instância de São Paulo"""

    def __init__(self):
        crawler_jurisprudencia_tj.__init__(self)
        self.link_inicial = "https://esaj.tjsp.jus.br/cjsg/consultaCompleta.do"
        self.pesquisa_livre = '//*[@id="iddados.buscaInteiroTeor"]'
        self.data_julgamento_inicialXP = '//*[@id="iddados.dtJulgamentoInicio"]'
        self.data_julgamento_finalXP = '//*[@id="iddados.dtJulgamentoFim"]'
        self.botao_pesquisar = '//*[@id="pbSubmit"]'
        self.botao_proximo_ini = (
            '//*[@id="paginacaoSuperior-A"]/table/tbody/tr[1]/td[2]/div/a[5]'
        )
        self.botao_proximo = (
            '//*[@id="paginacaoSuperior-A"]/table/tbody/tr[1]/td[2]/div/a[6]'
        )
        self.tabela_colunas = "justica_estadual.jurisprudencia_sp (ementas)"
        self.tabela_colunas_1_inst = (
            "justica_estadual.jurisprudencia_sp_1_inst (sentenca)"
        )
        self.link_esaj = (
            "https://esaj.tjsp.jus.br/cjsg/getArquivo.do?cdAcordao=%s&cdForo=%s"
        )

    def download_1_inst(self, data_ini, data_fim, termo="a"):
        botao_proximo = '//*[@id="resultados"]/table[1]/tbody/tr[1]/td[2]/div/a[6]'
        botao_proximo_ini = '//*[@id="resultados"]/table[1]/tbody/tr[1]/td[2]/div/a[5]'
        data_ini_xpath = '//*[@id="iddadosConsulta.dtInicio"]'
        data_fim_xpath = '//*[@id="iddadosConsulta.dtFim"]'
        link = "https://esaj.tjsp.jus.br/cjpg/pesquisar.do"
        pesquisa_xpath = '//*[@id="iddadosConsulta.pesquisaLivre"]'
        cursor = cursorConexao()
        driver = webdriver.Chrome(self.chromedriver)
        driver.get(link)
        driver.find_element_by_xpath(pesquisa_xpath).send_keys(termo)
        driver.find_element_by_xpath(data_ini_xpath).send_keys(data_ini)
        driver.find_element_by_xpath(data_fim_xpath).send_keys(data_fim)
        driver.find_element_by_xpath(self.botao_pesquisar).click()
        time.sleep(1)
        texto = crawler_jurisprudencia_tj.extrai_texto_html(
            self, (driver.page_source)
        ).replace('"', "")
        cursor.execute(
            'INSERT INTO %s value ("%s");' % (self.tabela_colunas_1_inst, texto)
        )
        driver.find_element_by_xpath(botao_proximo_ini).click()
        time.sleep(1)
        texto = crawler_jurisprudencia_tj.extrai_texto_html(
            self, (driver.page_source)
        ).replace('"', "")
        cursor.execute(
            'INSERT INTO %s value ("%s");' % (self.tabela_colunas_1_inst, texto)
        )
        contador = 3
        while contador:
            try:
                driver.find_element_by_xpath(botao_proximo).click()
                time.sleep(2.5)
                texto = crawler_jurisprudencia_tj.extrai_texto_html(
                    self, (driver.page_source)
                ).replace('"', "")
                cursor.execute(
                    'INSERT INTO %s value ("%s");' % (self.tabela_colunas_1_inst, texto)
                )
                contador = 3
            except:
                time.sleep(2)
                contador -= 1
        driver.close()

    def download_acordao_sp(self, dados_baixar):
        crawler_jurisprudencia_tj.download_pdf_acordao_captcha_image(
            self,
            dados_baixar,
            '//*[@id="valorCaptcha"]',
            '//*[@id="pbEnviar"]',
            "sp_2_inst",
        )
        subprocess.Popen(
            "mv %s/sp_2_inst_*.pdf %s/sp_2_inst" % (path, path), shell=True
        )

    def download_diario_retroativo(self, data_especifica=None):
        cadernos = ["11", "12", "13", "15"]
        datas = []
        if data_especifica:
            datas.append(data_especifica)
        else:
            for l in range(len(self.lista_anos)):
                for i in range(1, 10):
                    for j in range(1, 10):
                        datas.append(
                            "0" + str(j) + "/0" + str(i) + "/" + self.lista_anos[l]
                        )
                    for j in range(10, 32):
                        datas.append(str(j) + "/0" + str(i) + "/" + self.lista_anos[l])
                for i in range(10, 13):
                    for j in range(1, 10):
                        datas.append(
                            "0" + str(j) + "/" + str(i) + "/" + self.lista_anos[l]
                        )
                    for j in range(10, 32):
                        datas.append(str(j) + "/" + str(i) + "/" + self.lista_anos[l])
        for data in datas:
            try:
                driver = webdriver.Chrome(self.chromedriver)
                driver.get("https://www.dje.tjsp.jus.br/cdje/index.do")
                print(data)
                for caderno in cadernos:
                    driver.execute_script(
                        "popup('/cdje/downloadCaderno.do?dtDiario=%s'+'&cdCaderno=%s','cadernoDownload');"
                        % (data, caderno)
                    )
                    time.sleep(1)
                time.sleep(30)
                nome_pasta = data.replace("/", "")
                subprocess.Popen(
                    'mkdir "%s/Diarios_sp/%s"' % (path_diarios, nome_pasta), shell=True
                )
                subprocess.Popen(
                    'mv %s/*.pdf "%s/Diarios_sp/%s"' % (path, path_diarios, nome_pasta),
                    shell=True,
                )
                driver.quit()
            except Exception as e:
                print(e)
                time.sleep(3)

    # Só funciona para a edição da cidade de jun/2017 e para as edições de 2018
    # REVER PARA OUTROS DIÁRIOS
    def download_diario_oficial_adm_retroativo(self):
        link = "http://diariooficial.imprensaoficial.com.br/doflash/prototipo/%s/%s/%s/%s/pdf/pg_%s.pdf"
        diarios = ["exce1", "exec2", "legislativo", "cidade"]
        for a in range(len(self.lista_anos) - 2, len(self.lista_anos)):
            for m in self.lista_meses_nomes:
                for d in range(1, 32):
                    diretorio = False
                    for diario in diarios:
                        for p in range(1, 10000):
                            nome_pasta = str(d) + m + self.lista_anos[a]
                            try:
                                response = urllib.request.urlopen(
                                    link
                                    % (
                                        self.lista_anos[a],
                                        m,
                                        str(d),
                                        diario,
                                        "0" * (4 - len(str(p))) + str(p),
                                    ),
                                    timeout=5,
                                )
                                file = open(nome_pasta + "_" + str(p) + ".pdf", "wb")
                                time.sleep(1)
                                file.write(response.read())
                                file.close()
                                if not diretorio:
                                    subprocess.Popen(
                                        "mkdir %s/Diarios_sp_DO/%s"
                                        % (path_hd, nome_pasta),
                                        shell=True,
                                    )
                                    for diario_pasta in diarios:
                                        subprocess.Popen(
                                            "mkdir %s/Diarios_sp_DO/%s/%s"
                                            % (path_hd, nome_pasta, diario_pasta),
                                            shell=True,
                                        )
                                    diretorio = True
                                subprocess.Popen(
                                    "mv %s/*.pdf %s/Diarios_sp_DO/%s/%s"
                                    % (os.getcwd(), path_hd, nome_pasta, diario_pasta),
                                    shell=True,
                                )
                                time.sleep(1)
                            except Exception as e:
                                print(nome_pasta)
                                print(e)
                                break

    def download_diario_oficial_adm_retrativo_antigos(self):
        crawler_aux = crawlerJus()
        datas = []
        diarios = [
            "Executivo+I",
            "Executivo+II",
            "Empresarial",
            "Empresarial+2",
            "Legislativo",
        ]
        diarios_secao = {
            "Executivo+I": "i",
            "Executivo+II": "ii",
            "Empresarial": None,
            "Empresarial+2": None,
            "Legislativo": None,
        }
        link_inicial = "https://www.imprensaoficial.com.br/DO/BuscaDO2001Resultado_11_3.aspx?filtrotipopalavraschavesalvar=FE&filtrodatafimsalvar={}&filtroperiodo={}%2f{}%2f{}+a+{}%2f{}%2f{}&filtrocadernos={}&filtropalavraschave=+&filtrodatainiciosalvar={}s&xhitlist_vpc=first&filtrocadernossalvar=ex1&filtrotodoscadernos=+"
        primeiro_resultado_xpath = '//*[@id="dtgResultado_lblData_0"]'
        profile = {
            "plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}],
            "download.default_directory": path,
            "download.extensions_to_open": "",
        }
        for i in range(6, 10):
            # for j in range(1,10):
            # 	datas.append('2013'+'0'+str(i)+'0'+str(j))
            for j in range(26, 32):
                datas.append("2013" + "0" + str(i) + str(j))
        for i in range(10, 13):
            for j in range(1, 10):
                datas.append("2013" + str(i) + "0" + str(j))
            for j in range(28, 32):
                datas.append("2013" + str(i) + str(j))
        for l in range(2012, 1890, -1):
            for i in range(1, 10):
                for j in range(1, 10):
                    datas.append(str(l) + "0" + str(i) + "0" + str(j))
                for j in range(10, 32):
                    datas.append(str(l) + "0" + str(i) + str(j))
            for i in range(10, 13):
                for j in range(1, 10):
                    datas.append(str(l) + str(i) + "0" + str(j))
                for j in range(10, 32):
                    datas.append(str(l) + str(i) + str(j))
        for data in datas:
            ano = data[:4]
            mes = data[4:6]
            dia = data[6:]
            nome_pasta = dia + mes + ano
            subprocess.Popen(
                "mkdir %s/Diarios_sp_DO_2/%s" % (path_hd, nome_pasta), shell=True
            )
            for diario in diarios:
                subprocess.Popen(
                    "mkdir %s/Diarios_sp_DO_2/%s/%s" % (path_hd, nome_pasta, diario),
                    shell=True,
                )
                try:
                    options = webdriver.ChromeOptions()
                    options.add_experimental_option("prefs", profile)
                    driver = webdriver.Chrome(self.chromedriver, chrome_options=options)
                    driver.get(
                        link_inicial.format(
                            data, dia, mes, ano, dia, mes, ano, diario, data
                        )
                    )
                    html = driver.page_source
                    pag = BeautifulSoup(html, "lxml")
                    for l in pag.find_all("a", href=True):
                        if re.search(
                            r"javascript\:pop\('\/DO\/BuscaDO2001Documento\_", l["href"]
                        ):
                            codigo_script = re.search(r"pagnot(.*?)\.", l["href"])
                            if codigo_script:
                                codigo_script = codigo_script.group(1)
                                break
                    script_base = "pop('/DO/BuscaDO2001Documento_11_4.aspx?link=%2f{}%2f{}%2520secao%2520{}%2f{}%2f{}%2fpagnot{}.pdf&pagina=I&data={}/{}/{}&caderno={}&paginaordenacao=1',738,577,'0','1')"
                    script_base_sem_secao = "pop('/DO/BuscaDO2001Documento_11_4.aspx?link=%2f{}%2f{}%25202%2f{}%2f{}%2fpag{}.pdf&pagina=1&data={}/{}/{}&caderno={}&paginaordenacao=100001',738,577,'0','1');"
                    if diarios_secao[diario]:
                        driver.execute_script(
                            script_base.format(
                                ano,
                                diario.replace("+", "")
                                .replace("I", "")
                                .replace("2", "")
                                .lower(),
                                diarios_secao[diario],
                                crawler_aux.mes_numero_nome(mes),
                                dia,
                                codigo_script,
                                dia,
                                mes,
                                ano,
                                diario.replace("+", " "),
                            )
                        )
                    else:
                        driver.execute_script(
                            script_base_sem_secao.format(
                                ano,
                                diario.replace("+", "")
                                .replace("I", "")
                                .replace("2", "")
                                .lower(),
                                crawler_aux.mes_numero_nome(mes),
                                dia,
                                codigo_script,
                                dia,
                                mes,
                                ano,
                                diario.replace("+", " "),
                            )
                        )
                    time.sleep(0.5)
                    driver.switch_to.window(driver.window_handles[1])
                    time.sleep(1)
                    driver.switch_to_frame(
                        driver.find_element_by_name("GatewayNavegacao")
                    )
                    ult_pagina = int(driver.find_element_by_id("lblTotalPagina").text)
                    contador = 2
                    while contador <= ult_pagina:
                        try:
                            driver.switch_to.window(driver.window_handles[1])
                            driver.switch_to_frame(
                                driver.find_element_by_name("GatewayNavegacao")
                            )
                            time.sleep(1)
                            driver.find_element_by_xpath('//*[@id="txtPagina"]').clear()
                            driver.find_element_by_xpath(
                                '//*[@id="txtPagina"]'
                            ).send_keys(str(contador))
                            driver.find_element_by_xpath('//*[@id="ibtPagina"]').click()
                            time.sleep(4)
                            contador += 1
                            try:
                                time.sleep(0.1)
                                subprocess.Popen(
                                    "mv %s/GatewayPDF.pdf %s/%s.pdf"
                                    % (path, path, str(contador - 1)),
                                    shell=True,
                                )
                                time.sleep(0.1)
                                subprocess.Popen(
                                    "mv %s/*.pdf %s/Diarios_sp_DO_2/%s/%s"
                                    % (path, path_hd, nome_pasta, diario),
                                    shell=True,
                                )
                            except Exception as e:
                                pass
                        except Exception as e:
                            break
                    driver.switch_to.window(driver.window_handles[1])
                    driver.close()
                except Exception as e:
                    driver.close()

    def parse_sp_dados_1_inst(self, texto, cursor):
        def parse(texto_decisao, cursor):
            dados_re = r"\s*?{}\:.*?\n(.*?)\n"
            assunto = busca(dados_re.format("Assunto"), texto_decisao)
            classe = busca(dados_re.format("Classe"), texto_decisao)
            comarca = busca(dados_re.format("Comarca"), texto_decisao)
            data_disponibilizacao = busca(
                r"\s*?Data de Disponibilização\:.*?\n(.*?)\n", texto_decisao
            )
            foro = busca(dados_re.format("Foro"), texto_decisao)
            juiz = busca(dados_re.format("Magistrad."), texto_decisao)
            numero = busca(
                r"\d{7}\-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}",
                texto_decisao,
                ngroup=0,
                args=re.DOTALL,
            )
            requerente = busca(r"\s*?Requerent.*?\:.*?\n.*?\n(.*?)\n", texto_decisao)
            requerido = busca(r"\s*?Requerid.*?\:.*?\n.*?\n(.*?)\n", texto_decisao)
            if re.search(r"\n\s*?Justiça Gratuita", texto_decisao, re.I):
                justica_gratuita = "1"
            else:
                justica_gratuita = "0"
            cursor.execute(
                'INSERT INTO jurisprudencia_1_inst.jurisprudencia_1_inst_sp (tribunal, numero, assunto, classe, data_decisao, orgao_julgador, julgador, texto_decisao, polo_ativo, polo_passivo, comarca, justica_gratuita) values ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")'
                % (
                    "SP",
                    numero,
                    assunto,
                    classe,
                    data_disponibilizacao,
                    foro,
                    juiz,
                    texto_decisao,
                    requerente,
                    requerido,
                    comarca,
                    justica_gratuita,
                )
            )

        decisoes = re.split(r"\n\s*?\d+\s*?\-\s*?\n", texto)
        for d in range(1, len(decisoes)):
            try:
                parse(decisoes[d], cursor)
            except:
                pass

    def parse_sp_dados_2_inst(self, path_arquivos=path + "/sp_2_inst/"):
        cursor = cursorConexao()
        p = pdf_to_text()
        for arq in os.listdir(path_arquivos):
            try:
                if re.search(r"\.pdf", arq):
                    texto = (
                        p.convert_Tika(path_arquivos + arq)
                        .strip()
                        .replace("\\", "")
                        .replace("/", "")
                        .replace('"', "")
                    )
                    tribunal = "sp"
                    numero = busca(
                        r"\d{7}\-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}", texto, ngroup=0
                    )
                    polo_ativo = busca(r"apelante\s*?\:(.*?)\n", texto, args=re.I)
                    polo_passivo = busca(r"apelado\s*?\:(.*?)\n", texto, args=re.I)
                    cursor.execute(
                        'INSERT INTO jurisprudencia_2_inst.jurisprudencia_2_inst_societario_processos (tribunal, numero, texto_decisao, polo_ativo, polo_passivo) values ("%s","%s","%s","%s","%s");'
                        % (tribunal, numero, texto, polo_ativo, polo_passivo)
                    )
            except Exception as e:
                print(arq)
                print(e)


def main():
    c = crawler_jurisprudencia_tjsp()

    c.download_diario_retroativo()

    # cursor = cursorConexao()
    # c.parse_sp_dados_2_inst(cursor)

    # print('comecei ',c.__class__.__name__)
    # try:
    # 	for l in range(len(c.lista_anos)):
    # 		print(c.lista_anos[l],'\n')
    # 		for m in range(len(c.lista_meses)):
    # 			try:
    # 				c.download_1_inst('01'+c.lista_meses[m]+c.lista_anos[l],'28'+c.lista_meses[m]+c.lista_anos[l])
    # 			except Exception as e:
    # 				print(e)
    # except Exception as e:
    # 	print(e)

    # cursor = cursorConexao()
    # cursor.execute('SELECT sentenca FROM justica_estadual.jurisprudencia_sp_1_inst;')
    # dados = cursor.fetchall()
    # for dado in dados:
    # 	c.parse_sp_dados_1_inst(dado[0], cursor)

    # cursor = cursorConexao()
    # cursor.execute('SELECT id,ementas from justica_estadual.jurisprudencia_sp limit 10;')
    # cursor = cursorConexao()
    # for i in range(0,1500000,1000):
    # 	print(1500000-i)
    # 	cursor.execute('SELECT sentencas FROM justica_estadual.jurisprudencia_sp_1_inst limit %s,1000;' % str(i))
    # 	dados = cursor.fetchall()
    # 	for dado in dados:
    # 		c.parse_sp_dados_1_inst(dado[0], cursor)

    # print('comecei ',c.__class__.__name__)
    # try:
    # 	for l in range(len(c.lista_anos)):
    # 		print(c.lista_anos[l],'\n')
    # 		for m in range(len(c.lista_meses)):
    # 			try:
    # 				crawler_jurisprudencia_tj.download_tj_ESAJ(c,crawler_jurisprudencia_tj,'01'+c.lista_meses[m]+c.lista_anos[l],'28'+c.lista_meses[m]+c.lista_anos[l],termo='a')
    # 			except Exception as e:
    # 				print(e)
    # except Exception as e:
    # 	print('finalizei o ano com erro ',e)


if __name__ == "__main__":
    main()
    # c = crawler_jurisprudencia_tjsp()
    # try:
    # 	c.download_diario_oficial_adm_retrativo_antigos()
    # except Exception as e:
    # 	print(e)
    # cursor = cursorConexao()
    # p = pdf_to_text()
    # for arq in os.listdir('/home/danilo/Downloads/sp_2_inst/sp_2_inst_saude'):
    # try:
    # 	if re.search(r'\.txt',arq):
    # 		texto = ''.join([line for line in open('/home/danilo/Downloads/sp_2_inst/sp_2_inst_saude/'+arq,'r')])
    # 		tribunal = 'sp'
    # 		numero = busca(r'\d{7}\-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}',texto,ngroup=0)
    # 		polo_ativo = busca(r'apelante\s*?\:(.*?)\n',texto, args=re.I)
    # 		polo_passivo = busca(r'apelado\s*?\:(.*?)\n',texto, args=re.I)
    # 		cursor.execute('INSERT INTO jurisprudencia_2_inst.jurisprudencia_2_inst_sp_saude (tribunal, numero, texto_decisao, polo_ativo, polo_passivo) values ("%s","%s","%s","%s","%s");' % (tribunal, numero, texto.replace('"','').replace('\\',''), polo_ativo.replace('"',''), polo_passivo.replace('"','')))
    # except Exception as e:
    # 	print(arq)
    # 	print(e)
