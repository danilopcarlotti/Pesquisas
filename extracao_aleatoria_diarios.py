import glob
import re
import pandas as pd
import random
import pickle
import csv
import sys
import gc
from recursive_folders import recursive_folders

csv.field_size_limit(sys.maxsize)

# POSSESSÓRIAS
# REGULAR_EXPRESSIONS_TRUE = [r'(reintegração|manutenção) de posse',r'imóvel',r'outros terceiros incertos|demais ocupantes|invasores|invasão|réus desconhecidos|sem.teto|sem.terra|indígenas|quilombolas']
# REGULAR_EXPRESSIONS_FALSE = [r'leasing',r'alienação fiduciária',r'arrendamento', r'rescisão',
# r'compra e venda|venda e compra',r'factoring',r'ação monitória',r'cobrança',r'espécies de contratos']

# CORONAVÍRUS
# REGULAR_EXPRESSIONS_TRUE = [r'covid|coronav|corona v|pandemia|62.{1,5}CNJ']
# REGULAR_EXPRESSIONS_FALSE = []

# TAXA DE JUROS
# REGULAR_EXPRESSIONS_TRUE = [r'revis.o.{1,20}contrat',r'julgo.{,30}procedente',r'taxa.{1,5}juros(.{1,50}\%?.{1,50})(contrat|pactuada|acordada)(.{1,30}\%?)|(contrat|pactuada|acordada)(.{1,50}\%?.{1,50})taxa.{1,5}juros.{,30}\%?',r'(?<!(12))\%']
# REGULAR_EXPRESSIONS_FALSE = []

# # INSPER TRIBUTÁRIO
# REGULAR_EXPRESSIONS_TRUE = [r'fazenda nacional|tributário']
# REGULAR_EXPRESSIONS_FALSE = []

# # # MPSP - STJ
# REGULAR_EXPRESSIONS_TRUE = [r'\:\s*?minist.rio\s*?p.blico\s*?do\s*?estado\s*?de\s*?s.o\s*?paulo',r'penal|criminal|crime']
# REGULAR_EXPRESSIONS_FALSE = []

# # MPSP - TJSP
# REGULAR_EXPRESSIONS_TRUE = [r'tr.fico\s*?privilegiado',r'pena|criminal|crime']
# REGULAR_EXPRESSIONS_FALSE = []

# MPSP - TJSP
# REGULAR_EXPRESSIONS_TRUE = [r'integrar|cadastro|cadastrado',r'primeiro comando da capital|facção',r'288.{,3}CP|288.{,3}Código|art.{,5}lei do crime organizado',r'criminal|penal|crime',r'condenação|condenado|condeno']
# REGULAR_EXPRESSIONS_FALSE = []

# # AGÊNCIAS REGULADORAS - FURQUIM
# REGULAR_EXPRESSIONS_TRUE = [r'ANEEL|anatel|[\s\.,]anp[\s\.,]|anvisa|[\s\.,]ans[\s\.,]|agência nacional das águas|[\s\.,]antt[\s\.,]|[\s\.,]anac[\s\.,]']
# REGULAR_EXPRESSIONS_FALSE = []

# # # AITH - FURQUIM
# REGULAR_EXPRESSIONS_TRUE = [r'pet.{,5}ct|cintilografia|pet.{,5}scan|radiof.rmaco|iodoterapia']
# REGULAR_EXPRESSIONS_FALSE = []

# # TRIBUTÁRIO
# REGULAR_EXPRESSIONS_TRUE = [r'tributo|tributário']
# REGULAR_EXPRESSIONS_FALSE = []

# COMPENSAÇÃO CRUZADA
REGULAR_EXPRESSIONS_TRUE = [
    r"11\.*457\/[20]*07|13\.*670\/[20]*18|compensação cruzada|apuração anterior.{,20}(utilização|adesão).{,20}e\-*social"
]
REGULAR_EXPRESSIONS_FALSE = []

# REGULAR_EXPRESSIONS_TRUE = [r'saneamento b.sico']
# REGULAR_EXPRESSIONS_FALSE = []
# N = 500
# TEXTOS_TRIBUNAL = []
# IDS_PROCESSOS_INTERESSE = []

# # CORONAVÍRUS E ALUGUEL
# REGULAR_EXPRESSIONS_TRUE = [r'covid|coronav|corona v|pandemia', r'revis.{,10}aluguel']
# REGULAR_EXPRESSIONS_FALSE = []


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
                # textos_interesse.append(row[column_id])


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
    df = None


if __name__ == "__main__":
    # r = recursive_folders()
    # paths = [i for i in r.find_files(sys.argv[1]) if i[-4:] == '.csv']
    paths = glob.glob(sys.argv[1] + "/**/*.csv", recursive=True)
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
