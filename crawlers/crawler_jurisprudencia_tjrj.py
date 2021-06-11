from common.download_path_diarios import path as path_d
from crawlerJus import crawlerJus
import urllib.request
import time


class crawler_jurisprudencia_tjrj(crawlerJus):
    """Crawler especializado em retornar textos da jurisprudência de segunda instância do Rio de Janeiro"""

    def __init__(self):
        crawlerJus.__init__(self)

    def download_diario_retroativo(self, data_especifica=None):
        cadernos = ["A", "S", "C", "I", "E"]
        link_inicial = "https://www3.tjrj.jus.br/consultadje/pdf.aspx?dtPub={}&caderno={}&pagina=-1&dc="
        datas = []
        self.lista_anos = [str(i) for i in range(2011, 2022)]
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
                for i in range(10, 13):
                    for j in range(1, 10):
                        datas.append(
                            "0" + str(j) + "/" + str(i) + "/" + self.lista_anos[l]
                        )
                    for j in range(10, 32):
                        datas.append(str(j) + "/" + str(i) + "/" + self.lista_anos[l])
        for data in datas:
            for cad in cadernos:
                try:
                    link_data = link_inicial.format(data, cad)
                    print(link_data)
                    response = urllib.request.urlopen(link_data, timeout=20)
                    file = open(
                        path_d
                        + "/Diarios_rj/"
                        + data.replace("/", "_")
                        + "_"
                        + cad
                        + ".pdf",
                        "wb",
                    )
                    file.write(response.read())
                    file.close()
                    time.sleep(0.2)
                except Exception as e:
                    print(e)


if __name__ == "__main__":
    c = crawler_jurisprudencia_tjrj()
    c.download_diario_retroativo()
