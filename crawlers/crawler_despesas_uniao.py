import urllib.request
import json
import pymongo
import time
import glob
import sys

from bs4 import BeautifulSoup

link_licitacoes = "http://compras.dados.gov.br/licitacoes/v1/licitacoes.json?offset={}"
link_pregoes = "http://compras.dados.gov.br/pregoes/v1/pregoes.json?offset={}" #!

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
dbCN = myclient["Comprasnet"]
col_licitacoes = dbCN["licitacoes"]


def download_licitacoes_uniao(path, beg=0, end=1205364):
    for i in range(beg, end, 500):
        session = myclient.start_session()
        print("Faltam ", end - i)
        rows_to_insert = []
        try:
            with urllib.request.urlopen(link_licitacoes.format(i)) as url:
                data = json.loads(url.read().decode("utf-8"))
                for lic in data["_embedded"]["licitacoes"]:
                    dic_aux = {}
                    for k in lic:
                        if k == "_links":
                            continue
                        dic_aux[k] = lic[k]
                    dic_aux["link_contrato"] = lic["_links"]["contratos"]["href"]
                    dic_aux["link_itens"] = lic["_links"]["itens"]["href"]
                    dic_aux["link_edital"] = lic["_links"]["link_edital"]["href"]
                    rows_to_insert.append(dic_aux)
                json.dump(data, open(path.format(i), "w"))
            time.sleep(0.5)
        except Exception as e:
            print(e)
            time.sleep(5)
        if len(rows_to_insert):
            col_licitacoes.insert_many(rows_to_insert, ordered=False)
        myclient.admin.command("refreshSessions", [session.session_id], session=session)


def parse_json_licitacoes(path, beg=0, end=1205364):
    for i in range(beg, end, 500):
        print("Faltam ", end - i)
        rows_to_insert = []
        try:
            with open(path.format(i), encoding='utf-8') as fh:
                data = json.load(fh)
                for lic in data["_embedded"]["licitacoes"]:
                    dic_aux = {}
                    for k in lic:
                        if k == "_links":
                            continue
                        dic_aux[k] = lic[k]
                    if "contratos" in lic["_links"]:
                        dic_aux["link_contrato"] = lic["_links"]["contratos"]["href"]
                    if "itens" in lic["_links"]:
                        dic_aux["link_itens"] = lic["_links"]["itens"]["href"]
                    if "link_edital" in lic["_links"]:
                        dic_aux["link_edital"] = lic["_links"]["link_edital"]["href"]
                    rows_to_insert.append(dic_aux)
        except Exception as e:
            print(e)
        if len(rows_to_insert):
            col_licitacoes.insert_many(rows_to_insert, ordered=False)


def download_info_certames(col_download):
    path_master = "http://compras.dados.gov.br"
    links_folder = [
        ("link_contrato", "contratos", path_master, ("/contratos?","/contratos.json?")),
        ("link_itens", "itens", path_master, ("/itens","/itens.json")),
    ]
    counter = 0
    session = myclient.start_session()
    cursor = col_download.find(
        {},
        no_cursor_timeout=True
    )
    files_downloaded = set([i.split("\\")[1].split(".")[0] for i in glob.glob('Z:/data/raw/Despesas_uniao/contratos/**/*.json',recursive=True)])
    print("Quantidade de arquivos baixados", len(files_downloaded))
    for dic_data in cursor:
        if "identificador" not in dic_data or str(dic_data["identificador"]) in files_downloaded:
            continue
        for name, folder_n, prefix, replace_str in links_folder:
            if name in dic_data:
                try:
                    with urllib.request.urlopen(prefix+dic_data[name].replace(replace_str[0],replace_str[1]), timeout=30) as url:
                        data = json.loads(url.read().decode("utf-8"))
                        json.dump(data, open("Z:/data/raw/Despesas_uniao/{}/{}.json".format(folder_n, dic_data["identificador"]), "w"))
                except:
                    pass
        if "link_edital" in dic_data:
            try:
                with urllib.request.urlopen(dic_data["link_edital"], timeout=30) as html:
                    soup = BeautifulSoup(html, "lxml")
                    for script in soup(["script", "style"]):
                        script.extract()
                    arq = open("Z:/data/raw/Despesas_uniao/editais/{}.txt".format(dic_data["identificador"]),"w",encoding="utf-8")
                    arq.write(soup.get_text())
            except:
                pass
        counter += 1
        if counter > 10:
            myclient.admin.command("refreshSessions", [session.session_id], session=session)
            session = myclient.start_session()
            counter = 0
    cursor.close()
    return True


if __name__ == "__main__":
    # download_licitacoes_uniao("Z:/data/raw/Despesas_uniao/licitacoes/{}.json")
    # parse_json_licitacoes("Z:/data/raw/Despesas_uniao/licitacoes/{}.json")
    done = False
    while not done:
        try:
            done = download_info_certames(col_licitacoes)
        except Exception as e:
            print(e)
