import sys, re, time, os, subprocess, pyautogui
from bs4 import BeautifulSoup
from common.conexao_local import cursorConexao
from common.download_path import path, path_hd
from crawler_jurisprudencia_tj import crawler_jurisprudencia_tj
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select

sys.path.append(os.path.dirname(os.getcwd()))
from common_nlp.parse_texto import busca


class crawler_jurisprudencia_cvm:
    """Crawler especializado em retornar textos da jurisprudência de segunda instância do Piauí"""

    def __init__(self):
        crawler_jurisprudencia_tj.__init__(self)
        self.link_inicial = "http://www.cvm.gov.br/decisoes/index.html?lastNameShow=&lastName=&filtro=todos&dataInicio=&dataFim=&buscadoDecisao=false&categoria=decisao"
        self.file_links = open(
            "/media/danilo/Seagate Expansion Drive/Links_cvm/lista_links.txt", "a"
        )
        self.numero_pagina_xp = '//*[@id="irPara"]'
        self.botao_proximo_xp = '//*[@id="irParaButton"]'

    def download_cvm(self, ultima_pagina_visitada=1, ultima_pagina=197):
        driver = webdriver.Chrome(self.chromedriver)
        driver.get(self.link_inicial)
        input("Aguardando loading")
        target = driver.find_element_by_xpath(self.numero_pagina_xp)
        driver.execute_script("arguments[0].scrollIntoView(true);", target)
        driver.find_element_by_xpath(self.numero_pagina_xp).clear()
        driver.find_element_by_xpath(self.numero_pagina_xp).send_keys(
            str(ultima_pagina_visitada)
        )
        target = driver.find_element_by_xpath(self.botao_proximo_xp)
        print("Terminei de andar para frente")
        time.sleep(10)
        contador_pag = ultima_pagina_visitada
        esperar = 20
        while ultima_pagina:
            try:
                time.sleep(1)
                html_source = driver.page_source
                pag_jur = BeautifulSoup(html_source, "html.parser")
                links = pag_jur.find_all("a")
                for l in links:
                    if re.search(r"/decisoes/\d+/", str(l.get("href"))):
                        self.file_links.write(str(l.get("href")) + "\n")
                target = driver.find_element_by_xpath(self.numero_pagina_xp)
                driver.execute_script("arguments[0].scrollIntoView(true);", target)
                driver.find_element_by_xpath(self.numero_pagina_xp).clear()
                driver.find_element_by_xpath(self.numero_pagina_xp).send_keys(
                    str(contador_pag)
                )
                target = driver.find_element_by_xpath(self.botao_proximo_xp)
                driver.execute_script("arguments[0].scrollIntoView(true);", target)
                driver.find_element_by_xpath(self.botao_proximo_xp).click()
                ultima_pagina -= 1
                contador_pag += 1
                time.sleep(esperar)
            except Exception as e:
                print(e)
                aux = False
                while not aux:
                    try:
                        target = driver.find_element_by_xpath(self.numero_pagina_xp)
                        driver.execute_script(
                            "arguments[0].scrollIntoView(true);", target
                        )
                        driver.find_element_by_xpath(self.numero_pagina_xp).clear()
                        driver.find_element_by_xpath(self.numero_pagina_xp).send_keys(
                            str(contador_pag)
                        )
                        target = driver.find_element_by_xpath(self.botao_proximo_xp)
                        driver.execute_script(
                            "arguments[0].scrollIntoView(true);", target
                        )
                        driver.find_element_by_xpath(self.botao_proximo_xp).click()
                        time.sleep(esperar)
                        aux = True
                    except:
                        esperar += 3
                        time.sleep(esperar)
        driver.close()

    def parser_acordaos(self, texto, cursor):
        pass


if __name__ == "__main__":
    c = crawler_jurisprudencia_cvm()
    print("comecei ", c.__class__.__name__)
    try:
        c.download_cvm()
    except Exception as e:
        print(e)
        print("finalizei com erro\n")
