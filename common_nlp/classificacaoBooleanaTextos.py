import re, pandas as pd
from parserTextoJuridico import parserTextoJuridico

class classificacaoBooleanaTextos():
	"""docstring for classificacaoBooleanaTextos
"""
	def __init__(self, dicionario_bool):
		self.var_bool = dicionario_bool
	
	def variaveis_textos(self, dicionario_outros, dados, to_csv=False, titulo=None):
		rows = []
		index = []
		index_counter = 1
		for id_p, texto in dados:
			dicionario_df = {'numero':id_p}
			for k,v in dicionario_outros.items():
				if re.search(v, texto):
					dicionario_df[k] = 1
				else:
					dicionario_df[k] = 0
			rows.append(dicionario_df)
			index.append(index_counter)
			index_counter += 1
		data_frame = pd.DataFrame(rows, index=index)
		if to_csv and titulo:
			data_frame.to_csv(titulo+'.csv',quotechar='"', index= False)
		else:
			return data_frame
