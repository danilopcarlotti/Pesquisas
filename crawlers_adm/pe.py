import sys
import re
import os
import pandas as pd
import urllib.request
from tika import parser
from download_path import path

sys.path.append(os.path.dirname(os.getcwd()))
from common.recursive_folders import recursive_folders


def download_ementario_tributario(link, nome_arq):
    """Função para fazer o download de emntário elaborado
    pela secretaria da Fazenda do Estado de São Paulo"""
    response = urllib.request.urlopen(link, timeout=60)
    file = open(path + "/PE/" + nome_arq + ".pdf", "wb")
    file.write(response.read())
    file.close()


def transform_pdfs_ementario_tributario():
    rec = recursive_folders()
    files = [i for i in rec.find_files(path + "/PE") if i[-3:] == "pdf"]
    for f in files:
        file_data = parser.from_file(f)
        texto = file_data["content"]
        arq = open(f.replace("pdf", "txt"), "w", encoding="utf-8")
        arq.write(texto)
        arq.close()


def parse_ementario_tributario():
    rec = recursive_folders()
    files = [i for i in rec.find_files(path + "/PE") if i[-3:] == "txt"]
    for f in files:
        rows = []
        texto = " ".join([line for line in open(f, "r", encoding="utf-8")])
        pubs = [
            re.sub(r"\s+", " ", i)
            for i in re.split(
                r"\n\s*?RECURSO ORDINÁRIO|\n\s*?CONSULTA SF|\n\s*?REEXAME NECESSÁRIO|\n\s*?PEDIDO  DE  REVISÃO|\n\s*?AI\s*?SF",
                texto,
                flags=re.S,
            )[1:]
            if i and len(i) > 100
        ]
        for pub in pubs:
            rows.append(
                {
                    "texto_publicacao": pub,
                }
            )
        df = pd.DataFrame(rows)
        df.to_csv(f.replace(".txt", ".csv"), index=False)


if __name__ == "__main__":
    # PRIMEIRO SEMESTRE DE 2020
    # link_2013_em_diante_pleno = "https://www.sefaz.pe.gov.br/Servicos/TATE/Acordaos%20%20Primeira%20Turma/A%20PARTIR%20DE%202013%20-%20PLENO.pdf"
    # link_2013_em_diante_turmas = "https://www.sefaz.pe.gov.br/Servicos/TATE/Acordaos%20%20Primeira%20Turma/A%20PARTIR%20DE%202013%20-%20TURMAS.pdf"
    # print("Fazendo download")
    # download_ementario_tributario(link_2013_em_diante_pleno, "2013_em_diante_pleno")
    # download_ementario_tributario(link_2013_em_diante_turmas, "2013_em_diante_turmas")
    # print("Transformando pdfs em txts")
    # transform_pdfs_ementario_tributario()
    print("Parsing ementario")
    parse_ementario_tributario()
