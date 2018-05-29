 # -*- coding: utf-8 -*-

from crawlers.common.conexao_local import cursorConexao
from common_nlp.mNB_classification_text import mNB_classification_text
import numpy as np


cursor = cursorConexao()
cursor.execute('SELECT texto_decisao, classificacao from jurisprudencia_2_inst.jurisprudencia_2_inst where classificacao is not null limit 50;')
dados = cursor.fetchall()
print(len(dados))
# acuracia = np.array([])
mNB = mNB_classification_text(dados)

cursor.execute('SELECT texto_decisao, classificacao from jurisprudencia_2_inst.jurisprudencia_2_inst where classificacao is not null limit 51,1;')
examples = cursor.fetchall()
for e, class_e in examples:
	print(e.encode('utf-8'),mNB.test_mNB([e.encode('utf-8')]),(mNB.test_mNB([e.encode('utf-8')]) == class_e))
# print(np.mean(acuracia))