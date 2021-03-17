import time, re, sys, os, urllib.request
from bs4 import BeautifulSoup
from common.conexao_local import cursorConexao
from common.download_path import path, path_hd
from crawler_jurisprudencia_tj import crawler_jurisprudencia_tj
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

sys.path.append(os.path.dirname(os.getcwd()))
from common_nlp.parse_texto import busca


class crawler_jurisprudencia_tjma(crawler_jurisprudencia_tj):
    """Crawler especializado em retornar textos da jurisprudência de segunda instância de Maranhão"""

    def __init__(self):
        crawler_jurisprudencia_tj.__init__(self)
        self.link_inicial = "http://jurisconsult.tjma.jus.br/"
        self.pesquisa_livre = '//*[@id="txtChaveJurisprudencia"]'
        self.data_julgamento_inicial = "dtaInicio"
        self.data_julgamento_final = "dtaTermino"
        self.botao_pesquisar = "btnConsultar"

    def download_tj(self, data_julg_ini, data_julg_fim, termo="acordam"):
        cursor = cursorConexao()
        driver = webdriver.Chrome(self.chromedriver)
        driver.get(self.link_inicial)
        driver.find_element_by_xpath(self.pesquisa_livre).send_keys(termo)
        driver.find_element_by_name(self.data_julgamento_inicial).send_keys(
            data_julg_ini
        )
        driver.find_element_by_name(self.data_julgamento_final).send_keys(data_julg_fim)
        driver.find_elements_by_name(self.botao_pesquisar)[2].click()
        texto = crawler_jurisprudencia_tj.extrai_texto_html(self, driver.page_source)
        tamanho = 5
        while True:
            try:
                time.sleep(3)
                links_proximos = driver.find_elements_by_class_name("linkQuery")
                texto = crawler_jurisprudencia_tj.extrai_texto_html(
                    self, driver.page_source
                )
                cursor.execute(
                    'INSERT INTO justica_estadual.jurisprudencia_ma (ementas) value("%s")'
                    % texto.replace('"', "")
                )
                try:
                    int(links_proximos[-1].text)
                    driver.close()
                    break
                except:
                    driver.find_element_by_id("pagination").click()
            except Exception as e:
                driver.close()
                print(e)
                break

    def download_diario_retroativo_old(self, data_especifica=None):
        # view-source:http://www.tjma.jus.br/inicio/diario/pagina/21/dtaInicio/2011-01-01/dtaTermino/2019-11-13
        data_ini_xpath = '//*[@id="dtaInicio"]'
        data_fim_xpath = '//*[@id="dtaTermino"]'
        download_xpath = '//*[@id="table1"]/tbody/tr[2]/td[3]/a[1]'
        link_inicial = "http://www.tjma.jus.br/inicio/diario"
        pesquisar_xpath = '//*[@id="btnConsultar"]'
        driver = webdriver.Chrome(self.chromedriver)
        driver.get(link_inicial)
        time.sleep(4)
        datas = []
        if data_especifica:
            data_ini_element = driver.find_element_by_xpath(data_ini_xpath)
            driver.execute_script(
                "arguments[0].style.visibility = 'visible';", data_ini_element
            )
            driver.execute_script(
                "arguments[0].removeAttribute('readonly')", data_ini_element
            )
            data_ini_element.click()
            data_ini_element.clear()
            data_ini_element.send_keys(data_especifica)
            data_fim_element = driver.find_element_by_xpath(data_fim_xpath)
            driver.execute_script(
                "arguments[0].style.visibility = 'visible';", data_fim_element
            )
            driver.execute_script(
                "arguments[0].removeAttribute('readonly')", data_fim_element
            )
            data_fim_element.click()
            data_fim_element.clear()
            data_fim_element.send_keys(data_especifica)
            data_fim_element.click()
            try:
                driver.find_element_by_xpath(download_xpath).click()
                time.sleep(3)
                driver.switch_to.window(driver.window_handles[-1])
                url = driver.current_url
                driver.close()
                response = urllib.request.urlopen(url, timeout=15)
                file = open(data_especifica + "_MA.pdf", "wb")
                time.sleep(1)
                file.write(response.read())
                file.close()
                # subprocess.Popen('mkdir %s/Diarios_ma/%s' % (path_hd,nome_pasta), shell=True)
                # subprocess.Popen('mv %s/*.pdf %s/Diarios_ma/%s' % (path,path_hd,nome_pasta), shell=True)
            except Exception as e:
                print(e)
            return
        for l in range(len(self.lista_anos)):
            for i in range(1, 10):
                for j in range(1, 10):
                    datas.append("0" + str(j) + "0" + str(i) + self.lista_anos[l])
                for j in range(10, 32):
                    datas.append(str(j) + "0" + str(i) + self.lista_anos[l])
            for i in range(10, 13):
                for j in range(1, 10):
                    datas.append("0" + str(j) + str(i) + self.lista_anos[l])
                for j in range(10, 32):
                    datas.append(str(j) + str(i) + self.lista_anos[l])
        for data in datas:
            # PROBLEMA COM VISIBILIDADE DE ELEMENTO
            driver.find_element_by_id(data_ini_xpath).send_keys(data)
            driver.find_element_by_id(data_fim_xpath).send_keys(data)
            driver.find_element_by_xpath(pesquisar_xpath).click()
            try:
                driver.find_element_by_xpath(download_xpath).click()
                time.sleep(3)
                subprocess.Popen(
                    "mkdir %s/Diarios_ma/%s" % (path_hd, nome_pasta), shell=True
                )
                subprocess.Popen(
                    "mv %s/*.pdf %s/Diarios_ma/%s" % (path, path_hd, nome_pasta),
                    shell=True,
                )
            except Exception as e:
                print(e)

    def download_diario_retroativo(self, path_diarios, primeiro=1167, ultimo=3133):
        for i in range(primeiro, ultimo):
            link = (
                "https://www3.tjma.jus.br/diario/VisualizacaoDiarioA3.mtw?idDiario=%s"
            )
            response = urllib.request.urlopen(link % (str(i),), timeout=40)
            try:
                file = open(path_diarios + "diario_ma_" + str(i) + ".pdf", "wb")
                file.write(response.read())
                time.sleep(3)
                file.close()
            except:
                print(i)

    def parser_acordaos(self, texto, cursor):
        numero = busca(r"\n(.*?)\(clique aqui para visualizar o processo\)", texto)
        data_disponibilizacao = busca(
            r"Data do registro do acordão\:\n(\d{2}/\d{2}/\d{4})", texto
        )
        julgador = busca(r"\nRelator.*?\:\n(.*?)\n", texto)
        orgao_julgador = busca(r"\n.rgão\:\n(.*?)\n", texto)
        if numero != "":
            cursor.execute(
                'INSERT INTO jurisprudencia_2_inst.jurisprudencia_2_inst (tribunal, numero, data_decisao, orgao_julgador, julgador, texto_decisao) values ("%s","%s","%s","%s","%s","%s");'
                % (
                    "ma",
                    numero,
                    data_disponibilizacao,
                    orgao_julgador,
                    julgador,
                    texto.replace('"', "").replace("/", "").replace("\\", ""),
                )
            )


if __name__ == "__main__":
    c = crawler_jurisprudencia_tjma()

    # cursor = cursorConexao()
    # cursor.execute('SELECT id, ementas from justica_estadual.jurisprudencia_ma;')
    # dados = cursor.fetchall()
    # for id_d, dado in dados:
    # 	try:
    # 		c.parser_acordaos(dado, cursor)
    # 	except Exception as e:
    # 		print(id_d, e)

    # try:
    # 	for a in c.lista_anos:
    # 		for m in range(len(c.lista_meses)):
    # 			c.download_tj('01'+c.lista_meses[m]+a,'28'+c.lista_meses[m]+a)
    # except Exception as e:
    # 	print(e)

    c.download_diario_retroativo(
        "/media/danilo/Seagate Expansion Drive/Diarios/Diarios_ma/"
    )
