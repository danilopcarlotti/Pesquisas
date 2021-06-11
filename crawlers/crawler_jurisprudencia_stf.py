import re, os, sys, time, datetime, urllib.request, ssl, logging, pyautogui, json, pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from crawlerJus import crawlerJus
from common.conexao_local import cursorConexao
from common.download_path_diarios import path as path_d
from common.login_stf import USER, SENHA


class crawler_jurisprudencia_stf(crawlerJus):
    """Classe para download de informações sobre processos do STF"""

    def __init__(self):
        super().__init__()
        ssl._create_default_https_context = ssl._create_unverified_context
        self.link_base = (
            "http://www.stf.jus.br/portal/processo/verProcessoAndamento.asp?incidente="
        )
        self.numero_final = 7000000  # jan 2020
        self.numero_inicial = 5428907  # jun 2018
        self.cursor = None

    def baixarDadosProcesso(self, link_processos):
        id_processo_stf = ""
        for _, link in link_processos:
            try:
                relator = ""
                pag = self.baixa_pag(link)
                soup = BeautifulSoup(pag, "html.parser")
                div_andamento = [
                    x
                    for x in soup.find("div", {"id": "detalheProcesso"})
                    .get_text()
                    .split("\n")
                    if x != ""
                ]
                for i in range(len(div_andamento) - 1):
                    if div_andamento[i] == "Relator atual":
                        relator = div_andamento[i + 1]
                link = link.replace("Andamento", "Detalhe")
                pag = self.baixa_pag(link)
                soup = BeautifulSoup(pag, "html.parser")
                div_detalhe = [
                    x
                    for x in soup.find("div", {"id": "conteudoAbasAcompanhamento"})
                    .get_text()
                    .split("\n")
                    if x != ""
                ]
                id_processo_stf = soup.find("h3").text.split("-")[0].strip()
                assunto = ""
                autuacao = ""
                numero_origem = ""
                polo_ativo = ""
                polo_passivo = ""
                ramo_direito = ""
                tribunal_origem = ""
                for i in range(len(div_detalhe) - 1):
                    if div_detalhe[i] == "Orgão de Origem:":
                        tribunal_origem = (
                            div_detalhe[i + 1]
                            .replace(")", "")
                            .replace("(", "")
                            .replace("\\", "")
                            .replace('"', "")
                            .replace("/", "")
                        )
                    elif div_detalhe[i] == "Números de Origem:":
                        numero_origem = (
                            div_detalhe[i + 1]
                            .replace(")", "")
                            .replace("(", "")
                            .replace("\\", "")
                            .replace('"', "")
                            .replace("/", "")
                        )
                    elif div_detalhe[i] == "Ramo do Direito":
                        if div_detalhe[i + 1] != "Assunto":
                            ramo_direito = (
                                div_detalhe[i + 1]
                                .replace(")", "")
                                .replace("(", "")
                                .replace("\\", "")
                                .replace('"', "")
                                .replace("/", "")
                            )
                    elif div_detalhe[i] == "Assunto":
                        assunto = (
                            div_detalhe[i + 1]
                            .replace(")", "")
                            .replace("(", "")
                            .replace("\\", "")
                            .replace('"', "")
                            .replace("/", "")
                        )
                    elif div_detalhe[i] == "Data de Protocolo":
                        autuacao = (
                            div_detalhe[i + 1]
                            .replace(")", "")
                            .replace("(", "")
                            .replace("\\", "")
                            .replace('"', "")
                            .replace("/", "")
                        )
                    elif re.search(r"TE\.\(S\)", div_detalhe[i]):
                        polo_ativo = (
                            div_detalhe[i + 1]
                            .replace(")", "")
                            .replace("(", "")
                            .replace("\\", "")
                            .replace('"', "")
                            .replace("/", "")
                        )
                    elif re.search(r"DO\.\(A/S\)", div_detalhe[i]):
                        polo_passivo = (
                            div_detalhe[i + 1]
                            .replace(")", "")
                            .replace("(", "")
                            .replace("\\", "")
                            .replace('"', "")
                            .replace("/", "")
                        )
                self.cursor.execute(
                    'INSERT INTO stf.dados_processo (processo, polo_ativo, polo_passivo, autuacao, numero_origem, relator, ramo_direito, assunto, tribunal_origem, link_dados) values ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")'
                    % (
                        id_processo_stf,
                        polo_ativo,
                        polo_passivo,
                        autuacao,
                        numero_origem,
                        relator,
                        ramo_direito,
                        assunto,
                        tribunal_origem,
                        link,
                    )
                )
            except Exception as e:
                print(e)

    def baixarVotos(self, link, link_jurisprudencia):
        pagina_jurisprudencia = self.baixa_pag(link_jurisprudencia)
        if pagina_jurisprudencia != "":
            # print('Pagina jurisprudencia')
            pagina = BeautifulSoup(pagina_jurisprudencia, "lxml")
            link_texto_jurisprudencia = pagina.find(
                "a", href=re.compile(r"listarJurisprudencia\.asp\?.+")
            )
            if link_texto_jurisprudencia:
                # print('Link texto jurisprudencia')
                link_texto = (
                    "http://www.stf.jus.br/portal/jurisprudencia/"
                    + link_texto_jurisprudencia["href"]
                )
                pagina_texto = self.baixa_pag(link_texto)
                pagina = BeautifulSoup(pagina_texto, "lxml")
                div_texto = pagina.find("div", {"id": "divImpressao"})
                if div_texto:
                    # print('Div texto')
                    texto_final = div_texto.get_text().replace('"', "")
                    if texto_final:
                        self.cursor.execute(
                            'INSERT INTO stf.decisoes (link_pagina, texto_decisao) values("%s","%s");'
                            % (link, texto_final)
                        )

    def baixarVotosDriver(self, link):
        print(link)
        driver = webdriver.Chrome(self.chromedriver)
        try:
            driver.get(link)
            driver.find_element_by_xpath('//*[@id="btn-jurisprudencia"]').click()
            time.sleep(5)
            driver.switch_to_window(driver.window_handles[-1])
            self.baixarVotos(link, driver.current_url)
        except Exception as e:
            print(e)
            time.sleep(10)
        driver.quit()

    def baixa_decisoes_proc(self):
        for i in range(self.numero_inicial, self.numero_final):
            # self.baixarVotos(self.link_base+str(i))
            self.baixarVotosDriver(self.link_base + str(i))

    def baixar_documentos_stf(self):
        print("**FAZENDO DOWNLOAD DOS DOCUMENTOS DE PROCESSOS DO STF**")
        driver = self.login_stf()
        link_mensagem_link = '//*[@id="example"]/tbody/tr/td[2]/span/a'
        link_download = '//*[@id="idModalVisualizacaoConteudoComunicacao"]/div/div/div[2]/div/div/h4/div/p[2]/a'
        time.sleep(5)
        while True:
            try:
                driver.find_element_by_xpath(link_mensagem_link).click()
                time.sleep(1)
                driver.find_element_by_xpath(link_download).click()
                time.sleep(2)
                try:
                    driver.switch_to.window(driver.window_handles[-1])
                    pyautogui.hotkey("ctrl", "w")
                except:
                    pass
                time.sleep(1)
                driver.switch_to.window(driver.window_handles[0])
                driver.find_element_by_xpath("/html/body/a").click()
                time.sleep(1)
            except:
                driver.refresh()
                time.sleep(5)

    def login_stf(self):
        driver = webdriver.Chrome(self.chromedriver)
        link = "https://sistemas.stf.jus.br/peticionamento/"
        driver.get(link)
        try:
            senha_xpath = '//*[@id="password"]'
            submit_login_xpath = '//*[@id="fm1"]/div[3]/div[2]/input'
            username_xpath = '//*[@id="username"]'
            driver.find_element_by_xpath(username_xpath).send_keys(USER)
            driver.find_element_by_xpath(senha_xpath).send_keys(SENHA)
            driver.find_element_by_xpath(submit_login_xpath).click()
        except:
            pass
        return driver

    def parse_json_decisions(self, path_json, path_csv):
        json_file = open(path_json, "r")
        rows = []
        for line in json_file:
            data = json.loads(line)
            dic = data.copy()
            data_julgamento = re.search(r"\d{2}\.\d{2}\.\d{4}", data["voto"][-500:])
            dic["data"] = data_julgamento.group(0) if data_julgamento else ""
            rows.append(dic)
        df = pd.DataFrame(rows, index=[i for i in range(len(rows))])
        df.to_csv(path_csv, index=False)

    def solicitar_link_download_documentos(self, ids_doc):
        aba_pecas_xpath = '//*[@id="abaPecas"]'
        download_todas_pecas_xpath = (
            '//*[@id="pecas"]/processo-pecas/div/div/div/div/div/button[3]'
        )
        processo_interesse_xpath = '//*[@id="txt-pesquisa-processo"]'
        submit_processo_interesse_xpath = '//*[@id="container"]/div[3]/div[1]/div[2]/div[2]/div/div/div[4]/div/div[1]/div/span/button'
        ver_mais_processo_interesse_xpath = '//*[@id="container"]/div[3]/div[1]/div[2]/div[2]/div/div/div[4]/div/div[2]/div/div/a'
        for i in ids_doc:
            driver = self.login_stf()
            while True:
                try:
                    driver.switch_to.window(driver.window_handles[0])
                    driver.find_element_by_xpath(processo_interesse_xpath).clear()
                    driver.find_element_by_xpath(processo_interesse_xpath).send_keys(i)
                    time.sleep(2)
                    driver.find_element_by_xpath(
                        submit_processo_interesse_xpath
                    ).click()
                    time.sleep(5)
                    driver.find_element_by_xpath(
                        ver_mais_processo_interesse_xpath
                    ).click()
                    time.sleep(2)
                    driver.switch_to.window(driver.window_handles[1])
                    time.sleep(1)
                    driver.find_element_by_xpath(aba_pecas_xpath).click()
                    try:
                        driver.find_element_by_xpath(download_todas_pecas_xpath).click()
                        break
                    except:
                        break
                except:
                    time.sleep(1)
            driver.close()

    def download_diario_retroativo(self):
        link_inicial = "https://www.stf.jus.br/arquivo/djEletronico/DJE_{}_{}.pdf"
        self.lista_anos = [str(i) for i in range(2021, 2022)]
        for l in range(len(self.lista_anos)):
            datas = []
            for i in range(7, 10):
                for j in range(1, 10):
                    datas.append(self.lista_anos[l] + "0" + str(i) + "0" + str(j))
                for j in range(10, 32):
                    datas.append(self.lista_anos[l] + "0" + str(i) + str(j))
            for i in range(11, 13):
                for j in range(1, 10):
                    datas.append(self.lista_anos[l] + str(i) + "0" + str(j))
                for j in range(10, 32):
                    datas.append(self.lista_anos[l] + str(i) + str(j))
            counter = 1
            for data in datas:
                try:
                    link = link_inicial.format(data, "{:03d}".format(counter))
                    print(link)
                    self.baixa_html_pdf(link, path_d + "/Diarios_stf/" + data + "_STF")
                    counter += 1
                except Exception as e:
                    print(e)
                    break
                break


if __name__ == "__main__":
    # cursor = cursorConexao()
    c = crawler_jurisprudencia_stf()
    c.download_diario_retroativo()
