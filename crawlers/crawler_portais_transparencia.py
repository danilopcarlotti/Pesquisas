from crawlerJus import crawlerJus
from selenium import webdriver
import pandas as pd, time, subprocess

class crawler_portais_transparencia(crawlerJus):
	"""crawler para obtenção de informações de portais de transparência"""
	def __init__(self, path_csv):
		crawlerJus.__init__(self)
		self.df_portais = pd.read_csv(path_csv+'portais_transparencia.csv')
	
	def download_portais(self, download_path, final_path, ano_xpath):
		for _, row in self.df_portais.iterrows():
			driver = webdriver.Chrome(self.chromedriver)
			driver.get(row['link'])
			if input('Clique no ano\n'):
				driver.execute_script("return ProcessaDados('lnkLicitacoes');")
			if input('Clique em download\n'):
				driver.execute_script("return ProcessaDados('lnkContratos');")
			if input('Clique em download\n'):
				nome_pasta = row['prefeitura']
				subprocess.Popen('mkdir "%s/%s"' % (final_path,nome_pasta), shell=True) 
				subprocess.Popen('mv %s/*.csv "%s/%s/"' % (download_path,final_path,nome_pasta), shell=True)
			driver.close()

if __name__ == '__main__':
	c = crawler_portais_transparencia('/mnt/Dados/Documents/pesquisas_privado_dados/compras_publicas/')
	print(c.download_portais('/home/danilo/Downloads','/mnt/Dados/Documents/pesquisas_privado_dados/compras_publicas/Portais transparência/Transparencia 2019','//*[@id="cmbExercicio_DDD_L_LBI6T0"]'))