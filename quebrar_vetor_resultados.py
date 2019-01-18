import pandas as pd


def quebrar_vetor_resultados():
	df = pd.read_csv('relatorio_booleano_cnj_16_jan_2019_2_inst.csv')
	# [0, 0, 1, 0]
	# FAZER DUMMY VARIABLES A PARTIR DE UM VETOR
	r0 = []
	r1 = []
	r2 = []
	r3 = []
	r4 = []
	for index, row in df.iterrows():
		if row['resultado'] == '[1, 0, 0, 0, 0]':
			r0.append(1)
			r1.append(0)
			r2.append(0)
			r3.append(0)
			r4.append(0)
		elif row['resultado'] == '[0, 1, 0, 0, 0]':
			r0.append(0)
			r1.append(1)
			r2.append(0)
			r3.append(0)
			r4.append(0)
		elif row['resultado'] == '[0, 0, 1, 0, 0]':
			r0.append(0)
			r1.append(0)
			r2.append(1)
			r3.append(0)
			r4.append(0)
		elif row['resultado'] == '[0, 0, 0, 1, 0]':
			r1.append(0)
			r0.append(0)
			r2.append(0)
			r3.append(1)
			r4.append(0)
		else:
			r0.append(0)
			r1.append(0)
			r2.append(0)
			r3.append(0)
			r4.append(1)
	column_r0 = pd.Series(r0, name='r0', index=df.index)
	df['r0'] = column_r0
	column_r1 = pd.Series(r1, name='r1', index=df.index)
	df['r1'] = column_r1
	column_r2 = pd.Series(r2, name='r2', index=df.index)
	df['r2'] = column_r2
	column_r3 = pd.Series(r3, name='r3', index=df.index)
	df['r3'] = column_r3
	column_r4 = pd.Series(r4, name='r4', index=df.index)
	df['r4'] = column_r4
	df.to_csv('relatorio_booleano_cnj_16_jan_2019_2_inst_separados.csv', index= False)

if __name__ == '__main__':
	quebrar_vetor_resultados()