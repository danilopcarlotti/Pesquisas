from common.recursive_folders import recursive_folders
import pandas as pd
import re

# VARIÁVEIS A SEREM FORNECIDAS
dic_expressoes = {
    "penal_hc": [r"habeas corpus"],
    "regime_semiaberto": [
        r"fixo.{,50}o\s*?regime\s*?semiaberto|ser\s*?cumprida\s*?no\s*?regime\s*?semiaberto"
    ],
    "regime_aberto": [
        r"fixo.{,50}o\s*?regime\s*?aberto|ser\s*?cumprida\s*?no\s*?regime\s*?aberto|alterar\s*?o\s*?regime\s*?inicial\s*?para\s*?o\s*?aberto"
    ],
    "regime_fechado": [
        r"Fixo.{,50}o regime inicial fechado|ser\s*?cumprida\s*?no\s*?regime\s*?aberto"
    ],
    "deferimento_indulto": [r"DECLARO\s*?INDULTADA.{,20}pena|[\s,]defiro.{,40}indulto"],
    "indeferimento_liminar": [
        r"Indefiro.{,30}liminar|Não\s*?havendo\s*?como\s*?ser\s*?concedida\s*?a\s*?liminar|indeferida\s*?a\s*?liminar"
    ],
    "deferimento_liminar": [r"[\s,]defiro.{,30}liminar"],
    "extinção": [r"julgo extinto"],
    "livramento_condicional": [r"[\s,]DEFIRO.{,30}livramento condicional"],
    "extinção": [r"julgo extinto"],
    "indeferimento_indulto": [r"indefiro.{,40}indulto"],
    "concessão_liberdade_provisória": [
        r"CONCEDO.{,100}liberdade provisória|[\s,]defiro.{,100}liberdade provisória"
    ],
    "não_concessão_liberdade_provisória": [r"indefiro.{,100}liberdade provisória"],
    "afastar_tráfico_privilegiado": [
        r"para\s*?afastar\s*?o\s*?tráfico\s*?privilegiado"
    ],
    "privilegiado_hediondo": [
        r"consider.{,30}tráfico\s*?privilegiado.{,30}equiparado\s*?a\s*?hediondo"
    ],
}
path = "/home/deathstar/Dados/Extração_mpsp_stj"
nome_relatorio = "/home/deathstar/Dados/Extração_mpsp_stj/relatório_booleano_tráfico_privilegiado.csv"

rec = recursive_folders()
paths = [i for i in rec.find_files(path) if i[-3:] == "csv"]
dic_processos = {}
for f in paths:
    print(f)
    try:
        df = pd.read_csv(f)
    except Exception as e:
        print(e)
        continue
    for _, row in df.iterrows():
        if row["numero_processo"] not in dic_processos:
            dic_processos[row["numero_processo"]] = {k: 0 for k in dic_expressoes}
            dic_processos[row["numero_processo"]]["tribunal"] = row["tribunal"]
        for k, v in dic_expressoes.items():
            found = True
            for exp in v:
                if not re.search(exp, row["texto_publicacao"], flags=re.S | re.I):
                    found = False
                    break
            if found:
                dic_processos[row["numero_processo"]][k] = 1
rows = []
for num, dic_vars in dic_processos.items():
    dic_aux = {"numero_processo": num}
    for var, res in dic_vars.items():
        dic_aux[var] = res
    rows.append(dic_aux)
df_new = pd.DataFrame(rows)
df_new.to_csv(nome_relatorio, index=False)
