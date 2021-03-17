import sys, re, time, os, pyautogui, subprocess
from bs4 import BeautifulSoup
from common.conexao_local import cursorConexao
from common.download_path import path, path_hd
from crawlerJus import crawlerJus
from crawler_jurisprudencia_tj import crawler_jurisprudencia_tj
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

sys.path.append(os.path.dirname(os.getcwd()))
from common_nlp.parse_texto import busca


class crawler_jurisprudencia_tjrr(crawler_jurisprudencia_tj):
    """Crawler especializado em retornar textos da jurisprudência de segunda instância de Roraima"""

    def __init__(self):
        crawler_jurisprudencia_tj.__init__(self)
        self.link_inicial = (
            "http://www.tjrr.jus.br/sistemas/php/jurisprudencia/pesqform.php"
        )
        self.pesquisa_livre = '//*[@id="pesqjuris"]/table/tbody/tr[5]/td[2]/input'
        self.botao_pesquisar = '//*[@id="pesqjuris"]/table/tbody/tr[11]/td/input'
        self.botao_proximoXP = '//*[@id="conteudo"]/table[1]/tbody/tr/td/a[%s]/b'
        self.lista_proximos = ["5", "8", "9", "10"]
        self.tabela_colunas = "justica_estadual.jurisprudencia_rr (ementas)"

    def download_tj(self, termo="a"):
        cursor = cursorConexao()
        crawler = crawlerJus()
        driver = webdriver.Chrome(self.chromedriver)
        driver.get(self.link_inicial)
        driver.find_element_by_xpath(self.pesquisa_livre).send_keys(termo)
        driver.find_element_by_xpath(self.botao_pesquisar).click()
        for i in self.lista_proximos:
            bota_p = self.botao_proximoXP % i
            links_inteiro_teor = driver.find_elements_by_partial_link_text("")
            for l in links_inteiro_teor:
                try:
                    if re.search(r"inteiroteor\.php", l.get_attribute("href")):
                        texto = (
                            crawler.baixa_texto_html(l.get_attribute("href"))
                            .replace("/", "")
                            .replace("\\", "")
                            .replace('"', "")
                        )
                        cursor.execute(
                            'INSERT INTO %s value ("%s");'
                            % (self.tabela_colunas, texto)
                        )
                except Exception as e:
                    print(e)
            driver.find_element_by_xpath(bota_p).click()
        self.botao_proximoXP = '//*[@id="conteudo"]/table[1]/tbody/tr/td/a[11]/b'
        loop_counter = 0
        while True:
            try:
                links_inteiro_teor = driver.find_elements_by_partial_link_text("")
                for l in links_inteiro_teor:
                    try:
                        if re.search(r"inteiroteor\.php", l.get_attribute("href")):
                            texto = (
                                crawler.baixa_texto_html(l.get_attribute("href"))
                                .replace("/", "")
                                .replace("\\", "")
                                .replace('"', "")
                            )
                            cursor.execute(
                                'INSERT INTO %s value ("%s");'
                                % (self.tabela_colunas, texto)
                            )
                    except:
                        pass
                driver.find_element_by_xpath(self.botao_proximoXP).click()
                time.sleep(2)
            except:
                loop_counter += 1
                time.sleep(5)
                driver.refresh()
                if loop_counter > 5:
                    break
        driver.close()

    def download_diario_retroativo(self, lista_anos=None):
        if not lista_anos:
            lista_anos = self.lista_anos
        link = "http://diario.tjrr.jus.br/dpj/dpj-%s.pdf"
        datas = []
        for l in range(len(lista_anos)):
            for i in range(1, 10):
                for j in range(1, 10):
                    datas.append(lista_anos[l] + "0" + str(i) + "0" + str(j))
                for j in range(10, 32):
                    datas.append(lista_anos[l] + "0" + str(i) + str(j))
            for i in range(10, 13):
                for j in range(1, 10):
                    datas.append(lista_anos[l] + str(i) + "0" + str(j))
                for j in range(10, 32):
                    datas.append(lista_anos[l] + str(i) + str(j))
        for data in datas:
            try:
                driver = webdriver.Chrome(self.chromedriver)
                driver.get(link % data)
                time.sleep(2.5)
                pyautogui.hotkey("ctrl", "s")
                time.sleep(1)
                pyautogui.press("enter")
                time.sleep(1)
                try:
                    subprocess.Popen("rm %s/*.html" % (path,), shell=True)
                except:
                    pass
                try:
                    subprocess.Popen(
                        'mkdir "%s/Diarios_rr/%s"' % (path_hd, data), shell=True
                    )
                    subprocess.Popen(
                        'mv %s/*.pdf "%s/Diarios_rr/%s"' % (path, path_hd, data),
                        shell=True,
                    )
                except Exception as e:
                    print(e)
                driver.close()
            except Exception as e:
                print(e)

    def parser_acordaos(self, texto, cursor):
        numero = busca(r"\nNúmero do processo\:\s*?(\d{1,45})\n", texto)
        data_disponibilizacao = busca(r"\nPublicado em\s*?\:\s*?(\d{8})", texto)
        julgador = busca(r"\n\s*?Relator.*?\:(.*?)\n", texto)
        classe = busca(r"\n\s*?Classe\:(.*?)\)", texto)
        orgao_julgador = busca(r"\nInteiro teor\:\n\s*?(.*?)\n", texto, args=re.I)
        cursor.execute(
            'INSERT INTO jurisprudencia_2_inst.jurisprudencia_2_inst (tribunal, numero, classe, data_decisao, orgao_julgador, julgador, texto_decisao) values ("%s","%s","%s","%s","%s","%s","%s");'
            % (
                "rr",
                numero,
                classe,
                data_disponibilizacao,
                orgao_julgador,
                julgador,
                texto,
            )
        )


if __name__ == "__main__":
    c = crawler_jurisprudencia_tjrr()

    # print('comecei ',c.__class__.__name__)
    # try:
    # 	c.download_tj()
    # except Exception as e:
    # 	print('finalizei com erro ',e)

    # cursor = cursorConexao()
    # cursor.execute('SELECT ementas from justica_estadual.jurisprudencia_rr;')
    # dados = cursor.fetchall()
    # for dado in dados:
    # 	c.parser_acordaos(dado[0], cursor)

    c.download_diario_retroativo()
