from bs4 import BeautifulSoup
from crawler_jurisprudencia_tj import crawler_jurisprudencia_tj
from common.conexao_local import cursorConexao
from common.download_path import path, path_hd
from common.download_path_diarios import path as path_d
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sys, re, os, urllib.request, time, subprocess

sys.path.append(os.path.dirname(os.getcwd()))
from common_nlp.parse_texto import busca


class crawler_jurisprudencia_tjce(crawler_jurisprudencia_tj):
    """Crawler especializado em retornar textos da jurisprudência de segunda instância do Ceará"""

    def __init__(self):
        crawler_jurisprudencia_tj.__init__(self)
        self.link_inicial = "http://www.tjce.jus.br/institucional/consulta-de-acordao/"
        self.pesquisa_livre = '//*[@id="iddados.buscaInteiroTeor"]'
        self.data_julgamento_inicialXP = '//*[@id="dtJulgamentoInicio"]/input'
        self.data_julgamento_finalXP = '//*[@id="dtJulgamentoFim"]/input'
        self.botao_pesquisar = '//*[@id="pbSubmit"]'
        self.botao_proximo_ini = (
            '//*[@id="paginacaoSuperior-A"]/table/tbody/tr[1]/td[2]/div/a[5]'
        )
        self.botao_proximo = (
            '//*[@id="paginacaoSuperior-A"]/table/tbody/tr[1]/td[2]/div/a[6]'
        )
        self.tabela_colunas = "justica_estadual.jurisprudencia_ce (ementas)"

    def download_diario_retroativo(self, data_especifica=None):
        cadernos = ["1", "2"]
        link_inicial = "http://esaj.tjce.jus.br/cdje/index.do"
        datas = []
        self.lista_anos = ["2021"]
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
                "mkdir %s/Diarios_ce/%s" % (path_d, nome_pasta), shell=True
            )
            subprocess.Popen(
                "mv %s/*.pdf %s/Diarios_ce/%s" % (path, path_d, nome_pasta), shell=True
            )
            if contador > 10:
                time.sleep(3)
                driver.close()
                driver = webdriver.Chrome(self.chromedriver)
                driver.get(link_inicial)
                contador = 0

    def parser_acordaos(self, texto, cursor):
        decisoes = re.split(r"\n\d+\s*?\-", texto)
        for d in range(1, len(decisoes)):
            numero = busca(
                r"\d{7}\-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}", decisoes[d], ngroup=0
            )
            classe_assunto = busca(r"\n\s*?Classe/Assunto\s*?\:\n(.*?)\n", decisoes[d])
            try:
                classe = classe_assunto.split("/")[0]
                assunto = classe_assunto.split("/")[1]
            except:
                classe = ""
                assunto = ""
            julgador = busca(r"\n\s*?Relator.*?\:\n\s*?(.*?)\-", decisoes[d])
            orgao_julgador = busca(
                r"\n\s*?.rgão julgador\:\n\n\s*?(.*?)\n", decisoes[d]
            )
            data_disponibilizacao = busca(
                r"\n\s*?Data d[oe]? publicação\s*?\:\n\n\s*?(\d{2}/\d{2}/\d{4})",
                decisoes[d],
            )
            cursor.execute(
                'INSERT INTO jurisprudencia_2_inst.jurisprudencia_2_inst (tribunal, numero, classe, assunto, data_decisao, orgao_julgador, julgador, texto_decisao) values ("%s","%s","%s","%s","%s","%s","%s","%s");'
                % (
                    "ce",
                    numero,
                    classe,
                    assunto,
                    data_disponibilizacao,
                    orgao_julgador,
                    julgador,
                    decisoes[d],
                )
            )


if __name__ == "__main__":
    c = crawler_jurisprudencia_tjce()
    # print('comecei ',c.__class__.__name__)
    # try:
    # 	for l in range(len(c.lista_anos)):
    # 		print(c.lista_anos[l],'\n')
    # 		try:
    # 			crawler_jurisprudencia_tj.download_tj_ESAJ_recaptcha(c,crawler_jurisprudencia_tj,'0101'+c.lista_anos[l],'3112'+c.lista_anos[l],termo='processo')
    # 		except Exception as e:
    # 			print(e)
    # except Exception as e:
    # 	print('finalizei o ano com erro ', e)

    # cursor = cursorConexao()
    # cursor.execute('SELECT ementas from justica_estadual.jurisprudencia_ce;')
    # dados = cursor.fetchall()
    # for ementa in dados:
    # 	c.parser_acordaos(ementa[0], cursor)

    c.download_diario_retroativo()
