from common.recursive_folders import recursive_folders
import gc
import numpy as np
import pandas as pd
import sys

def main(path_files, qualificador):
    rec = recursive_folders()
    lista_arquivos = [i for i in rec.find_files(path_files) if i[-3:] == 'csv']
    d_n_diarios_ano = {}
    d_n_publicacoes_ano = {}
    for arq in lista_arquivos:
        print(arq)
        try:
            df = pd.read_csv(arq)
            if 'tribunal' not in df.columns:
                continue
            tribunal = None
            ano = None
            for _, row in df.iterrows():
                if tribunal and ano:
                    break
                if not tribunal:
                    if row['tribunal'] != np.nan:
                        tribunal = row['tribunal']
                if not ano:
                    if len(str(row['data'])) > 6:
                        ano = str(row['data'])[-4:]
            if ano and tribunal:
                if tribunal not in d_n_publicacoes_ano:
                    d_n_publicacoes_ano[tribunal] = {}
                if ano not in d_n_publicacoes_ano[tribunal]:
                    d_n_publicacoes_ano[tribunal][ano] = 0
                d_n_publicacoes_ano[tribunal][ano] += len(df.index)
                if tribunal not in d_n_diarios_ano:
                    d_n_diarios_ano[tribunal] = {}
                if ano not in d_n_diarios_ano[tribunal]:
                    d_n_diarios_ano[tribunal][ano] = 0
                d_n_diarios_ano[tribunal][ano] += 1
        except Exception as e:
            print(e)
        gc.collect()
    rows_descritivo_n_pub = []
    for tribunal, dic_a in d_n_publicacoes_ano.items():
        dic_aux = {str(ano):0 for ano in range(2008,2021)}
        dic_aux['tribunal'] = tribunal
        for ano, value in dic_a.items():
            if ano in dic_aux:
                dic_aux[ano] = value
        rows_descritivo_n_pub.append(dic_aux)
    rows_descritivo_n_diario = []
    for tribunal, dic_a in d_n_diarios_ano.items():
        dic_aux = {str(ano):0 for ano in range(2008,2021)}
        dic_aux['tribunal'] = tribunal
        for ano, value in dic_a.items():
            if ano in dic_aux:
                dic_aux[ano] = value
        rows_descritivo_n_diario.append(dic_aux)
    df_descritivo_pub = pd.DataFrame(rows_descritivo_n_pub)
    df_descritivo_pub.to_csv('descritivo_numero_publicações_ano{}.csv'.format(qualificador),index=False)
    df_descritivo_diarios = pd.DataFrame(rows_descritivo_n_diario)
    df_descritivo_diarios.to_csv('descritivo_numero_diarios_ano{}.csv'.format(qualificador),index=False)

if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2])