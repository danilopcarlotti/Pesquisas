from common.recursive_folders import recursive_folders
import gc
import numpy as np
import pandas as pd
import pickle
import sys

def consertar_ncnj(nCnj):
    if len(nCnj) == 20:
        return nCnj
    elif len(nCnj) < 20:
        return consertar_ncnj('0'+nCnj)
    else:
        return consertar_ncnj(nCnj[:-1])

def criar_dic_acoes(path_numeros_csv, path_final=''):
    dicionario_acoes = {}
    df = pd.read_csv(path_numeros_csv,chunksize=100)
    for chunk in df:
        for _, row in chunk.iterrows():
            num_processo = consertar_ncnj(str(row['numero_processo']).replace('.','').replace('/','').replace('-',''))
            if num_processo not in dicionario_acoes:
                dicionario_acoes[num_processo] = 0
    pickle.dump(dicionario_acoes,open(path_final+'dicionario_acoes.pickle','wb'))

def extracao_decisoes_cnj_csvs(lista_arquivos, path_final=''):
    dicionario_acoes = pickle.load(open(path_final+'dicionario_acoes.pickle','rb'))
    decisoes_interesse = []
    counter = 0
    for arq in lista_arquivos:
        print('faltam {} arquivos'.format(len(lista_arquivos) - counter))
        try:
            try:
                df = pd.read_csv(arq,usecols=['numero_processo','tribunal','texto_publicacao'])
            except:
                df = pd.read_csv(arq,sep=';',usecols=['numero_processo','tribunal','texto_publicacao'])
            for _, row in df.iterrows():
                n_processo = consertar_ncnj(str(row['numero_processo']).replace('.','').replace('-',''))
                if n_processo in dicionario_acoes:
                    decisoes_interesse.append({'numero_processo':n_processo,'tribunal':row['tribunal'],'texto_publicacao':row['texto_publicacao']})
            if len(decisoes_interesse) > 200000:
                df_new = pd.DataFrame(decisoes_interesse,index=[i for i in range(len(decisoes_interesse))])
                df_new.to_csv(path_final+'extração_ações_cnj_encontradas_texto_%s.csv' % (str(counter,)),index=False)
                decisoes_interesse = []
        except Exception as e:
            print(e)
        counter += 1
        gc.collect()
    if len(decisoes_interesse):
        df_new = pd.DataFrame(decisoes_interesse,index=[i for i in range(len(decisoes_interesse))])
        df_new.to_csv(path_final+'extração_ações_cnj_encontradas_texto_%s.csv' % (str(counter,)),index=False)

def main():
    print('Criando dicionário de ações')
    criar_dic_acoes('/home/deathstar/Dados/Extracao_cnj_adocao/numeros_processos.csv',path_final='/home/deathstar/Dados/Extracao_cnj_adocao/')
    rec = recursive_folders()
    lista_arquivos = [i for i in rec.find_files('/home/deathstar/Dados/Diarios') if i[-3:] == 'csv']
    print('Extraindo decisões')
    extracao_decisoes_cnj_csvs(lista_arquivos,path_final='/home/deathstar/Dados/Extracao_cnj_adocao/')
    
    # criar_dic_acoes(sys.argv[1],path_final=sys.argv[2])
    # rec = recursive_folders()
    # lista_arquivos = [i for i in rec.find_files(sys.argv[1]) if i[-3:] == 'csv']
    # extracao_decisoes_cnj_csvs(lista_arquivos)

if __name__ == "__main__":
    main()