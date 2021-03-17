import re, os, sys, time

sys.path.append(os.path.dirname(os.getcwd()))
from common_nlp.parse_texto import busca

re_final_ac = [
    r"(\n\n\s*?)(Acórdão n)",
    r"(\n\n\s*?)(\d+\. Classe)",
    r"(\n\n\s*?)(Classe)",
    r"(\n\n\s*?)(\d+\. CLASSE)",
    r"(\n\n\s*?)(CLASSE)",
    r"(\n\n\s*?\d+ - )(\d{7})",
    r"(\n\n\s*?)(ADV\:)",
    r"(\n\n\s*?)(Processo)",
    r"(\n\n\s*?)(Autos n)",
]
re_final_am = [
    r"(\n\n.{0,15})(PROCESSO DIGITAL\:)",
    r"(\n\n\s*?)(.{0,15}De ordem d[oa])",
    r"(\n\n\s*?)(.{0,15}Despacho proferido pel)",
    r"(\n\n\s*?)(.{0,15}Apelação n)",
    r"(\n\n\s*?)(.{0,15}Processo n\.)",
    r"(\n\n\s*?)(.{0,15}Processo\s*?\:)",
    r"(\n\n\s*?)(.{0,15}PROCESSO\:)",
    r"(\n\n\s*?)(.{0,15}Autos n)",
    r"(\n\n\s*?)(.{0,15}ADV\:)",
    r"(\n\n\s*?)(.{0,15}Apelação)",
    r"(\n\n\s*?)(.{0,15}Agravo)",
    r"(\n\n\s*?)(.{0,15}Recurso)",
]
re_final_ce = [
    r"(\n\n\s*?)(PROCESSO)",
    r"(\n\n\s*?)(\s*?Processo)",
    r"(\n\n\s*?)(DECISÃO MONOCRÁTICA)",
    r"(\n\n\s*?)(\d{1,5}\))",
    r"(\n\n\s*?)(\s*D\s*ISTR\s*IBU\s*IÇÃO)",
    r"(\n\n\s*?)(\s° \d{4,})",
    r"(\n\n\s*?)(ADV\:)",
    r"(\n\n\s*?)(\s*?\d{4,8}\-\d\d\.\d{4}\.\d\.\d\d\.\d{4})",
    r"(\n\n\s*?)(\d+\s*?\d{4,8}\-\d\d\.\d{4}\.\d\.\d\d\.\d{4})",
]
re_final_ma = [
    r"(\n\n\s*?)(REQUERIMENTO DE )",
    r"(\n\n\s*?)(PETIÇÃO N)",
    r"(\n\n\s*?)(HABEAS CORPUS N)",
    r"(\n\n\s*?)(PORTARIA\-TJ)",
    r"(\n\n\s*?)(\d{1,3}\-PROCESSO)",
    r"(\n\n\s*?)(ACÓRDÃO N)",
    r"(\n\n\s*?)(Processo)",
]
re_final_ms = [
    r"(\n\ns*?)(JUÍZO DE DIREITO DA)",
    r"(\n\ns*?)(Agravo de Instrumento)",
    r"(\n\ns*?)(Apelação)",
    r"(\n\ns*?)(Habeas Corpus)",
    r"(\n\ns*?)(Comarca de)",
    r"(\n\ns*?)(Revisão Criminal)",
    r"(\n\ns*?)(Mandado de Segurança)",
    r"(\n\ns*?)(Recurso Em Sentido Estrito)",
    r"(\n\ns*?)(Embargos)",
    r"(\n\ns*?)(Exceção)",
    r"(\n\ns*?)(Reexame)",
]
re_final_pa = [r"(\n\n\s*?)(PROCESSO\:)", r"(\n\n\s*?)(Processo\:)"]
re_final_pb = [
    r"(\n\n\s*?)(APELAÇÃO)",
    r"(\n\n\s*?)(MANDADO)",
    r"(\n\n\s*?)(HABEAS)",
    r"(\n\n\s*?)(EMBARGOS)",
    r"(\n\n\s*?)(AGRAVO)",
    r"(\n\n\s*?)(CONFLITO NEGATIVO)",
    r"(\n\n\s*?)(RECURSO)",
    r"(\n\n\s*?)(REEXAME)",
    r"(\n\n\s*?)(RELATOR\(A\)\:)",
    r"(\n\n\s*?)(COMARCA)",
    r"(\n\n\s*?)(Processo)",
    r"(\n\n\s*?)(\d+\s*?Processo)",
    r"(\n\n\s*?)(Agravo de Instrumento)",
]
re_final_pi = [
    r"(\n\n\s*?)(PROCESSOS [Nn])",
    r"(\n\n\s*?)(HABEAS CORPUS [Nn])",
    r"(\n\n\s*?)(AGRAVO DE INSTRUMENTO [Nn])",
    r"(\n\n\s*?)(REEXAME NECESSÁRIO [Nn])",
    r"(\n\n\s*?)(APELAÇÃO)",
    r"(\n\n\s*?)(MANDADO DE SEGURANÇA [Nn])",
    r"(\n\n\s*?)(DESPACHO)",
    r"(\n\n\s*?)(EDITAL)",
    r"(\n\n\s*?)(AVISO)",
    r"(\n\n\s*?)(ATO ORDINATÓRIO)",
    r"(\n\n\s*?)(SENTENÇA)",
    r"(\n\n\s*?)(Processos [Nn])",
    r"(\n\n\s*?)(Habeas Corpus [Nn])",
    r"(\n\n\s*?)(Agravo De Instrumento [Nn])",
    r"(\n\n\s*?)(Reexame Necessário [Nn])",
    r"(\n\n\s*?)(Apelação)",
    r"(\n\n\s*?)(Mandado de Segurança [Nn])",
    r"(\n\n\s*?)(Despacho)",
    r"(\n\n\s*?)(Edital)",
    r"(\n\n\s*?)(Aviso)",
    r"(\n\n\s*?)(Ato Ordinatório)",
    r"(\n\n\s*?)(Sentença)",
    r"(\n\n\s*?)(Ref\. Processo)",
    r"(\n\n\s*?)(PROCESSO [Nn])",
    r"(\n\n\s*?)(\d*\-*\s*?Processo [Nn])",
    r"(\n\n\s*?)(\d+\.\s\d{4})",
]
re_final_rn = [
    r"(\n\n\s*?)(APELAÇÃO)",
    r"(\n\n\s*?)(EMBARGOS DE)",
    r"(\n\n\s*?)(AGRAVO)",
    r"(\n\n\s*?)(CONFLITO NEGATIVO)",
    r"(\n\n\s*?)(MANDADO DE SEGUR)",
    r"(\n\n\s*?)(EXECUÇÃO)",
    r"(\n\n\d*\s*?\-*\s*?)(Embargos de)",
    r"(\n\n\d*\s*?\-*\s*?)(Agravo Interno)",
    r"(\n\n\d*\s*?\-*\s*?)(Mandado de Segurança)",
    r"(\n\n\d*\s*?\-*\s*?)(Apelação)",
    r"(\n\n\d*\s*?\-*\s*?)(Execução)",
    r"(\n\n\d*\s*?\-*\s*?)(Ação Rescisória)",
    r"(\n\n\s*?)(ADV\:)",
    r"(\n\d*\s*?\-*\s*?)(Agravo de Instrumento)",
]
re_final_ro = [
    r"(\n\n\s*?)(Origem\:)",
    r"(\n\n\s*?)(Mandado de Segurança)",
    r"(\n\n\s*?)(Número do Processo)",
    r"(\n\n\s*?)(Processo n)",
    r"(\n\n\s*?)(Proc\.\:)",
    r"(\n\n\s*?)(Processo\:)",
]
re_final_sc = [
    r"(\n\n\s*?)(ADV\s*?\:)",
    r"(\n\n\s*?)(Processo)",
    r"(\n\n\s*?)(\d*\s*\.*Recurso)",
    r"(\n\n\s*?)(\d*\s*\.*Ag\s*ra\s*vo)",
    r"(\n\n\s*?)(\d*\s*\.*Embargo)",
    r"(\n\n\s*?)(\d*\s*\.*Apelação)",
    r"(\n\n\s*?)(N\.)",
    r"(\n\n\s*?)(\d+\s*?\-\s*?N\.)",
]
re_final_sp = [
    r"(\n\n\s*?)(Processo)",
    r"(\n\n\s*?)(PROCESSO\:)",
    r"(\n\n\s*?)(N\.*[º°](?! ORDEM))",
    r"(\n\n\s*?)(\d{3}\s*[\-\.]\s*\d{2})",
    r"(\n\n\s*?)(\d{4,8}\s*[\-\.\W]\s*\d{2})",
]
re_final_stf = [
    r"\n\n\s*?HABEAS CORPUS",
    r"(\n\n\s*?)(\d+)",
    r"(\n\n\s*?)(AGRAVO DE INSTRUMENTO)",
    r"(\n\n\s*?)(MANDADO DE SEGURANÇA)",
    r"(\n\n\s*?)(RECLAMAÇÃO)",
    r"(\n\n\s*?)(RECURSO EXTRAORDINÁRIO)",
    r"(\n\n\s*?)(AG\.REG\.)",
    r"(\n\n\s*?)(EMB\.DECL\.)",
    r"(\n\n\s*?)(RECURSO EXTRAORDINÁRIO)",
    r"(\n\n\s*?)(AÇÃO DIRETA DE INCONSTITUCIONALIDADE)",
    r"(\n\n\s*?)(AÇÃO ORIGINÁRIA)",
    r"(\n\n\s*?)(AÇÃO PENAL)",
    r"(\n\n\s*?)(MEDIDA CAUTELAR NA RECLAMAÇÃO)",
    r"(\n\n\s*?)(CUMPRIMENTO DE SENTENÇA NA AÇÃO)",
    r"(\n\n\s*?)()",
    r"(\n\n\s*?)(EXECUÇÃO CONTRA A FAZENDA)",
    r"(\n\n\s*?)(nEXTRADIÇÃO)",
    r"(\n\n\s*?)(RECURSO ORDINÁRIO)",
    r"(\n\n\s*?)(SEGUNDO AG\.REG\.)",
]
re_final_to = [
    r"(\n\n\s*?)(Autos n)",
    r"(\n\n\s*?)(AUTOS N)",
    r"(\n\n\s*?)(Processo N)",
    r"(\n\n\s*?)(EDITAL DE CITAÇÃO)",
    r"(\n\n\s*?)(EDITAL DE INTIMAÇÃO)",
    r"(\n\n\s*?)(PROCESSO N)",
    r"(\n\n\s*?)(PROTOCOLO)",
    r"(\n\n\s*?)(\d{1,4}\s*?\-\s*?Recurso)",
    r"(\n\n\s*?)(ORIGEM\:)",
]
re_final_trf1 = [
    r"(\n\n\s*?)(Processo Orig)",
    r"(\n\n\s*?)(Tribunal\s*?Regional\s*?Federal\s*?da\s*?1ª\s*?Região)",
    r"(\n\n\s*?)(PODER JUDICI.RIO)",
    r"(\n\n\s*?)(Numera..o .nica)",
    r"(\n\n\s*?)(\d{4,8})",
    r"(\n\n\s*?)(Ap\s)",
    r"(\n\n\s*?)(APELAÇÃO\s*?C.VEL)",
    r"(\n\n\s*?)(AGRAVO\s*?DE\s*?INSTRUMENTO)",
    r"(\n\n\s*?)(N\.)",
    r"(\n\n\s*?)(REEXAME\s*?NECESSÁRIO\s*?N\.)",
    r"(\n\n\s*?)(APELAÇÃO\/REEXAME\s*?NECESSÁRIO)",
    r"(\n\n\s*?)(Relator\s*?AGRAVO\s*?DE\s*?INSTRUMENTO)",
]
re_final_trf3 = [
    r"(\n\n\s*?)(\d{4,8})",
    r"(\n\n\s*?)(PROCESSO)",
    r"(\n\n\s*?)(PROC\.)",
    r"(\n\n\s*?)(Processo n)",
    r"(\n\n\s*?)(AGRAVO)",
    r"(\n\n\s*?)(EMBARGOS)",
    r"(\n\n\s*?)(MANDADO)",
    r"(\n\n\s*?)(EXECUÇÃO)",
    r"(\n\n\s*?)(PROCEDIMENTO)",
    r"(\n\n\s*?)(AÇÃO)",
    r"(\n\n\s*?)(REMESSA)",
    r"(\n\n\s*?)(APELAÇÃO\s*?CÍVEL)",
    r"(\n\n\s*?)(APELAÇÃO)",
    r"(\n\n\s*?)(APELAÇÃO\s*?REEXAME)",
    r"(\n\n\s*?)(EDITAL)",
    r"(\n\n\s*?)(São Paulo, \d+ de \w+ de \d+\.\s*?)",
]
re_final_trf4 = [
    r"(\n\n\s*?)(AGRAVO)",
    r"(\n\n\s*?)(MANDADO)",
    r"(\n\n\s*?)(EXECUÇÃO)",
    r"(\n\n\s*?)(PROCEDIMENTO)",
    r"(\n\n\s*?)(AÇÃO)",
    r"(\n\n\s*?)(REMESSA)",
    r"(\n\n\s*?)(APELAÇÃO)",
    r"(\n\n\s*?)(EDITAL)",
    r"(\n\n\s*?)(\d{7})",
]
re_final_trf5 = [
    r"(\n\n\s*?)(AC \-)",
    r"(\n\n\s*?)(AGTR)",
    r"(\n\n\s*?)(REOAC)",
    r"(\n\n\s*?)(APELREEX)",
    r"(\n\n\s*?)()",
    r"(\n\n\s*?)(AGIVP)",
    r"(\n\n\s*?)(PROTOCOLO)",
    r"(\n\n\s*?)(\d{4}\s*?\.\s*Processo)",
]
re_num_cnj = (
    r"\d{4,8}\s*\-*\.*\s*\d{2}\s*\.*\s*\d{4}\s*\.*\s*\d{1}\s*\.*\s*\d{2}\s*\.*\s*\d{4}"
)
re_num_stf_stj = r"\d.*?( -)"
re_num_trf_trt = r"\d{4}\.\d{2}\.\d{2}\.\d{6}\-\d|\d{7}\s*?-\d{2}\s*?\.\d{4}\s*?\.\d{1}\s*?\.\d{2}\s*?\.\d{4}|\d{7}\s*?-\d{2}\s*?\.\d{4}\s*?\.\d{3}\s*?\.\d{4}|\d{15}|\d{3,5}\-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}"

dicionario_separacao_diarios = {
    "ac": [re_final_ac, re_num_cnj, 0,],
    "al": [[r"(\n\n\s*?)(ADV\s*?\:)", r"(\n\n\s*?)(Macei.*?\n)"], re_num_cnj, 0],
    "am": [re_final_am, re_num_cnj, 0,],
    "ap": [
        [
            r"(\n\n\s*?)(DISTRIBUIÇÃO)",
            r"(\n\n\s*?)(N. do processo\:)",
            r"(\n\n\s*?)(VARA\:)",
        ],
        re_num_cnj,
        0,
    ],
    "ba": [
        [
            r"(\n\n\s*?)(DIREITO )",
            r"(\n\n\s*?)(Intimação)",
            r"(\n\n\s*?)(INTIMAÇÃO)",
            r"(\n\n\s*?)(DESPACHO)",
            r"(\n\n\s*?)(DECISÃO)",
            r"(\n\n\s*?)(ADV\:)",
        ],
        re_num_cnj,
        0,
    ],
    "ce": [
        re_final_ce,
        r"\d{4,8}\s*-\s*\d{2}\s*\.\s*\d{4}\s*\.\s*\d{1}\s*\.\s*\d{2}\s*\.\s*\d{4}",
        0,
    ],
    "df": [
        [
            r"(\n\n\s*?)(\d{1,4}\.)",
            r"(\n\n\s*?)(Num Processo)",
            r"(\n\n\s*?)(N. )",
            r"(\n\n\s*?)(Distribuição)",
        ],
        r"\d{4,8}\s*-?\.?\s*\d{2}\s*\.?\s*\d{4}\s*\.?\s*\d{1}\s*\.?\s*\d{2}\s*\.?\s*\d{4}|\d{4}\.*\s*\d{2}\.*\s*\d\.*\s*\d{6}\-*\s*\d",
        0,
    ],
    "go": [
        [
            r"(\n\n\s*?)(PROTOCOLO)",
            r"(\n\n\s*?)(NR\.)",
            r"(\n\n\s*?)(PROCESSO)",
            r"(\n\n\s*?)(\d+\s*?\-\s*?Processo n)",
            r"(\n\n\s*?)(Proc\.)",
        ],
        re_num_cnj,
        0,
    ],
    "ma": [re_final_ma, re_num_cnj, 0,],
    "mg": [[r"(\n\n\s*?)(\d{5} - )"], re_num_cnj, 0],
    "ms": [re_final_ms, re_num_cnj, 0,],
    "mt": [
        [
            r"(\n\n\s*?)(Protocolo)",
            r"(\n\n\s*?)(Intimação)",
            r"(\n\n\s*?)(Cod\.\s*?Proc\.)",
            r"(\n\n\s*?)(Processo)",
        ],
        r"\d{4,8}\s*-*\.*\s*\d{2}\s*\.\s*\d{4}\s*\.\s*\d{1}\s*\.\s*\d{2}\s*\.\s*\d{4}|\d{4,8}\s*-*\.*\s*\d{2}\s*\.\s*\d{4}\s*\.\s*\d{1,3}\s*\.\s*\d{2,4}",
        0,
    ],
    "pa": [re_final_pa, re_num_cnj, 0,],
    "pb": [
        re_final_pb,
        r"\d{4,8}\s*-*\.*\s*\d{2}\s*\.\s*\d{4}\s*\.\s*\d{1}\s*\.\s*\d{2}\s*\.\s*\d{4}|\d{4,8}\s*-*\.*\s*\d{2}\s*\.\s*\d{4}\s*\.\s*\d{1,3}\s*\.\s*\d{2,4}|\d{17}",
        0,
    ],
    "pe": [[r"(\n\n\s*?)(Protocolo)|(\n\n\s*?)(Processo N)"], re_num_cnj, 0],
    "pi": [
        re_final_pi,
        r"\d{4,8}\s*-*\.*\s*\d{2}\s*\.\s*\d{4}\s*\.\s*\d{1}\s*\.\s*\d{2}\s*\.\s*\d{4}|\d{4,8}\s*-*\.*\s*\d{2}\s*\.\s*\d{4}\s*\.\s*\d{1,3}\s*\.\s*\d{2,4}|\d{4}\.\d{4,6}\.\d{6,8}\-\d",
        0,
    ],
    "pr": [[r"(\n\n\s*?)(\d{1,4} \. Processo)", r"(\n\n\s*?)(\d+\.)"], re_num_cnj, 0],
    "rj": [r"\nProc\.", re_num_cnj, 0],
    "rn": [
        re_final_rn,
        r"\d{4,8}\s*-*\.*\s*\d{2}\s*\.\s*\d{4}\s*\.\s*\d{1}\s*\.\s*\d{2}\s*\.\s*\d{4}|\d{4}\.\d{6}\-\d",
        0,
    ],
    "ro": [re_final_ro, re_num_cnj, 0,],
    "rr": [[r"(\n\n\s*?)(\d{3}\s*?\-)"], re_num_cnj, 0],
    "rs": [
        [
            r"(\n\n\s*?)(EDITAL DE)",
            r"(\n\n\s*?)(\d{7})",
            r"(\n\n\s*?)(\d+.*?\(?\s*?CNJ)",
        ],
        re_num_cnj,
        0,
    ],
    "sc": [re_final_sc, re_num_cnj, 0,],
    "se": [
        [
            r"(\n\n\s*?)(NO\. PROCESSO)",
            r"(\n\n\s*?)(NO\. ACORDÃO)",
            r"(\n\n\s*?)(PROC\.\:)",
        ],
        r"\d{4,8}\s*-*\.*\s*\d{2}\s*\.\s*\d{4}\s*\.\s*\d{1}\s*\.\s*\d{2}\s*\.\s*\d{4}|\d{10,12}",
        0,
    ],
    "sp": [
        re_final_sp,
        r"\d{4,8}\s*[-\.]\s*\d{2}\s*\.\s*\d{4}\s*\.\s*\d{1}\s*\.\s*\d{2}\s*\.\s*\d{4}|\d{4,8}\s*-*\.*\s*\d{6}\-*\.*\d",
        0,
    ],
    "stf": [re_final_stf, re_num_cnj, 0,],
    "to": [
        re_final_to,
        r"\d{4,8}\s*-*\.*\s*\d{2}\s*\.\s*\d{4}\s*\.\s*\d{1}\s*\.\s*\d{2}\s*\.*\-*\s*\d{4}|\d{4}\.\d{4}\.\d{4}\-*\.*\d|\d{4}\/\d{2}",
        0,
    ],
    "trf1": [re_final_trf1, re_num_trf_trt, re.I,],
    "trf2": [re_final_trf4, re_num_trf_trt, 0,],
    "trf3": [re_final_trf3, re_num_trf_trt, 0,],
    "trf4": [re_final_trf4, re_num_trf_trt, 0,],
    "trf5": [re_final_trf5, re_num_trf_trt, 0,],
    "trt": [
        [
            r"(\n\n\s*?)(Processo N)",
            r"(\n\n\s*?)(Processo RO)",
            r"(\n\n\s*?)(PROCESSO N\.)",
        ],
        re_num_trf_trt,
        0,
    ],
}

tribunais_sem_separacao = ["stj"]


def encontra_publicacoes(tribunal, texto):
    if tribunal in tribunais_sem_separacao:
        return [texto]
    else:
        for separador in dicionario_separacao_diarios[tribunal][0]:
            texto = re.sub(separador, r"\1@@@@\2", texto)
        return [
            re.sub(r"\s+", " ", i)
            for i in re.split(
                r"@@@@", texto, flags=dicionario_separacao_diarios[tribunal][2],
            )[1:-1]
            if i and len(i) > 100
        ]


def encontra_numero(tribunal, texto):
    return busca(dicionario_separacao_diarios[tribunal][1], texto, ngroup=0).replace(
        "\n", ""
    )
