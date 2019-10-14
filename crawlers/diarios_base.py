import pymongo, sys, re, pandas as pd, os

sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))
from Pesquisas.common.recursive_folders import recursive_folders

def month_to_number(month):
    month = month.lower()
    dicionario_meses = {
        'dezembro':'12',
        'novembro':'11',
        'outubro':'10',
        'setembro':'09',
        'agosto':'08',
        'julho':'07',
        'junho':'06',
        'maio':'05',
        'abril':'04',
        'março':'03',
        'fevereiro':'02',
        'janeiro':'01'
    }
    if month in dicionario_meses:
        return dicionario_meses[month]
    else:
        return ' '

def extrair_data_sp(texto):
    data = re.search(r'Diarios_sp/(.*?)/', texto)
    if data:
        data = data.group(1)
        if len(data) == 8:
            return data[:2]+'/'+data[2:4]+'/'+data[4:]
        elif len(data) == 6:
            return '0'+data[0]+'/0'+data[1]+'/'+data[2:]
        elif len(data) == 7:
            if int(data[0]) > 1 or int(data[1]) > 1:
                return data[:2]+'/0'+data[2]+'/'+data[3:]
        else:
            return ''
    else:
        return ''

def extrair_data_pe(arq, path_prefix = '/media/danilo/Seagate Expansion Drive/Diarios/'):
    try:
        path_sufix = arq.split('/Diarios/')[1]
    except:
        return ''
    cabecalho = ''
    contador = 0
    for line in open(path_prefix+path_sufix,'r'):
        if contador > 10:
            break
        else:
            contador += 1
            cabecalho += line
    data_raw = re.search(r'Publicação: (\d{2}/\d{2}/\d{4})', cabecalho)
    if data_raw:
        return data_raw.group(1)
    else:
        return ''

def extrair_data_mt(arq, path_prefix = '/media/danilo/Seagate Expansion Drive/Diarios/'):
    try:
        path_sufix = arq.split('/Diarios/')[1]
    except:
        return ''
    cabecalho = ''
    contador = 0
    for line in open(path_prefix+path_sufix,'r'):
        if contador > 500:
            break
        else:
            contador += 1
            cabecalho += line
    data_raw = re.search(r'DISPONIBILIZADA NO DIÁRIO DA JUSTIÇA ELETRÔNICO, EDIÇÃO .*? DE (\d{2}/\d{2}/\d{4})', cabecalho)
    if data_raw:
        return data_raw.group(1)
    else:
        return ''

def extrair_data_am(texto):
    data = re.search(r'Diarios_am/(.*?)/', texto)
    if data:
        data = data.group(1)
        if len(data) == 8:
            return data[:2]+'/'+data[2:4]+'/'+data[4:]
        elif len(data) == 6:
            return '0'+data[0]+'/0'+data[1]+'/'+data[2:]
        elif len(data) == 7:
            if int(data[0]) > 1 or int(data[1]) > 1:
                return data[:2]+'/0'+data[2]+'/'+data[3:]
        else:
            return '-'
    else:
        return '-'

def extrair_data_trf1(texto):
    data = re.search(r'Diarios_trf1/dir_\d+/.*?(\d{4}\-\d{2}\-\d{2}).*?\.txt', texto)
    if data:
        data = data.group(1).replace('-','')
        return data[-2:]+'/'+data[-4:-2]+'/'+data[:4]
    else:
        return ''
    return ' '

def extrair_data_trf3(arq, path_prefix = '/media/danilo/Seagate Expansion Drive/Diarios/'):
    try:
        path_sufix = arq.split('/Diarios/')[1]
    except:
        return ''
    cabecalho = ''
    contador = 0
    for line in open(path_prefix+path_sufix,'r'):
        if contador > 10:
            break
        else:
            contador += 1
            cabecalho += line
    data_raw = re.search(r'Edição n.*?((\d{2}) de (.*?) de (\d{4}))', cabecalho, re.DOTALL)
    if data_raw:
        day = data_raw.group(2)
        month = month_to_number(data_raw.group(3))
        year = data_raw.group(4)
        return day+'/'+month+'/'+year
    else:
        return ''

def extrair_data_trf4(texto):
    data = re.search(r'Diarios_trf4/(\d{8})\.txt', texto)
    if data:
        data = data.group(1)
        return data[:2]+'/'+data[2:4]+'/'+data[4:]
    else:
        return ''
    return ' '

def extrair_data_trf5(arq, path_prefix = '/media/danilo/Seagate Expansion Drive/Diarios/'):
    try:
        path_sufix = arq.split('/Diarios/')[1]
    except:
        return ''
    cabecalho = ''
    contador = 0
    for line in open(path_prefix+path_sufix,'r'):
        if contador > 20:
            break
        else:
            contador += 1
            cabecalho += line
    data_raw = re.search(r', (\d{2}) (.*?) (\d{4})', cabecalho, re.DOTALL)
    if data_raw:
        day = data_raw.group(1)
        month = month_to_number(data_raw.group(2))
        year = data_raw.group(3)
        return day+'/'+month+'/'+year
    else:
        return ''

def extrair_geral(arq):
	return ' '

def dicionario_funcoes_data(tribunal):
	dicionario_funcoes = {
		'sp':{'f':extrair_data_sp,'i':'texto'},
		'am':{'f':extrair_data_am,'i':'arq'},
		'mt':{'f':extrair_data_mt,'i':'arq'},
		'pe':{'f':extrair_data_pe,'i':'texto'},
        'trf1':{'f':extrair_data_trf1,'i':'texto'},
        'trf3':{'f':extrair_data_trf3,'i':'arq'},
        'trf4':{'f':extrair_data_trf4,'i':'arq'},
        'trf5':{'f':extrair_data_trf5,'i':'arq'},
		'Geral':{'f':extrair_geral,'i':'arq'}
	}
	if tribunal in dicionario_funcoes:
		return dicionario_funcoes[tribunal]
	return dicionario_funcoes['Geral']

def insere_publicacoes(path_arquivo, collection_andamentos):
	df = pd.read_csv(path_arquivo, chunksize=100)
	for chunk in df:
		for index, row in chunk.iterrows():
			numero = str(row['numero_processo']).replace('/','').replace('-','').replace('.','')
			if len(numero) > 10:
				texto = row['texto_publicacao'].replace('\n',' ')
				dic_funcao_data = dicionario_funcoes_data(row['tribunal'])
				f_data = dic_funcao_data['f']
				input_type = dic_funcao_data['i']
				if input_type == 'texto':
					input_row = texto  
				else:
					input_row = row['nome_arquivo']
				if collection_andamentos.find_one({'_id':numero}):
					collection_andamentos.update_one({'_id':numero}, 
										{"$push":
											{'textos_publicacoes':texto,
											'nome_arquivo':row['nome_arquivo'],
											'data':f_data(input_row)
											}
										})
				else:
					collection_andamentos.insert_one({
						'_id':numero,
						'tribunal':row['tribunal'],
						'textos_publicacoes':[texto],
						'nome_arquivo':[row['nome_arquivo']],
						'data':[f_data(input_row)]
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
	if len(sys.argv) == 2:
		main(sys.argv[1], None)
	else:
		main(sys.argv[1], sys.argv[2])