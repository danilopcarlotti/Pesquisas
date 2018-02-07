from common_nlp.textNormalization import textNormalization
from crawlers.common.conexao_local import cursorConexao

cursor = cursorConexao()
cursor.execute('SELECT id, polo_ativo, polo_passivo, assunto from processos_stf.dados_processo limit 1000000;')
metadados = cursor.fetchall()
tn = textNormalization()
# polo_passivo = {}
polo_ativo = {}
assunto = {}
for id_p,p_a,p_p,ass in metadados:
	# polo_passivo_text = set(tn.normalize_text(p_p))
	# for w in polo_passivo_text:
	# 	if w in polo_passivo:
	# 		polo_passivo[w].append(id_p)
	# 	else:
	# 		polo_passivo[w] = [id_p]
	polo_atiov_text = set(tn.normalize_text(p_a))
	for w in polo_ativo_text:
		if w in polo_ativo:
			polo_ativo[w].append(id_p)
		else:
			polo_ativo[w] = [id_p]
	assunto_text = set(tn.normalize_text(ass))
	for w in assunto_text:
		if w in assunto:
			assunto[w].append(id_p)
		else:
			assunto[w] = [id_p]

# for k,v in polo_passivo.items():
# 	cursor.execute('INSERT INTO processos_stf.indice_polo_passivo (palavra,processo) values ("%s","%s");' % (k,v))
for k,v in polo_ativo.items():
	cursor.execute('INSERT INTO processos_stf.indice_polo_ativo (palavra,processo) values ("%s","%s");' % (k,v))
for k,v in assunto.items():
	try:
		cursor.execute('INSERT INTO processos_stf.indice_assunto (palavra,processo) values ("%s","%s");' % (k,v))
	except:
		pass

cursor.execute('SELECT id_processo, texto_decisao from processos_stf.decisoes limit 1000000;')
decisoes = cursor.fetchall()
decisoes_dic = {}
for id_p, texto in decisoes:
	decisoes_text = set(tn.normalize_text(texto))
	for w in decisoes_text:
		if w in decisoes_dic:
			decisoes_dic[w].append(id_p)
		else:
			decisoes_dic[w] = [id_p]

for k,v in decisoes_dic.items():
	try:
		cursor.execute('INSERT INTO processos_stf.indice_votos (palavra,processo) values ("%s","%s");' % (k,v))
	except:
		pass