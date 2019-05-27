import pandas as pd

class remove_duplicates_pandas():
	def __init__(self):
		pass

	def read_file(self, filepath, typedf):
		if typedf == 'csv':
			return pd.read_csv(filepath)
		elif typedf == 'excel':
			return pd.read_excel(filepath)

	def remove_duplicates(self, filepath, typedf, target_column, new_file='arquivo_sem_duplicatas.'):
		df = self.read_file(filepath, typedf)
		columns = df.columns
		rows_new_df = []
		targets = []
		for index, row in df.iterrows():
			if row[target_column] not in targets:
				targets.append(row[target_column])
				dictionary_row = {}
				for c in columns:
					dictionary_row[c] = row[c]
				rows_new_df.append(dictionary_row)
		df_new = pd.DataFrame(rows_new_df,index=[i for i in range(len(rows_new_df))])
		if typedf == 'csv':
			df_new.to_csv(new_file+'csv')
		elif typedf == 'excel':
			df_new.to_excel(new_file+'xlsx')

def main(filepath, typedf, target_column):
	rem = remove_duplicates_pandas()
	rem.remove_duplicates(filepath, typedf, target_column)

if __name__ == '__main__':
	main('/media/danilo/66F5773E19426C79/CNJ_jud_saude/relatorio_booleano_cnj_16_jan_2019_sp.xlsx','excel','numero')