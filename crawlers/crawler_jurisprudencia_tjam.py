import sys, re, os, subprocess, time, pyautogui
from crawler_jurisprudencia_tj import crawler_jurisprudencia_tj
from common.download_path import path, path_hd
from common.conexao_local import cursorConexao
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

sys.path.append(os.path.dirname(os.getcwd()))
from common_nlp.parse_texto import busca


class crawler_jurisprudencia_tjam(crawler_jurisprudencia_tj):
    """Crawler especializado em retornar textos da jurisprudência de segunda instância do Amazonas"""

    def __init__(self):
        crawler_jurisprudencia_tj.__init__(self)
        self.link_inicial = "http://consultasaj.tjam.jus.br/cjsg/consultaCompleta.do"
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
        self.tabela_colunas = "justica_estadual.jurisprudencia_am (ementas)"
        self.link_esaj = (
            "http://consultasaj.tjam.jus.br/cjsg/getArquivo.do?cdAcordao=%s&cdForo=%s"
        )

    def download_acordao_am(self, dados_baixar):
        self.download_pdf_acordao_captcha_image(
            dados_baixar, '//*[@id="valorCaptcha"]', '//*[@id="pbEnviar"]', "am_2_inst"
        )

    def download_diario_retroativo(self, data_especifica=None):
        cadernos = ["2", "3", "4"]
        datas = []
        if data_especifica:
            datas.append(data_especifica)
        else:
            for l in range(len(self.lista_anos)):
                for i in range(5, 10):
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
        contador = 0
        driver = webdriver.Chrome(self.chromedriver)
        driver.get("http://consultasaj.tjam.jus.br/cdje/index.do")
        for data in datas:
            contador += 1
            print(data)
            for caderno in cadernos:
                driver.execute_script(
                    "popup('/cdje/downloadCaderno.do?dtDiario=%s'+'&cdCaderno=%s&tpDownload=D','cadernoDownload');"
                    % (data, caderno)
                )
                time.sleep(1)
            time.sleep(5)
            nome_pasta = data.replace("/", "")
            subprocess.Popen(
                "mkdir %s/Diarios_am/%s" % (path_hd, nome_pasta), shell=True
            )
            subprocess.Popen(
                "mv %s/*.pdf %s/Diarios_am/%s" % (path, path_hd, nome_pasta), shell=True
            )
            if contador > 10:
                time.sleep(5)
                driver.close()
                driver = webdriver.Chrome(self.chromedriver)
                driver.get("http://consultasaj.tjam.jus.br/cdje/index.do")
                contador = 0

    def parser_acordaos(self, arquivo, cursor, pdf_class):
        texto = (
            pdf_class.convert_pdfminer(arquivo)
            .replace('"', "")
            .replace("/", "")
            .replace("\\", "")
        )
        numero = re.search(r"\nPROCESSO N.. (.{1,44})", texto)
        if numero:
            numero = numero.group(1)
            julgador = busca(r"\s*?Des\. (.*?)\n", texto)
            cursor.execute(
                'INSERT INTO jurisprudencia_2_inst.jurisprudencia_2_inst (tribunal, numero, julgador, texto_decisao) values ("%s","%s","%s","%s");'
                % ("am", numero, julgador, texto)
            )
        else:
            numero = busca(r"\nAutos n. (.{1,44})\.?", texto)
            classe = busca(r"\nClasse\: (.*?)\.", texto)
            julgador = busca(r"\nRelator\:(.*?)\n", texto)
            orgao_julgador = busca(r".rg.o Julgador\:(.*?)\n", texto)
            cursor.execute(
                'INSERT INTO jurisprudencia_2_inst.jurisprudencia_2_inst (tribunal, numero, classe, orgao_julgador, julgador, texto_decisao) values ("%s","%s","%s","%s","%s","%s");'
                % ("am", numero, classe, orgao_julgador, julgador, texto)
            )


def main():
    c = crawler_jurisprudencia_tjam()
    c.download_diario_retroativo()
    # cursor = cursorConexao()
    # cursor.execute('SELECT id,ementas from justica_estadual.jurisprudencia_am where id > 29237 limit 10000000;')
    # lista_links = cursor.fetchall()
    # c.download_acordao_am(lista_links)

    # p = pdf_to_text()
    # for arq in os.listdir(path+'/am_2_inst'):
    # 	c.parser_acordaos(path+'/am_2_inst/'+arq, cursor, p)

    # print('comecei ',c.__class__.__name__)
    # try:
    # 	for l in range(3,len(c.lista_anos)):
    # 		print(c.lista_anos[l],'\n')
    # 		for m in range(len(c.lista_meses)):
    # 			try:
    # 				crawler_jurisprudencia_tj.download_tj_ESAJ(c,crawler_jurisprudencia_tj,'01'+c.lista_meses[m]+c.lista_anos[l],'28'+c.lista_meses[m]+c.lista_anos[l])
    # 			except Exception as e:
    # 				print(e)
    # except Exception as e:
    # 	print('finalizei o ano com erro ',e)


if __name__ == "__main__":
    main()
