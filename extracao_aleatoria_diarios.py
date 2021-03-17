import re, pandas as pd, random, pickle, csv, sys, gc
from common.recursive_folders import recursive_folders

csv.field_size_limit(sys.maxsize)

# REGULAR_EXPRESSIONS_TRUE = [r'covid|coronav|corona v|pandemia',r'habeas\s*?corpus']
REGULAR_EXPRESSIONS_TRUE = [r"revis.{,30}contrato|revis.{,30}aluguel"]
REGULAR_EXPRESSIONS_FALSE = []
# REGULAR_EXPRESSIONS_TRUE = [r'revis.o.{1,20}contrat',r'julgo.{,30}procedente',r'taxa.{1,5}juros(.{1,50}\%?.{1,50})(contrat|pactuada|acordada)(.{1,30}\%?)|(contrat|pactuada|acordada)(.{1,50}\%?.{1,50})taxa.{1,5}juros.{,30}\%?',r'(?<!(12))\%']
# REGULAR_EXPRESSIONS_FALSE = []
# N = 500
# TEXTOS_TRIBUNAL = []
# IDS_PROCESSOS_INTERESSE = []


def pesquisa_diario(
    df_path,
    textos_interesse,
    expressions_true=REGULAR_EXPRESSIONS_TRUE,
    expressions_false=REGULAR_EXPRESSIONS_FALSE,
    column_text="texto_publicacao",
    column_id="numero_processo",
):
    df = pd.read_csv(
        df_path, chunksize=100, usecols=[column_text, column_id], engine="python"
    )
    for chunk in df:
        for _, row in chunk.iterrows():
            # if len(textos_interesse) > N:
            #     return
            aux = True
            for expression in expressions_true:
                if not re.search(expression, row[column_text], flags=re.I | re.DOTALL):
                    aux = False
                    break
            if aux:
                for expression in expressions_false:
                    if re.search(expression, row[column_text], flags=re.I | re.DOTALL):
                        aux = False
                        break
            if aux:
                textos_interesse.append(row[column_text])


def pesquisa_diario_to_csv(
    df_path,
    rows,
    expressions_true=REGULAR_EXPRESSIONS_TRUE,
    expressions_false=REGULAR_EXPRESSIONS_FALSE,
    column_text="texto_publicacao",
    column_id="numero_processo",
):
    df = pd.read_csv(
        df_path,
        chunksize=100,
        usecols=[column_text, column_id, "tribunal", "data"],
        engine="python",
    )
    for chunk in df:
        for _, row in chunk.iterrows():
            aux = True
            for expression in expressions_true:
                if not re.search(expression, row[column_text], flags=re.I | re.DOTALL):
                    aux = False
                    break
            if aux:
                for expression in expressions_false:
                    if re.search(expression, row[column_text], flags=re.I | re.DOTALL):
                        aux = False
                        break
            if aux:
                rows.append(row)


if __name__ == "__main__":
    r = recursive_folders()
    paths = [
        i
        for i in r.find_files(sys.argv[1])
        if i[-4:] == ".csv" and re.search(r"2020", i)
    ]
    # paths = random.choices(paths, k=10*N)
    rows = []
    counter = 1
    for diario in paths:
        try:
            print("Numero de textos encontrados ", len(rows))
            pesquisa_diario_to_csv(diario, rows)
        except:
            pass
        if len(rows) > 10000:
            df_new = pd.DataFrame(rows)
            df_new.to_csv(
                "{}/extracao_{}.csv".format(str(sys.argv[2]), str(counter)), index=False
            )
            counter += 1
            rows = []
        gc.collect()
    if len(rows):
        df_new = pd.DataFrame(rows)
        df_new.to_csv(
            "{}/extracao_{}.csv".format(str(sys.argv[2]), str(counter)), index=False
        )
    # IDS_PROCESSOS_INTERESSE = list(set(IDS_PROCESSOS_INTERESSE))
    # pickle.dump(IDS_PROCESSOS_INTERESSE, open('textos_interesse_diarios_%s.pickle' % (str(sys.argv[2]),),'wb'))
    # print('Foram encontrados ',len(IDS_PROCESSOS_INTERESSE),' processos de interesse')
