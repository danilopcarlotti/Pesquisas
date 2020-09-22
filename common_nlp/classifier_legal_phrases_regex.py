import re
from regex_classifier_legal_phrases import palavras_interesse

def break_sentences(text, nlp):
	# return re.split(r'\w\.\s',text)
    text = re.sub(r'\s+',' ',text)
    text = re.sub(r'art\.','art ',text)
    text = re.sub(r'fls?\.','fls ',text)
    text = re.sub(r'inc\.','inc ',text)
    doc = nlp(text)
    return [sent.text for sent in doc.sents]

def dicionario_frases_tipos():
    dic_tipos_frases = {}
    for frase, tipo in palavras_interesse.items():
        if tipo not in dic_tipos_frases:
            dic_tipos_frases[tipo] = []
        dic_tipos_frases[tipo].append(r'{}'.format(frase))
    return dic_tipos_frases

dic_tipos_frases = dicionario_frases_tipos()

def classifier_legal_phrases_regex(phrase):
    for tipo, conj_exp in dic_tipos_frases.items():
        for exp in conj_exp:
            if re.search(exp, phrase, re.I):
                return tipo
    return 'argumento'