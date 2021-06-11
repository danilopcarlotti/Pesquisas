from bs4 import BeautifulSoup
from crawler_jurisprudencia_tj import crawler_jurisprudencia_tj
from crawlerJus import crawlerJus
from common.conexao_local import cursorConexao
from common.download_path import path, path_hd
from common.download_path_diarios import path as path_d
from selenium import webdriver
import sys, re, os, time, urllib.request, subprocess

sys.path.append(os.path.dirname(os.getcwd()))
from common_nlp.parse_texto import busca


class crawler_jurisprudencia_tjdf(crawler_jurisprudencia_tj):
    """Crawler especializado em retornar textos da jurisprudência de segunda instância do Distrito Federal"""

    def __init__(self):
        crawler_jurisprudencia_tj.__init__(self)
        self.link_inicial = "https://pesquisajuris.tjdft.jus.br/IndexadorAcordaos-web/sistj?visaoId=tjdf.sistj.acordaoeletronico.buscaindexada.apresentacao.VisaoBuscaAcordao&nomeDaPagina=buscaLivre2&buscaPorQuery=1&baseSelecionada=BASE_ACORDAOS&ramoJuridico=&baseDados=[BASE_ACORDAOS,%%20TURMAS_RECURSAIS]&argumentoDePesquisa=a&filtroSegredoDeJustica=false&desembargador=&indexacao=&tipoDeNumero=NumAcordao&tipoDeRelator=TODOS&camposSelecionados=[ESPELHO]&numero=&tipoDeData=DataPublicacao&dataFim=&dataInicio=&ementa=&orgaoJulgador=&filtroAcordaosPublicos=false&legislacao=&numeroDaPaginaAtual=%s&quantidadeDeRegistros=20&totalHits=799443"
        self.tabela_colunas = "justica_estadual.jurisprudencia_df (ementas)"
        self.tabela_colunas_1_inst = (
            "justica_estadual.jurisprudencia_df_1_inst (sentencas)"
        )

    def download_diario_retroativo(self):

        # checar o ano e número de diários no ano!!!!
        # https://dje.tjdft.jus.br/dje/djeletronico?visaoId=tjdf.djeletronico.comum.internet.apresentacao.VisaoDiarioEletronicoInternetPorData

        # 240 diários por ano. Salvo 2018, que tem, atualmente 130
        link_inicial = "https://dje.tjdft.jus.br/dje/jsp/dje/DownloadDeDiario.jsp?dj=DJ%s_%s-ASSINADO.PDF&statusDoDiario=ASSINADO"
        for l in range(len(self.lista_anos)):
            for i in range(240, 0, -1):
                try:
                    # print(link_inicial % (str(i),self.lista_anos[l]))
                    response = urllib.request.urlopen(
                        link_inicial % (str(i), self.lista_anos[l]), timeout=15
                    )
                    file = open(str(i) + "_" + self.lista_anos[l] + ".pdf", "wb")
                    file.write(response.read())
                    file.close()
                    subprocess.Popen(
                        'mv %s/*.pdf "%s/Diarios_df"' % (os.getcwd(), path_d),
                        shell=True,
                    )
                except Exception as e:
                    print(e)

    def download_tj(self, ultima_pag):
        cursor = cursorConexao()
        for i in range(ultima_pag):
            try:
                time.sleep(5)
                link = self.link_inicial % str(i)
                driver = webdriver.Chrome(self.chromedriver)
                driver.get(link)
                lista_acordaos = driver.find_elements_by_id(
                    "id_link_abrir_dados_acordao"
                )
                for i in range(len(lista_acordaos)):
                    lista_acordaos_aux = driver.find_elements_by_id(
                        "id_link_abrir_dados_acordao"
                    )
                    lista_acordaos_aux[i].click()
                    divs_com_rotulo = driver.find_elements_by_class_name(
                        "conteudoComRotulo"
                    )
                    links_inteiro_teor = divs_com_rotulo[-1].find_elements_by_tag_name(
                        "span"
                    )
                    try:
                        links_inteiro_teor[0].click()
                    except:
                        pass
                    time.sleep(1)
                    driver.find_element_by_id("id_comando_voltar_supra").click()
                driver.close()
            except Exception as e:
                print(e)

    # def parser_acordaos(self, arquivo, cursor):
    #     texto = (
    #         docx2txt.process(arquivo)
    #         .replace("\\", "")
    #         .replace("/", "")
    #         .replace('"', "")
    #     )
    #     numero = busca(r"\n\s*?N.\s*?Processo\s*?\:(.*?)\n", texto)
    #     if numero == "":
    #         numero = busca(r"\n\s*?Processo N.\s*?\n\n.*?(\d{10,30})", texto)
    #     julgador = busca(r"\n\s*?Desembargador(.*?)\n", texto)
    #     data_decisao = busca(r"\n\s*?Brasília \(DF\)\, (.*?)\n", texto)
    #     orgao_julgador = busca(r"\n\s*?Órgão.*?\n\n(.*?)\n", texto)
    #     cursor.execute(
    #         'INSERT INTO jurisprudencia_2_inst.jurisprudencia_2_inst (tribunal, numero, data_decisao, orgao_julgador, julgador, texto_decisao) values ("%s","%s","%s","%s","%s","%s");'
    #         % ("df", numero, data_decisao, orgao_julgador, julgador, texto)
    #     )


def main():
    c = crawler_jurisprudencia_tjdf()
    print("comecei ", c.__class__.__name__)
    try:
        c.download_tj(40000)  # número atualizado em jan 2018
    except Exception as e:
        print(e)
    subprocess.Popen(
        "cd %s;for A in *.doc; do libreoffice --headless --convert-to docx $A; done; libreoffice --headless --convert-to docx *.doc; rm *.doc;"
        % (path + "/df_2_inst/",),
        shell=True,
    )
    cursor = cursorConexao()
    for arq in os.listdir(path + "/df_2_inst"):
        if re.search(r"docx", arq):
            try:
                c.parser_acordaos(path + "/df_2_inst/" + arq, cursor)
            except Exception as e:
                print(arq, e)


if __name__ == "__main__":
    # main()
    c = crawler_jurisprudencia_tjdf()
    c.download_diario_retroativo()
