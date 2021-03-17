from bs4 import BeautifulSoup
import re
import time
import urllib.request
from download_path import path


def download_ementario_tributario():
    """Função para fazer o download de emntário elaborado
    pela secretaria da Fazenda do Estado do Pará"""
    link_pleno = "http://www.sefa.pa.gov.br/index.php/contencioso/41-contencioso/tarf/pesquisa-de-acordaos/camara-numero/121-trib-pleno"
    link_1cpj = "http://www.sefa.pa.gov.br/index.php/contencioso/tarf/pesquisa-de-acordaos/camara-numero/1050-1-cpj"
    link_2cpj = "http://www.sefa.pa.gov.br/index.php/contencioso/41-contencioso/tarf/pesquisa-de-acordaos/camara-numero/119-2cpj-acordao"
    counter = 1
    for link_ini in [link_pleno, link_1cpj, link_2cpj]:
        links_baixar = []
        req = urllib.request.Request(link_ini, headers={"User-Agent": "Mozilla/5.0"})
        html = urllib.request.urlopen(req, timeout=30).read()
        pag = BeautifulSoup(html, "html.parser")
        for l in pag.find_all("a", href=True):
            if re.search(r"/contencioso", l["href"]):
                links_baixar.append("http://www.sefa.pa.gov.br" + l["href"])
        for link in links_baixar:
            if counter < 5857:
                counter += 1
                continue
            try:
                req = urllib.request.Request(
                    link, headers={"User-Agent": "Mozilla/5.0"}
                )
                html = urllib.request.urlopen(req, timeout=60)
                soup = BeautifulSoup(html, "lxml")
                for script in soup(["script", "style"]):
                    script.extract()
                text = soup.get_text()
                file = open(
                    path + "/PA/" + str(counter) + ".txt", "w", encoding="utf-8"
                )
                file.write("ACÓRDÃO N." + text)
                file.close()
                time.sleep(1)
            except Exception as e:
                print(e)
            counter += 1


if __name__ == "__main__":
    download_ementario_tributario()
