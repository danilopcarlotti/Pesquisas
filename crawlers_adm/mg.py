from bs4 import BeautifulSoup
import re
import urllib.request
from download_path import path


def download_ementario_tributario():
    """Função para fazer o download de emntário elaborado
    pela secretaria da Fazenda do Estado de Minas Gerais"""
    link_master = "http://www.fazenda.mg.gov.br/secretaria/conselho_contribuintes/acordaos/ap{}{}{}.html"
    links = []
    for dia in range(1, 32):
        for mes in range(1, 12):
            for ano in range(2009, 2020):
                dia = str(dia)
                mes = str(mes)
                ano = str(ano)[-2:]
                if len(dia) == 1:
                    dia = "0" + dia
                if len(mes) == 1:
                    mes = "0" + mes
                links.append(link_master.format(dia, mes, ano))
    for link_ini in links:
        try:
            links_baixar = []
            req = urllib.request.Request(
                link_ini, headers={"User-Agent": "Mozilla/5.0"}
            )
            html = urllib.request.urlopen(req, timeout=30).read()
            pag = BeautifulSoup(html, "html.parser")
            for l in pag.find_all("a", href=True):
                if re.search(r"\.pdf", l["href"]):
                    links_baixar.append("http://www.fazenda.mg.gov.br" + l["href"])
            for link in links_baixar:
                response = urllib.request.urlopen(link, timeout=60)
                file = open(path + "/MG/" + link.split("/")[-1], "wb")
                file.write(response.read())
                file.close()
        except Exception as e:
            pass


if __name__ == "__main__":
    download_ementario_tributario()
