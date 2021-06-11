import time, re, urllib.request, sys, os, subprocess
from bs4 import BeautifulSoup
from common.conexao_local import cursorConexao
from common.download_path import path, path_hd
from common.download_path_diarios import path as path_d
from crawler_jurisprudencia_tj import crawler_jurisprudencia_tj
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

sys.path.append(os.path.dirname(os.getcwd()))
from common_nlp.parse_texto import busca


class crawler_jurisprudencia_trf4(crawler_jurisprudencia_tj):
    """Crawler especializado em retornar textos da jurisprudência do tribunal regional federal da quarta região"""

    def __init__(self):
        crawler_jurisprudencia_tj.__init__(self)
        self.link_inicial = "https://jurisprudencia.trf4.jus.br/pesquisa/pesquisa.php"
        self.botao_pesquisar = '//*[@id="frmPesquisar"]/table/tbody/tr[13]/td[2]/table/tbody/tr/td/input[1]'
        self.botao_prox = '//*[@id="sbmProximaPagina"]'
        self.data_inicial_xpath = '//*[@id="dataIni"]'
        self.data_final_xpath = '//*[@id="dataFim"]'
        self.link_resultado_xpath = '//*[@id="parcial"]'
        self.pesquisa_livre = '//*[@id="textoPesqLivre"]'
        self.tabela_colunas = "justica_federal.jurisprudencia_trf4 (ementas)"

    def download_diario_retroativo(self):
        link_inicial = (
            "https://www.trf4.jus.br/trf4/diario/download.php?id_publicacao={}"
        )
        n_ini = 0
        n_fim = 8154
        for i in range(n_ini, n_fim):
            try:
                response = urllib.request.urlopen(
                    link_inicial.format(i),
                    timeout=20,
                )
                file = open("{}/Diarios_trf4/{}.pdf".format(path_d, i), "wb")
                file.write(response.read())
                file.close()
            except Exception as e:
                print(e)

    def download_trf4(self, data_ini, data_fim, termo="recurso"):
        cursor = cursorConexao()
        driver = webdriver.Chrome(self.chromedriver)
        driver.get(self.link_inicial)
        time.sleep(1)
        driver.find_element_by_xpath(self.pesquisa_livre).send_keys(termo)
        driver.find_element_by_xpath(self.data_inicial_xpath).send_keys(data_ini)
        driver.find_element_by_xpath(self.data_final_xpath).send_keys(data_fim)
        driver.find_element_by_xpath(self.botao_pesquisar).click()
        time.sleep(1)
        try:
            driver.find_element_by_xpath(self.link_resultado_xpath).click()
            time.sleep(1)
        except:
            pass
        time.sleep(1)
        texto = crawler_jurisprudencia_tj.extrai_texto_html(
            self, (driver.page_source)
        ).replace('"', "")
        cursor.execute('INSERT INTO %s value ("%s");' % (self.tabela_colunas, texto))
        try:
            driver.find_element_by_xpath(self.botao_prox).click()
        except:
            driver.close()
            return
        contador = 0
        while True:
            try:
                time.sleep(1)
                texto = crawler_jurisprudencia_tj.extrai_texto_html(
                    self, (driver.page_source)
                ).replace('"', "")
                cursor.execute(
                    'INSERT INTO %s value ("%s");' % (self.tabela_colunas, texto)
                )
                driver.find_element_by_xpath(self.botao_prox).click()
                contador = 0
            except Exception as e:
                print(e)
                contador += 1
                time.sleep(5)
                if contador > 3:
                    driver.close()
                    break
        driver.close()

    def parser_acordaos(self, texto, cursor):
        inicio = False
        linhas = [l + "\n" for l in texto.split("\n")]
        re_inicio = r"^\s*?\d+$"
        texto_decisao = ""

        def parse(texto_decisao):
            classe = busca(r"\n\s*?Classe\:\s*?(.*?)\n", texto_decisao)
            numero = busca(r"\n\s*?Processo\:\s*?([\d\.\-]{1,25})", texto_decisao)
            tribunal_origem = busca(r"UF\:\s*?(\w{2})", texto_decisao)
            data_decisao = busca(
                r"\n\s*?Data da Decisão\: (\d{2}/\d{2}/\d{4}|\d{7}\-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4})",
                texto_decisao,
            )
            orgao_julgador = busca(r".rgão Julgador\:\s*?(.*?\n)", texto_decisao)
            relator = busca(r"\n\s*?Relator.*?\n(.*?)\n", texto_decisao)
            decisao = busca(r"\n\s*?Decisão\s*?(.+)", texto_decisao, args=re.DOTALL)
            cursor.execute(
                'INSERT INTO jurisprudencia_2_inst.jurisprudencia_2_inst (tribunal, numero, classe, data_decisao, orgao_julgador, julgador, texto_decisao, origem) values ("%s","%s","%s","%s","%s","%s","%s","%s");'
                % (
                    "trf4",
                    numero,
                    classe,
                    data_decisao,
                    orgao_julgador,
                    relator,
                    decisao,
                    tribunal_origem,
                )
            )

        for linha in linhas:
            if inicio:
                if re.search(re_inicio, linha):
                    parse(texto_decisao)
                    texto_decisao = ""
                else:
                    texto_decisao += linha
            else:
                if re.search(re_inicio, linha):
                    inicio = True
        parse(texto_decisao)


if __name__ == "__main__":
    c = crawler_jurisprudencia_trf4()

    # cursor = cursorConexao()
    # cursor.execute('SELECT ementas FROM justica_federal.jurisprudencia_trf4;')
    # dados = cursor.fetchall()
    # for ementa in dados:
    # 	c.parser_acordaos(ementa[0],cursor)
    # try:
    # 	for l in range(len(c.lista_anos)):
    # 		print(c.lista_anos[l],'\n')
    # 		for m in range(len(c.lista_meses)):
    # 			for i in range(1,9):
    # 				try:
    # 					c.download_trf4('0'+str(i)+c.lista_meses[m]+c.lista_anos[l],'0'+str(i+1)+c.lista_meses[m]+c.lista_anos[l])
    # 				except Exception as e:
    # 					print(e)
    # 			for i in range(10,27):
    # 				try:
    # 					c.download_trf4(str(i)+c.lista_meses[m]+c.lista_anos[l],str(i+1)+c.lista_meses[m]+c.lista_anos[l])
    # 				except Exception as e:
    # 					print(e)
    # except Exception as e:
    # 	print(e)

    c.download_diario_retroativo()
