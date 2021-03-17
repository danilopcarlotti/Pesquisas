import sys, re, os, urllib.request, time, subprocess
from common.download_path import path, path_hd
from common.download_path_diarios import path as path_diarios
from common.conexao_local import cursorConexao
from crawler_jurisprudencia_tj import crawler_jurisprudencia_tj
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

sys.path.append(os.path.dirname(os.getcwd()))
from common_nlp.parse_texto import busca


class crawler_jurisprudencia_tjal(crawler_jurisprudencia_tj):
    """Crawler especializado em retornar textos da jurisprudência de segunda instância de Alagoas"""

    def __init__(self):
        crawler_jurisprudencia_tj.__init__(self)
        self.link_inicial = "https://www2.tjal.jus.br/cjsg/consultaCompleta.do"
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
        self.tabela_colunas = "justica_estadual.jurisprudencia_al (ementas)"

    def download_1_inst(self):
        botao_proximo_ini = 2
        botao_proximo = '//*[@id="pn_%s"]'
        botao_xpath = '//*[@id="corpo_texto"]/div/div/div/form/button'
        driver = webdriver.Chrome(self.chromedriver)
        link = "http://www.tjal.jus.br/corregedoria/?pag=sentencas"
        re_href = r"http\://www.intranet.tjal.jus.br/bancodesentencas/arquivos/"
        texto_xpath = '//*[@id="corpo_texto"]/div/div/div/form/input'
        driver.get(link)
        driver.find_element_by_xpath(texto_xpath).send_keys("a ou não a")
        driver.find_element_by_xpath(botao_xpath).click()
        time.sleep(1)
        contador = 0
        loop_counter = 0
        while True:
            try:
                soup = BeautifulSoup(driver.page_source, "html.parser")
                for l in soup.find_all("a", href=True):
                    if re.search(re_href, l["href"]):
                        urllib.request.urlretrieve(
                            l["href"], "TJAL_1_inst_%s.pdf" % str(contador)
                        )
                        subprocess.Popen(
                            "mv TJAL_1_inst_*.pdf %s/al_1_inst" % (path,), shell=True
                        )
                        contador += 1
                try:
                    driver.find_element_by_xpath(
                        botao_proximo % str(botao_proximo_ini)
                    ).click()
                except:
                    botao_proximo_ini += 1
                    driver.find_element_by_xpath(
                        botao_proximo % str(botao_proximo_ini)
                    ).click()
                loop_counter = 0
            except Exception as e:
                if loop_counter > 2:
                    break
                loop_counter += 1
                print(e)

    def download_diario_retroativo(self, data_especifica=None):
        cadernos = ["2", "3"]
        link_inicial = "http://www2.tjal.jus.br/cdje/index.do"
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
                for i in range(11, 13):
                    for j in range(1, 10):
                        datas.append(
                            "0" + str(j) + "/" + str(i) + "/" + self.lista_anos[l]
                        )
                    for j in range(10, 32):
                        datas.append(str(j) + "/" + str(i) + "/" + self.lista_anos[l])
        contador = 0
        driver = webdriver.Chrome(self.chromedriver)
        driver.get(link_inicial)
        for data in datas:
            contador += 1
            print(data)
            for caderno in cadernos:
                driver.execute_script(
                    "popup('/cdje/downloadCaderno.do?dtDiario=%s'+'&cdCaderno=%s&tpDownload=D','cadernoDownload');"
                    % (data, caderno)
                )
                time.sleep(1)
            time.sleep(3)
            nome_pasta = data.replace("/", "")
            subprocess.Popen(
                "mkdir %s/Diarios_al/%s" % (path_diarios, nome_pasta), shell=True
            )
            subprocess.Popen(
                "mv %s/*.pdf %s/Diarios_al/%s" % (path, path_diarios, nome_pasta),
                shell=True,
            )
            if contador > 10:
                time.sleep(3)
                driver.close()
                driver = webdriver.Chrome(self.chromedriver)
                driver.get(link_inicial)
                contador = 0

    def parser_acordaos(self, texto, cursor):
        decisoes = re.split(r"\n\s*?\d*?\s*?\-\s*?\n", texto)
        for d in range(1, len(decisoes)):
            numero = busca(
                r"\d{7}\-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}", decisoes[d], ngroup=0
            )
            classe_assunto = busca(r"\n\s*?Classe/Assunto\:\n(.+)", decisoes[d])
            classe = classe_assunto.split("/")[0]
            assunto = classe_assunto.split("/")[-1]
            julgador = busca(r"Relator \(a\)\:(.*?)\;", decisoes[d])
            orgao_julgador = busca(r"Órgão julgador\:(.*?)\;", decisoes[d])
            data_disponibilizacao = busca(
                r"Data do julgamento\:\s*?(.*?)\;", decisoes[d]
            )
            cursor.execute(
                'INSERT INTO jurisprudencia_2_inst.jurisprudencia_2_inst (tribunal, numero, assunto, classe, data_decisao, orgao_julgador, julgador, texto_decisao) 	values ("%s","%s","%s","%s","%s","%s","%s","%s");'
                % (
                    "al",
                    numero,
                    assunto,
                    classe,
                    data_disponibilizacao,
                    orgao_julgador,
                    julgador,
                    decisoes[d],
                )
            )


def main():
    c = crawler_jurisprudencia_tjal()
    # c.download_1_inst()

    # print('comecei ',c.__class__.__name__)
    # for l in c.lista_anos:
    # 	try:
    # 		print(l,'\n')
    # 		crawler_jurisprudencia_tj.download_tj_ESAJ_recaptcha(c,crawler_jurisprudencia_tj,'01/01/'+l,'31/12/'+l)
    # 	except Exception as e:
    # 		print('finalizei o ano ',l)
    # 		print(e)
    # cursor = cursorConexao()
    # cursor.execute('SELECT id, ementas from justica_estadual.jurisprudencia_al limit 1000000')
    # dados = cursor.fetchall()
    # for id_p, dado in dados:
    # 	try:
    # 		c.parser_acordaos(dado, cursor)
    # 	except:
    # 		print(id_p)

    c.download_diario_retroativo()


if __name__ == "__main__":
    main()
