import pandas as pd

class crawler_portais_transparencia():
	"""crawler para obtenção de informações de portais de transparência"""
	def __init__(self):
		self.df_portais = pd.read_excel('portais_transparencia.xls')
		self.dicionario_metodo_download = {}

def main():
	c = crawler_portais_transparencia()
	

if __name__ == '__main__':
	main()