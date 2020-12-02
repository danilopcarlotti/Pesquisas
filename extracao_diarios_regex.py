import os
import re
import os.path
import pandas as pd
import sys
from common.recursive_folders import recursive_folders

ini_path = '/home/deathstar/Documents/Diarios/Diarios_trf3'
final_path = '/home/deathstar/Documents/'
name_report = 'extracao_trf3_possessoria.csv'

dicionario_expressoes_1 = {
    'alienacao_fiduciaria': r'aliena\w{2}o\s?fiduci\wria',
    'acao_penal': r'a\w{2}o\s?penal',
    'arrendamento_mercantil': r'arrendamento[s]?\s+mercanti',
    'veiculos': r've\wculo[s]?\s?',
    'leasing': r'leasing',
    'bradesco': r'bradesco',
    'santander': r'santander',
    'dpvat': r'dpvat',
    'seguradora': r'seguradora',
    'criminal': r'criminal',
    'contratos_bancarios': r'contrato[s]?\s+banc\wrio[s]?',
    'ministerio_publico':
    r'a[cç][aã]o\scivil\sp[uú]blica[\s-]{1,3}minist[eé]rio\sp[uú]blico',
    'mandado_direito_adm':
    r'mandado\sde\sseguran[cç]a[\s-]{1,3}direito\sadmnistrativo',
    'mandado_concessao':
    r'mandado\sde\sseguran[cç]a[\s-]{1,3}concess[aã]o[\s/]{1,3}permiss[aã]o[\s/]{1,3}autoriza[cç][aã]o',
    'mandado_garantia':
    r'mandado\sde\sseguran[cç]a[\s-]{1,3}garantias\sconstitucionais',
    'mandado_exigibilidade':
    r'mandado\sde\sseguran[cç]a[\s-]{1,3}suspens[aã]o\sd[ea]\sexigibilidade',
    'direto_adm':
    r'a[cç][aã]o\scivil\sp[uú]blica[\s-]{1,3}direito\sadministrativo',
    'dominio_publico':
    r'a[cç][aã]o\scivil\sp[uú]blica[\s-]{1,3}dom[ií]nio\sp[uú]blico',
    'dano_ambiental':
    r'a[cç][aã]o\scivil\sp[uú]blica[\s-]{1,3}indeniza[cç][aã]o\spor\sdano\sambiental',
    'meio_ambiente': r'a[cç][aã]o\scivil\sp[uú]blica[\s-]{1,3}meio\sambiente',
    'moradia': r'a[cç][aã]o\scivil\sp[uú]blica[\s-]{1,3}moradia',
    'propriedade': r'a[cç][aã]o\scivil\sp[uú]blica[\s-]{1,3}propriedade',
    'resp_adm':
    r'a[cç][aã]o\scivil\sp[uú]blica[\s-]{1,3}responsabilidade\sda\sadministra[cç][aã]o',
    'flora': r'a[cç][aã]o\scivil\sp[uú]blica\sc[ií]vel[\s-]{1,3}flora',
    'civel_moradia':
    r'a[cç][aã]o\scivil\sp[uú]blica\sc[ií]vel[\s-]{1,3}moradia',
    'ordem_urb':
    r'a[cç][aã]o\scivil\sp[uú]blica\sc[ií]vel[\s-]{1,3}ordem\surban[ií]stica',
    'concessao_especial':
    r'a[cç][aã]o\sdeclarat[oó]ria\sde\sconcess[aã]o\sespecial\spara\sfins\sde\smoradia',
    'inexistencia_debito':
    r'a[cç][aã]o\sdeclarat[oó]ria\sdeinexist[eê]ncia\sde\sd[eé]bito',
    'apreensao':
    r'apreens[aã]o\se\sdep[oó]sito\sde\scoisa\svendida\scom\sreserva\sde\dom[ií]nio[\s-]{1,3}obriga[cç][oõ]es',
    'ausencia':
    r'declara[cç][aã]o\sde\saus[eê]ncia[\s-]{1,3}curadoria\sdos\bens\sdo\sausente',
    'demarcacao_divisao': r'divis[aã]o\se\sdemarca[cç][aã]o',
    'desapropriacao': r'desapropria[cç][aã]o[\s-]{1,3}desapropria[cç][aã]o',
    'denuncia_vazia': r'despejo[\s-]{1,3}despejo\spor\sden[uú]ncia\svazia',
    'falta_pagamento': r'despejo\spor\sfalta\sde\spagamento',
    'execucao_fiscal':
    r'embargos\s[aà]\sexecu[cç][aã]o\sfiscal[\s-]{1,3}nulidade',
    'embargos_coisas': r'embargos\s\sde\sterceiros[\s-]{1,3}coisas',
    'embargos_penhora':
    r'embargos\s\sde\sterceiros[\s-]{1,3}constri[cç][aã]o[\s/]{1,3}penhora[\s/]{1,3}avalia[cç][aã]o',
    'embargos_liquidacao':
    r'embargos\s\sde\sterceiros[\s-]{1,3}liquida[cç][aã]o[\s/]{1,3}cumprimento[\s/]{1,3}execu[cç][aã]o',
    'execucao_extrajudicial': r'execu[cç][aã]o\sde\st[ií]tulo\sextrajudicial',
    'execucao_iptu':
    r'execu[cç][aã]o\sfiscal[\s-]{1,3}iptu[\s/]{1,3}imposto\spredial\se\sterritorial\surbano',
    'execucao_taxas': r'execu[cç][aã]o\sfiscal[\s-]{1,3}taxas',
    'imissao': r'imiss[aã]o\s\sna\sposse[\s-]{1,3}propriedade',
    'inventario': r'invent[aá]rio[\s-]{1,3}invent[aá]rio\se\spartilha',
    'mandado_protesto':
    r'mandado\sde\sseguran[cç]a[\s-]{1,3}protesto\sindevido\sde\st[ií]tulo',
    'nuciacao_obra':
    r'nucia[cç][aã]o\sde\sobra\snova[\s-]{1,3}direito\sde\svizinhan[cç]a',
    'procedimento_aquisicao': r'procedimento\scomum[\s-]{1,3}aquisi[cç][aã]o',
    'procedimento_saj':
    r'procedimento\scomum[\s-]{1,3}assuntos\santigos\sdo\saj',
    'procedimento_edificio':
    r'procedimento\scomum[\s-]{1,3}condom[ií]nio\sem\sedif[ií]cio',
    'procedimento_desap':
    r'procedimento\scomum[\s-]{1,3}desapropria[cç][aã]o\sindireta',
    'procedimento_vizinhanca':
    r'procedimento\scomum[\s-]{1,3}direito\sde\svizinhan[cç]a',
    'procedimento_dano':
    r'procedimento\scomum[\s-]{1,3}indeniza[cç][aã]o\spor\sdano\smoral',
    'procedimento_moradia': r'procedimento\scomum[\s-]{1,3}moradia',
    'procedimento_multas':
    r'procedimento\scomum[\s-]{1,3}multas\se\sdemais\san[cç][oõ]es',
    'procedimento_reivindicacao':
    r'procedimento\scomum[\s-]{1,3}reivindica[cç][aã]o',
    'procedimento_usucapiao_1': r'procedimento\scomum[\s-]{1,3}usucapi[aã]o',
    'procedimento_desapropriacao_ind':
    r'procedimento\scomum\sc[ií]vel[\s-]{1,3}desapropria[cç][aã]o\sindireta',
    'procedimento_desapropriacao':
    r'procedimento\scomum\sc[ií]vel[\s-]{1,3}desapropria[cç][aã]o\spor\sutilidade\sp[uú]blica',
    'procedimento_civel_vizinhanca':
    r'procedimento\scomum\sc[ií]vel[\s-]{1,3}direito\sde\svizinhan[cç]a',
    'procedimento_condominio':
    r'procedimento\scomum\sc[ií]vel[\s-]{1,3}obriga[cç][aã]o\sde\sfazer[\s/]{1,3}n[aã]o\sfazer[\s-]{1,3}condom[ií]nio',
    'procedimento_juizao': r'procedimento\sdo\sjuizado\sespecial\sc[ií]vel',
    'procedimento_ordinario':
    r'procedimento\sordin[aá]rio[\s-]{1,3}anula[cç][aã]o\sde\sd[eé]bito\sfiscal',
    'procedimento_benfeitorias':
    r'procedimento\sordin[aá]rio[\s-]{1,3}benfeitorias',
    'procedimento_comodato': r'procedimento\sordin[aá]rio[\s-]{1,3}comodato',
    'procedimento_utilidade_pub':
    r'procedimento\sordin[aá]rio[\s-]{1,3}desapropria[cç][aã]o\spor\sutilidade\sp[uú]blica',
    'procedimento_agua':
    r'procedimento\sordin[aá]rio[\s-]{1,3}fornecimento\sde\s[aá]gua',
    'procedimento_inadimplemento':
    r'procedimento\sordin[aá]rio[\s-]{1,3}inadimplemento',
    'procedimento_dano_moral':
    r'procedimento\sordin[aá]rio[\s-]{1,3}indeniza[cç][aã]o\spor\sdano\smoral',
    'procedimento_dano_material':
    r'procedimento\sordin[aá]rio[\s-]{1,3}indeniza[cç][aã]o\spor\sdano\smaterial',
    'procedimento_propriedade':
    r'procedimento\sordin[aá]rio[\s-]{1,3}propriedade',
    'procedimento_usucapiao_2':
    r'procedimento\sordin[aá]rio[\s-]{1,3}usucapi[aã]o\sextraordin[aá]ria',
    'procedimento_usucapiao_3':
    r'procedimento\ssum[aá]rio[\s-]{1,3}usucapi[aã]o\sextraordin[aá]ria',
    'usucapiao_esbulho': r'usucapi[aã]o[\s-]{1,3}esbulho',
    'usucapiao_propriedade': r'usucapi[aã]o[\s-]{1,3}propriedade',
    'usucapiao_registro': r'usucapi[aã]o[\s-]{1,3}registro\sde\sim[oó]veis',
    'usucapiao_extra':
    r'usucapi[aã]o[\s-]{1,3}usucapi[aã]o\sextraordin[aá]ria',
    'usucapiao_ordin': r'usucapi[aã]o[\s-]{1,3}usucapi[aã]o\sordin[aá]ria',
    'usucapiao_especial': r'usucapi[aã]o\sespecial\s\(constitucional\)'
}

dicionario_expressoes_2 = {
    'manutencao_posse': r'manuten\w{2}o\s+d[ea]\s+posse',
    'reintegracao_posse': r'reintegra\w{2}o\s+d[ea]\s+posse',
    'interdito_proibitorio': r'interdito\s+proibit\wrio',
    'turbacao_esbulho_ameaca': r'esbulh|amea\wa|turba',
    'coletiva':r'ocupantes|invasor[ea]s|desconhecid[oa]s|fam[ií]lias|morador[ea]s|invadiram|ocuparam|amea[cç]aram|esbulharam|turbaram'
}

rows = []
rec = recursive_folders()
paths = rec.find_files(ini_path)
for f in paths:
    if f[-3:] == 'csv':
        print(f)
        try:
            df = pd.read_csv(os.path.join(ini_path, f))
        except Exception as e:
            print(e)
            continue
        for _, row in df.iterrows():
            if not re.search(r'manuten\w{2}o\s+d[ea]\s+posse|reintegra\w{2}o\s+d[ea]\s+posse|interdito\s+proibit\wrio',row['texto_publicacao'], re.S | re.I):
                continue
            flag = True
            for k, v in dicionario_expressoes_1.items():
                if re.search(v, row['texto_publicacao'], re.S | re.I):
                    flag = False
                    break
            if flag:
                dici = {}
                dici['numero_processo'] = row['numero_processo']
                dici['texto_publicacao'] = row['texto_publicacao']
                dici['tribunal'] = row['tribunal']
                dici['data'] = row['data']
                for k, v in dicionario_expressoes_2.items():
                    if re.search(v, row['texto_publicacao'], re.S | re.I):
                        dici[k] = 1
                    else:
                        dici[k] = 0
                rows.append(dici)

if len(rows) < 1000000:
    data_frame = pd.DataFrame(rows)
    data_frame.to_csv(os.path.join(final_path, name_report),index=False)
else:
    for i in range(0,len(rows),1000000):
        data_frame = pd.DataFrame(rows[i:i+1000000])
        data_frame.to_csv(os.path.join(final_path, name_report.replace('.csv','_'+str(i)+'.csv')),index=False)