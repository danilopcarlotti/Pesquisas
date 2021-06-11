import pymongo
import pandas as pd

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
DATABASE = myclient["diariosCnj"]
COLLECTION_PROCESSOS = DATABASE["processos"]
COLLECTION_PUBLICACOES = DATABASE["publicacoes"]

rows_processos = []
for c in COLLECTION_PROCESSOS.find({}).limit(50):
    rows_processos.append(c)
df_processos = pd.DataFrame(rows_processos)
df_processos.to_excel("diário_cnj_exemplo_processos.xlsx", index=False)

rows_publicacoes = []
for c in COLLECTION_PUBLICACOES.find({}).limit(50):
    rows_publicacoes.append(c)
df_publicacoes = pd.DataFrame(rows_publicacoes)
df_publicacoes.to_excel("diário_cnj_exemplo_publicacoes.xlsx", index=False)
