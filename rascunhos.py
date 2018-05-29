 # -*- coding: utf-8 -*-

from crawlers.common.conexao_local import cursorConexao
from common_nlp.mNB_classification_text import mNB_classification_text
import numpy as np


cursor = cursorConexao()
cursor.execute('SELECT texto_decisao, classificacao from jurisprudencia_2_inst.jurisprudencia_2_inst where classificacao is not null limit 700;')
dados = cursor.fetchall()
mNB = mNB_classification_text(dados)

acuracia = []
cursor.execute('SELECT texto_decisao, classificacao from jurisprudencia_2_inst.jurisprudencia_2_inst where classificacao is not null limit 700,20;')
examples = cursor.fetchall()
for e, class_e in examples:
	if (mNB.test_mNB([e.encode('utf-8')]) == class_e):
		acuracia.append(1)
	else:
		acuracia.append(0)
print(np.mean(acuracia))

acuracia = []
cursor.execute('SELECT texto_decisao, classificacao from jurisprudencia_2_inst.jurisprudencia_2_inst where classificacao is not null limit 720,20;')
examples = cursor.fetchall()
for e, class_e in examples:
	if (mNB.test_mNB([e.encode('utf-8')]) == class_e):
		acuracia.append(1)
	else:
		acuracia.append(0)
print(np.mean(acuracia))

acuracia = []
cursor.execute('SELECT texto_decisao, classificacao from jurisprudencia_2_inst.jurisprudencia_2_inst where classificacao is not null limit 740,20;')
examples = cursor.fetchall()
for e, class_e in examples:
	if (mNB.test_mNB([e.encode('utf-8')]) == class_e):
		acuracia.append(1)
	else:
		acuracia.append(0)
print(np.mean(acuracia))

acuracia = []
cursor.execute('SELECT texto_decisao, classificacao from jurisprudencia_2_inst.jurisprudencia_2_inst where classificacao is not null limit 760,20;')
examples = cursor.fetchall()
for e, class_e in examples:
	if (mNB.test_mNB([e.encode('utf-8')]) == class_e):
		acuracia.append(1)
	else:
		acuracia.append(0)
print(np.mean(acuracia))

acuracia = []
cursor.execute('SELECT texto_decisao, classificacao from jurisprudencia_2_inst.jurisprudencia_2_inst where classificacao is not null limit 780,20;')
examples = cursor.fetchall()
for e, class_e in examples:
	if (mNB.test_mNB([e.encode('utf-8')]) == class_e):
		acuracia.append(1)
	else:
		acuracia.append(0)
print(np.mean(acuracia))