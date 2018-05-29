 # -*- coding: utf-8 -*-

from crawlers.common.conexao_local import cursorConexao
from common_nlp.mNB_classification_text import mNB_classification_text
import numpy as np


cursor = cursorConexao()
cursor.execute('SELECT texto_decisao, classificacao from jurisprudencia_2_inst.jurisprudencia_2_inst where classificacao is not null;')
dados = cursor.fetchall()
mNB = mNB_classification_text(dados[:700])

acuracia = []
examples = dados[700:720]
for e, class_e in examples:
	if (mNB.test_mNB([e.encode('utf-8')]) == class_e):
		acuracia.append(1)
	else:
		acuracia.append(0)
print(np.mean(acuracia))

acuracia = []
examples = dados[720:740]
for e, class_e in examples:
	if (mNB.test_mNB([e.encode('utf-8')]) == class_e):
		acuracia.append(1)
	else:
		acuracia.append(0)
print(np.mean(acuracia))

acuracia = []
examples = dados[740:760]
for e, class_e in examples:
	if (mNB.test_mNB([e.encode('utf-8')]) == class_e):
		acuracia.append(1)
	else:
		acuracia.append(0)
print(np.mean(acuracia))

acuracia = []
examples = dados[760:780]
for e, class_e in examples:
	if (mNB.test_mNB([e.encode('utf-8')]) == class_e):
		acuracia.append(1)
	else:
		acuracia.append(0)
print(np.mean(acuracia))