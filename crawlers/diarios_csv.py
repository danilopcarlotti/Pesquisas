from diarios_separacao import dicionario_separacao_diarios, encontra_publicacoes, encontra_numero
import re, pandas as pd, subprocess, sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))
from pesquisas.common.recursive_folders import recursive_folders
from pesquisas.common.parallel_programming import parallel_programming

def month_to_number(month):
    month = month.lower().strip()
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

def extrair_data_texto_arq(arq):
    data_raw = re.search(r'(\d{1,2}) de (\w*?) de (\d{4})', arq, re.DOTALL)
    if data_raw:
        day = data_raw.group(1)
        month = month_to_number(data_raw.group(2))
        year = data_raw.group(3)
        return day+'/'+month+'/'+year
    else:
        return ' '

def extrair_data_ac(path_arquivo):
    data = re.search(r'dir_00\d/DE(\d*?)\.', path_arquivo)
    if data:
        data_encontrada = data.group(1)
        if len(data_encontrada) == 6:
            return data_encontrada[:2]+'/'+data_encontrada[2:4]+'/20'+data_encontrada[4:]
        elif len(data_encontrada) == 8:
            return data_encontrada[6:]+'/'+data_encontrada[4:6]+'/'+data_encontrada[:4]
    else:
        data_encontrada = ' '
    return data_encontrada

def extrair_data_al(path_arquivo):
    data = re.search(r'Diarios_al/(\d{8})/', path_arquivo)
    if data:
        data_encontrada = data.group(1)
        return data_encontrada[:2]+'/'+data_encontrada[2:4]+'/'+data_encontrada[4:]
    return ' '

def extrair_data_am(path_arquivo):
    data = re.search(r'Diarios_am/(.*?)/', path_arquivo)
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
            return ' '
    else:
        return ' '

def extrair_data_ba(arq):
    return extrair_data_texto_arq(arq[:500])

def extrair_data_ce(path_arquivo):
    data = re.search(r'Diarios_ce/(\d{8})/', path_arquivo)
    if data:
        data_encontrada = data.group(1)
        return data_encontrada[:2]+'/'+data_encontrada[2:4]+'/'+data_encontrada[4:]
    return ' '

def extrair_data_df(arq):
    return extrair_data_texto_arq(arq[:3000])

def extrair_data_go(arq):
    return extrair_data_texto_arq(arq[:3000])

def extrair_data_ms(path_arquivo):
    data = re.search(r'Diarios_ms/(\d{8})/', path_arquivo)
    if data:
        data_encontrada = data.group(1)
        return data_encontrada[:2]+'/'+data_encontrada[2:4]+'/'+data_encontrada[4:]
    return ' '

def extrair_data_mt(arq):
    data_raw = re.search(r'(\d{1,2}) de (.*?) de (\d{4})', arq[:30000], flags=re.DOTALL|re.I)
    if data_raw:
        day = data_raw.group(1)
        if len(day) == 1:
            day = '0'+day
        month = month_to_number(data_raw.group(2))
        year = data_raw.group(3)
        return day+'/'+month+'/'+year
    else:
        return ' '

def extrair_data_pa(arq):
    return extrair_data_texto_arq(arq[:3000])

def extrair_data_pb(arq):
    return extrair_data_texto_arq(arq[:3000])

def extrair_data_pe(arq):
    data_raw = re.search(r'Publicação: (\d{2}/\d{2}/\d{4})', arq)
    if data_raw:
        return data_raw.group(1)
    else:
        return ' '

def extrair_data_pi(path_arquivo):
    data = re.search(r'Diarios_pi/(\d{8})/', path_arquivo)
    if data:
        data_encontrada = data.group(1)
        return data_encontrada[:2]+'/'+data_encontrada[2:4]+'/'+data_encontrada[4:]
    return ' '

def extrair_data_pr(arq):
    return extrair_data_texto_arq(arq[:3000])

def extrair_data_rn(path_arquivo):
    data = re.search(r'Diarios_rn/(.*?)\.', path_arquivo)
    if data:
        data = data.group(1)
        return data[6:]+'/'+data[4:6]+'/'+data[:4]
    else:
        return ' '

def extrair_data_ro(arq):
    return extrair_data_texto_arq(arq[:300])

def extrair_data_rr(path_arquivo):
    data = re.search(r'Diarios_rr/(\d{8})/', path_arquivo)
    if data:
        data_encontrada = data.group(1)
        return data_encontrada[6:]+'/'+data_encontrada[4:6]+'/'+data_encontrada[:4]
    return ' '

def extrair_data_rs(arq):
    return extrair_data_texto_arq(arq[:3000])

def extrair_data_sc(arq):
    return extrair_data_texto_arq(arq[:3000])

def extrair_data_se(arq):
    return extrair_data_texto_arq(arq[:3000])

def extrair_data_sp(path_arquivo):
    data = re.search(r'Diarios_sp/(.*?)/', path_arquivo)
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
                return '0'+data[0]+'/0'+data[1:3]+'/'+data[3:]
        else:
            return ' '
    else:
        return ' '

def extrair_data_stj(path_arquivo):
    data = re.search(r'stj_dje_(.*?)_', path_arquivo)
    if data:
        data = data.group(1)
        return data[6:]+'/'+data[4:6]+'/'+data[:4]
    else:
        return ' '

def extrair_data_to(arq):
    data_raw = re.search(r'(\d{2}) de (.*?) de (\d{4})', arq[:3000], flags=re.DOTALL|re.IGNORECASE)
    if data_raw:
        day = data_raw.group(1)
        month = month_to_number(data_raw.group(2))
        year = data_raw.group(3)
        return day+'/'+month+'/'+year
    else:
        return ' '

def extrair_data_trf1(path_arquivo):
    # return extrair_data_texto_arq(arq[:3000])
    data = re.search(r'Diarios_trf1/dir_\d+/.*?(\d{4}\-\d{2}\-\d{2})', path_arquivo)
    if data:
       data = data.group(1).replace('-','')
       return data[-2:]+'/'+data[-4:-2]+'/'+data[:4]
    else:
       return extrair_data_texto_arq('\n'.join([i for i in open(path_arquivo,'r')]))

def extrair_data_trf3(arq):
    data_raw = re.search(r'Edição n.*?((\d{2}) de (.*?) de (\d{4}))', arq, re.DOTALL)
    if data_raw:
        day = data_raw.group(2)
        month = month_to_number(data_raw.group(3))
        year = data_raw.group(4)
        return day+'/'+month+'/'+year
    else:
        return ' '

def extrair_data_trf4(path_arquivo):
    data = re.search(r'Diarios_trf4/(\d{8})', path_arquivo)
    if data:
        data = data.group(1)
        return data[:2]+'/'+data[2:4]+'/'+data[4:]
    else:
        return ' '
    return ' '

def extrair_data_trf5(arq):
    data_raw = re.search(r'(\d{2}) de (.*?) de (\d{4})', arq[:300], re.DOTALL)
    if not data_raw:
        data_raw = re.search(r'(\d{1,2}) (\w{1,10}) (\d{4})', arq[:3000], re.DOTALL)
    if data_raw:
        day = data_raw.group(1)
        month = month_to_number(data_raw.group(2))
        year = data_raw.group(3)
        return day+'/'+month+'/'+year
    else:
        return ' '

def extrair_geral(arq):
	return ' '

def dicionario_funcoes_data(tribunal):
	dicionario_funcoes = {
		'ac':{'f':extrair_data_ac,'i':'path_arquivo'},
        'am':{'f':extrair_data_am,'i':'path_arquivo'},
        'al':{'f':extrair_data_al,'i':'path_arquivo'},
        'ba':{'f':extrair_data_ba,'i':'arq'},
        'ce':{'f':extrair_data_ce,'i':'path_arquivo'},
        'df':{'f':extrair_data_df,'i':'arq'},
        'go':{'f':extrair_data_go,'i':'arq'},
        'ms':{'f':extrair_data_ms,'i':'path_arquivo'},
        'mt':{'f':extrair_data_mt,'i':'arq'},
        'pa':{'f':extrair_data_pa,'i':'arq'},
        'pb':{'f':extrair_data_pb,'i':'arq'},
        'pe':{'f':extrair_data_pe,'i':'arq'},
        'pi':{'f':extrair_data_pi,'i':'path_arquivo'},
        'pr':{'f':extrair_data_pr,'i':'arq'},
        'rn':{'f':extrair_data_rn,'i':'path_arquivo'},
        'ro':{'f':extrair_data_ro,'i':'arq'},
        'rr':{'f':extrair_data_rr,'i':'path_arquivo'},
        'rs':{'f':extrair_data_rs,'i':'arq'},
        'sc':{'f':extrair_data_sc,'i':'arq'},
        'se':{'f':extrair_data_se,'i':'arq'},
        'sp':{'f':extrair_data_sp,'i':'path_arquivo'},
        'stj':{'f':extrair_data_stj,'i':'path_arquivo'},
        'to':{'f':extrair_data_to,'i':'arq'},
        'trf1':{'f':extrair_data_trf1,'i':'path_arquivo'},
        'trf3':{'f':extrair_data_trf3,'i':'arq'},
        'trf4':{'f':extrair_data_trf4,'i':'path_arquivo'},
        'trf5':{'f':extrair_data_trf5,'i':'arq'},
		'Geral':{'f':extrair_data_texto_arq,'i':'arq'}
	}
	if tribunal in dicionario_funcoes:
		return dicionario_funcoes[tribunal]
	return dicionario_funcoes['Geral']

def create_csv(filepath):
	rows = []
	partes_nome = filepath.split('/')
	tribunal = ''
	for p in partes_nome:
		if re.search(r'Diarios_',p):
			tribunal = p.split('_')[1]
			break
	if tribunal in dicionario_separacao_diarios:
		dic_funcao_data = dicionario_funcoes_data(tribunal)
		f_data = dic_funcao_data['f']
		input_type = dic_funcao_data['i']
		texto = '\n'.join([i for i in open(filepath,'r')])
		if input_type == 'arq':
			input_data = texto[:10000]
		else:
			input_data = filepath
		data = f_data(input_data)
		publicacoes = encontra_publicacoes(tribunal, texto)
		for pub in publicacoes:
			if pub:
				pub = ''.join(pub)
				numero = encontra_numero(tribunal, pub).replace('\n','').replace(' ','')
				rows.append({'tribunal':tribunal,'texto_publicacao':pub.replace('\n',' '),'nome_arquivo':filepath,'data':data,'numero_processo':numero})
		index = [j for j in range(len(rows))]
		df = pd.DataFrame(rows, index=index)
		df.to_csv(filepath.replace('.txt','.csv'),index=False)
		# subprocess.Popen('mv "%s.csv" "%s"' % (nome_arquivo[:-4],filepath.replace(nome_arquivo,'')), shell=True)

def main(path_diarios):
    rec_f = recursive_folders()
    arquivos_path = rec_f.find_files(path_diarios)
    diarios_processar = [i for i in arquivos_path if i[-4:] == '.txt']
    # parallel = parallel_programming()
    # parallel.run_f_nbatches(create_csv,diarios_processar)
    for diario in diarios_processar:
        print(diario)
        create_csv(diario)

def main_datas(path_diarios):
    rec = recursive_folders()
    diarios_processar = [i for i in rec.find_files(path_diarios) if i[-4:] == '.txt']
    dicionario_datas_ano = {}
    for path_arquivo in diarios_processar:
        tribunal = re.search(r'/Diarios_(.*?)/',path_arquivo)
        if tribunal:
            tribunal = tribunal.group(1)
            dic_funcao_data = dicionario_funcoes_data(tribunal)
            f_data = dic_funcao_data['f']
            input_type = dic_funcao_data['i']
            if input_type == 'path_arquivo':
                input_f = path_arquivo  
            else:
                input_f = ' '.join([line for line in open(path_arquivo.replace('csv','txt'),'r')])
            try:
                if tribunal not in dicionario_datas_ano:
                    dicionario_datas_ano[tribunal] = {i:0 for i in range(2008,2020)}
                data_encontrada = f_data(input_f)
                if data_encontrada != ' ':
                    ano = int(data_encontrada[-4:])
                    if ano in dicionario_datas_ano[tribunal]:
                        dicionario_datas_ano[tribunal][ano] += 1
            except Exception as e:
                print(path_arquivo)
                print(e)
    rows = []
    for k,v in dicionario_datas_ano.items():
        dic_aux = v.copy()
        dic_aux['ano'] = k
        rows.append(dic_aux)
    df_datas = pd.DataFrame(rows,index=[i for i in range(len(rows))])
    df_datas.to_excel('contagem_diarios_anos_geral.xlsx',index=False)

if __name__ == '__main__':
	path_diarios = sys.argv[1]
	main(path_diarios)
    # main_datas('/home/deathstar/Documents/Diarios')
    # main('/home/deathstar/Dados/Diarios/Diarios_ba')