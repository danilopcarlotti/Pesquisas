import pymongo, sys, re, pandas as pd, os

sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))
from Pesquisas.common.recursive_folders import recursive_folders

def insere_publicacoes(path_arquivo, collection_andamentos):
    df = pd.read_csv(path_arquivo, chunksize=100)
    tribunal = re.search(r'/Diarios_(.*?)/',path_arquivo)
    if tribunal:
        tribunal = tribunal.group(1)
    else:
        return
    for chunk in df:
        for index, row in chunk.iterrows():
            numero = str(row['numero_processo']).replace('/','').replace('-','').replace('.','')
            texto = row['texto_publicacao'].replace('\n',' ')
            if len(numero) > 10:
                if collection_andamentos.find_one({'_id':numero}):
                    collection_andamentos.update_one({'_id':numero}, 
                        {"$push":
                            {'textos_publicacoes':texto,
                            'nome_arquivo':row['nome_arquivo'],
                            'data':row['data']
                            }
                        })
                else:
                    collection_andamentos.insert_one({
                        '_id':numero,
                        'tribunal':row['tribunal'],
                        'textos_publicacoes':[texto],
                        'nome_arquivo':[row['nome_arquivo']],
                        'data':[row['data']]
                    })	

def main(path_diarios, uri_mongo):
	# VARIÁVEIS DA COLLECTION NA BASE MONGODB
	if not uri_mongo:
		uri_mongo = "mongodb://localhost:27017/"
	myclient = pymongo.MongoClient(uri_mongo)
	mydb = myclient["jurisprudencia"]
	collection_andamentos = mydb['andamentos']

	rec = recursive_folders()
	diarios_processar = [i for i in rec.find_files(path_diarios) if i[-4:] == '.csv']
	for diario in diarios_processar:
		try:
			insere_publicacoes(diario, collection_andamentos)
		except Exception as e:
			print(diario)
			print(e)

if __name__ == '__main__':
	# if len(sys.argv) == 2:
	# 	main(sys.argv[1], None)
	# else:
	# 	main(sys.argv[1], sys.argv[2])
    # main_datas('/media/danilo/Seagate Expansion Drive/Diarios')
    main_datas('/media/danilo/Seagate Expansion Drive/Diarios/Diarios_trf5')