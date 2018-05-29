from crawlers.common.conexao_local import cursorConexao
from common_nlp.mNB_classification_text import mNB_classification_text
import numpy as np, pandas as pd


cursor = cursorConexao()
cursor.execute('SELECT texto_decisao, classificacao from jurisprudencia_2_inst.jurisprudencia_2_inst where classificacao is not null;')
dados = cursor.fetchall()
mNB = mNB_classification_text(dados[:700])
df = mNB.dataframe
df.to_csv('testes_saude.csv',sep=';',quotechar='"')
