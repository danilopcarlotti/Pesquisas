import re
from regex_classifier_legal_phrases import palavras_interesse

def dicionario_frases_tipos():
    dic_tipos_frases = {}
    for frase, tipo in palavras_interesse.items():
        if tipo not in dic_tipos_frases:
            dic_tipos_frases[tipo] = []
        dic_tipos_frases[tipo].append(r'{}'.format(frase))
    return dic_tipos_frases

def classifier_legal_phrases_regex(phrase):
    dic_tipos_frases = dicionario_frases_tipos()
    for tipo, conj_exp in dic_tipos_frases.items():
        for exp in conj_exp:
            if re.search(exp, phrase, re.I):
                return tipo