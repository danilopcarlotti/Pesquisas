from crawlers.common.conexao_local import cursorConexao
import random

def main(tabela, lower, upper, n):
	dados_aleatorios = []
	random.seed()
	cursor = cursorConexao()
	ids_aleatorios = random.sample(range(lower, upper), n*2)
	contador = 0
	id_dado = 0
	while contador < n and id_dado < len(ids_aleatorios):
		cursor.execute('SELECT * FROM %s where id = %s;' % (tabela,str(ids_aleatorios[id_dado])))
		id_dado += 1
		dado = cursor.fetchall()
		if dado:
			contador += 1
			dados_aleatorios.append(dado)
	return dados_aleatorios

if __name__ == '__main__':
	dados = main('jurisprudencia_2_inst.jurisprudencia_2_inst',1324911,10000000 ,10000)
	print(dados)
