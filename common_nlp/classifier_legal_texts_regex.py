import re


def resultado_decisao(texto, recursos=False):
    texto = texto[-1500:]
    res = -1
    if re.search(r"julg.{,15}procedente", texto, flags=re.I | re.S):
        if re.search(r"julg.{,15}\sprocedente", texto, flags=re.I | re.S):
            res = 1
        elif re.search(r"julg.{,15}improcedente", texto, flags=re.I | re.S):
            res = 0
    elif recursos and re.search(
        r"PROV.{1,20}RECURSO|D.{,5}PROVIMENTO|RECURSO.{0,30}PROVIDO|ORDEM.{1,10}CONCEDIDA|SEGURANÇA.{1,10}CONCEDIDA|REEXAME NECESSÁRIO.{1,20}PROVIDO|(SENTEN.A|DECIS.O).{1,20}(REFORMADA|MANTIDA)",
        texto,
        flags=re.I | re.S,
    ):
        if re.search(
            r"PROV.{1,20}RECURSO|D.{,5}PROVIMENTO|RECURSO.{0,30} PROVIDO|ORDEM.{1,10}CONCEDIDA|SEGURANÇA.{1,10}CONCEDIDA|REEXAME NECESSÁRIO.{1,20}PROVIDO|(SENTEN.A|DECIS.O).{1,20}REFORMADA",
            texto,
            flags=re.I | re.S,
        ):
            res = 1
        elif re.search(
            r"NEGA.{1,20}PROVIMENTO|REGIMENTAL.{1,20}IMPROVIDO|RECURSO.{1,30}IMPROVIDO|RECURSO.{1,30}DESPROVIDO|N.O PROVIDO|SENTEN.A.{1,30}MANTIDA|DECIS.O.{1,30}MANTIDA|SENTEN.A.{1,30}CONFIRMADA|SENTEN.A.{1,30}RATIFICADA|ORDEM.{1,10}NEGADA|CONHECID.{1,40}IMPROVIDO|REJEITADOS.{0,5}\.|REEXAME.{1,20}IMPROVIDO",
            texto,
            flags=re.I | re.S,
        ):
            res = 0
    return res
