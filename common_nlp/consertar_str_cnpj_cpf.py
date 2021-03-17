def consertar_str_cnpj(cnpj):
    cnpj = cnpj.replace("/", "").replace("-", "").replace(".", "")
    if len(cnpj) == 14:
        return cnpj
    elif len(cnpj) > 14:
        return consertar_str_cnpj(cnpj[:-1])
    else:
        return consertar_str_cnpj("0" + cnpj)


def consertar_str_cpf(cpf):
    cpf = cpf.replace("/", "").replace("-", "").replace(".", "")
    if len(cpf) == 11:
        return cpf
    elif len(cpf) > 11:
        return consertar_str_cpf(cpf[:-1])
    else:
        return consertar_str_cpf("0" + cpf)
