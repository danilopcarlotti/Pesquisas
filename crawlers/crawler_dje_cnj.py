import json
import ssl
import urllib.request

import pymongo
import sys

from common.download_path_diarios import path as path_d
from crawler_jurisprudencia_tj import crawler_jurisprudencia_tj


class crawler_jurisprudencia_cnj:
    """Crawler especializado em retornar textos da jurisprudência de segunda instância de Maranhão"""

    def __init__(self):
        crawler_jurisprudencia_tj.__init__(self)
        ssl._create_default_https_context = ssl._create_unverified_context
        self.link_inicial = "https://hcomunicaapi.cnj.jus.br/api/v1/comunicacao?dataDisponibilizacaoInicio={}&dataDisponibilizacaoFim={}"
        self.myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        self.DATABASE = self.myclient["diariosCnj"]
        self.COLLECTION_PROCESSOS = self.DATABASE["processos"]
        self.COLLECTION_PUBLICACOES = self.DATABASE["publicacoes"]

    def download_diario_retroativo(self, data_especifica=None):
        self.lista_anos = ["2021"]
        datas = []
        if data_especifica:
            datas.append(data_especifica)
        else:
            for l in range(len(self.lista_anos)):
                for i in range(1, 10):
                    for j in range(1, 10):
                        datas.append(
                            str(self.lista_anos[l]) + "-0" + str(i) + "-0" + str(j)
                        )
                    for j in range(10, 32):
                        datas.append(
                            str(self.lista_anos[l]) + "-0" + str(i) + "-" + str(j)
                        )
                for i in range(10, 13):
                    for j in range(1, 10):
                        datas.append(
                            str(self.lista_anos[l]) + str(i) + "-0" + "-" + str(j)
                        )
                    for j in range(10, 32):
                        datas.append(
                            str(self.lista_anos[l]) + "-" + str(i) + "-" + str(j)
                        )
        for data in range(len(datas) - 1):
            print(datas[data])
            try:
                response = urllib.request.urlopen(
                    self.link_inicial.format(datas[data], datas[data + 1]), timeout=15
                )
                file = open(path_d + "/" + str(datas[data]) + ".json", "wb")
                file.write(response.read())
                file.close()
            except Exception as e:
                print(e)

    def parser_json(self, json_file):
        pubs = []
        with open(json_file, encoding="utf-8") as f:
            data = json.load(f)
            for item in data["items"]:
                query_proc = {"_id": item["numeroprocessocommascara"]}
                update_proc = {
                    "$set": {
                        "_id": item["numeroprocessocommascara"],
                        "ativo": item["ativo"],
                        "siglaTribunal": item["siglaTribunal"],
                    }
                }
                self.COLLECTION_PROCESSOS.update_one(
                    query_proc, update_proc, upsert=True
                )
                for destinatario in item["destinatarios"]:
                    if "polo" in destinatario:
                        if destinatario["polo"] == "A":
                            update_proc = {"$set": {"poloA": destinatario["nome"]}}
                            self.COLLECTION_PROCESSOS.update_one(
                                query_proc, update_proc, upsert=True
                            )
                        elif destinatario["polo"] == "P":
                            update_proc = {"$set": {"poloP": destinatario["nome"]}}
                            self.COLLECTION_PROCESSOS.update_one(
                                query_proc, update_proc, upsert=True
                            )
                pubs.append(
                    {
                        "numeroprocessocommascara": item["numeroprocessocommascara"],
                        "data_disponibilizacao": item["data_disponibilizacao"],
                        "tipoComunicacao": item["tipoComunicacao"],
                        "nomeOrgao": item["nomeOrgao"],
                        "texto": item["texto"],
                        "tipoDocumento": item["tipoDocumento"],
                        "codigoClasse": item["codigoClasse"],
                        "nomeClasse": item["nomeClasse"],
                        "destinatarioadvogados": item["destinatarioadvogados"],
                    }
                )
            if len(pubs) > 5000:
                self.COLLECTION_PUBLICACOES.insert_many(pubs)
                pubs = []
        if len(pubs):
            self.COLLECTION_PUBLICACOES.insert_many(pubs)


if __name__ == "__main__":
    c = crawler_jurisprudencia_cnj()

    c.download_diario_retroativo()

    import glob

    for f in glob.glob("D:/Diarios_cnj/*.json"):
        print(f)
        c.parser_json(f)
