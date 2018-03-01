from common_nlp.textNormalization import textNormalization
from crawlers.common.conexao_local import cursorConexao

cursor = cursorConexao()
cursor.execute('SELECT id, recorrido from stj.dados_processo_recorrido_ok limit 1000000;')
metadados = cursor.fetchall()
tn = textNormalization()
polo_passivo = {}
for id_p,p_p in metadados:
	polo_passivo_text = set(tn.normalize_texts(p_p,one_text=True))
	for w in polo_passivo_text:
		if w in polo_passivo:
			polo_passivo[w].append(id_p)
		else:
			polo_passivo[w] = [id_p]

for k,v in polo_passivo.items():
	cursor.execute('INSERT INTO stj.indice_polo_passivo (palavra,id_processos) values ("%s","%s");' % (k,v))