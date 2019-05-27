from datetime import datetime
import pickle, pandas as pd, jellyfish, re

def encontra_string_semelhante(lista_nomes, stringAnalisada, nCaracteres):
	maior_semelhanca = 0
	item_normalizado = ''
	if nCaracteres:
		for item in lista_nomes:
			ratio_s = jellyfish.jaro_distance(stringAnalisada[:nCaracteres],item[:nCaracteres])
			if ratio_s > maior_semelhanca:
				maior_semelhanca = ratio_s
				item_normalizado = item
		if maior_semelhanca > 0.7:
			return item_normalizado
		else:
			return encontra_string_semelhante(lista_nomes, stringAnalisada, nCaracteres - 15)
	else:
		return 'Outros'


def main():
	pass
	
if __name__ == '__main__':
	main()