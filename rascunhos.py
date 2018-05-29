from crawlers.common.conexao_local import cursorConexao
from common_nlp.mNB_classification_text import mNB_classification_text
import numpy as np


cursor = cursorConexao()
cursor.execute('SELECT texto_decisao, classificacao from jurisprudencia_2_inst.jurisprudencia_2_inst where classificacao is not null limit 5;')
dados = cursor.fetchall()
acuracia = np.array([])
for i in range(1,len(dados)-1):
	dados_treino = dados[:i]+dados[i+1:]
	dados_teste = dados[i]
	mNB = mNB_classification_text(dados_treino)
	for texto, class_t in dados_teste:
		if (mNB.test_mNB([texto]) == class_t):
			acuracia = 1
		else:
			acuracia = 0
		acuracia.insert(int(classificacao))
print(np.mean(acuracia))