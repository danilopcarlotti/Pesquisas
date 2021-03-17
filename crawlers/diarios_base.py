import pymongo, sys, re, pandas as pd, os, pickle, gc

sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))
from pesquisas.common.recursive_folders import recursive_folders


def insere_publicacoes(path_arquivo, collection_andamentos):
    df = pd.read_csv(path_arquivo, chunksize=100)
    tribunal = re.search(r"/Diarios_(.*?)/", path_arquivo)
    if tribunal:
        tribunal = tribunal.group(1)
    else:
        return
    for chunk in df:
        for _, row in chunk.iterrows():
            numero = (
                str(row["numero_processo"])
                .replace("/", "")
                .replace("-", "")
                .replace(".", "")
            )
            texto = row["texto_publicacao"].replace("\n", " ")
            if len(numero) > 10:
                if collection_andamentos.find_one({"_id": numero}):
                    collection_andamentos.update_one(
                        {"_id": numero},
                        {
                            "$push": {
                                "textos_publicacoes": texto,
                                "data": row["data"],
                                "tipo_publicacao": -1,
                            }
                        },
                    )
                else:
                    collection_andamentos.insert_one(
                        {
                            "_id": numero,
                            "tribunal": row["tribunal"],
                            "textos_publicacoes": [texto],
                            "data": [row["data"]],
                            "tipo_publicacao": [-1],
                        }
                    )


def insere_publicacoes_condicional(
    path_arquivo, collection_andamentos, dicionario_processos
):
    print(path_arquivo)
    df = pd.read_csv(path_arquivo, chunksize=100)
    for chunk in df:
        for _, row in chunk.iterrows():
            # numero = str(row['numero_processo']).replace('/','').replace('-','').replace('.','')
            numero = str(row["numero_processo"])
            if numero not in dicionario_processos:
                continue
            texto = row["texto_publicacao"].replace("\n", " ")
            if len(numero) > 10:
                if collection_andamentos.find_one({"_id": numero}):
                    collection_andamentos.update_one(
                        {"_id": numero},
                        {
                            "$push": {
                                "textos_publicacoes": texto,
                                "data": row["data"],
                                "tipo_publicacao": -1,
                            }
                        },
                    )
                else:
                    collection_andamentos.insert_one(
                        {
                            "_id": numero,
                            "tribunal": row["tribunal"],
                            "textos_publicacoes": [texto],
                            "data": [row["data"]],
                            "tipo_publicacao": [-1],
                        }
                    )


def separa_publicacoes_frases_interesse(collection_andamentos, uri_mongo=None):
    for d in collection_andamentos.find({}):
        for pub in d["textos_publicacoes"]:
            pass


def main(
    path_diarios,
    uri_mongo,
    collection_name=None,
    condicional=False,
    dicionario_processos=None,
):
    # VARIÁVEIS DA COLLECTION NA BASE MONGODB
    if not uri_mongo:
        uri_mongo = "mongodb://localhost:27017/"
    myclient = pymongo.MongoClient(uri_mongo)
    mydb = myclient["jurisprudencia"]
    if collection_name:
        collection_andamentos = mydb[collection_name]
    else:
        collection_andamentos = mydb["andamentos"]
    rec = recursive_folders()
    diarios_processar = [i for i in rec.find_files(path_diarios) if i[-4:] == ".csv"]
    for diario in diarios_processar:
        try:
            if condicional:
                insere_publicacoes_condicional(
                    diario, collection_andamentos, dicionario_processos
                )
            else:
                insere_publicacoes(diario, collection_andamentos)
        except Exception as e:
            print(diario)
            print(e)
        gc.collect()


# if __name__ == '__main__':
# if len(sys.argv) == 2:
# 	main(sys.argv[1], None)
# else:
# 	main(sys.argv[1], sys.argv[2])

# dicionario = pickle.load(open('/home/deathstar/Documents/pesquisas_privado/possessoria/dicionario_acoes.pickle','rb'))
# main('/home/deathstar/Dados/Diarios', None, collection_name='jurisprudencia_possessoria', condicional=True, dicionario_processos=dicionario)

# # BAIXAR DADOS
# uri_mongo = "mongodb://localhost:27017/"
# myclient = pymongo.MongoClient(uri_mongo)
# mydb = myclient["jurisprudencia"]
# my_col = mydb['jurisprudencia_possessoria']
# rows = []
# for d in my_col.find({}):
#     for i in range(len(d['textos_publicacoes'])):
#         rows.append({
#             'tribunal':d['tribunal'],
#             'numero_processo':d['_id'],
#             'texto_publicacao':d['textos_publicacoes'][i],
#             'data':d['data'][i]
#         })
# df_new = pd.DataFrame(rows,index=[i for i in range(len(rows))])
# df_new.to_csv('/home/deathstar/Documents/pesquisas_privado/possessoria/extracao_possessoria_final.csv',index=False)
