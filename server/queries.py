import csv, io, sys
from conexao import cursorConexao

class Queries():
  def __init__(self):
    self.stf_query = 'SELECT processo, polo_ativo, polo_passivo, autuacao, numero_origem, relator, ramo_direito, assunto, tribunal_origem, texto_decisao FROM stf.dados_processo inner join stf.decisoes on dados_processo.id = decisoes.id_processo where lower(texto_decisao) like "%{}%";'
    self.stf_campos = [['processo','polo_ativo','polo_passivo','autuacao','numero_origem','relator','ramo_direito','assunto','tribunal_origem','texto_decisao']]
    self.stj_query = 'SELECT texto_decisao FROM stf.decisoes where lower(texto_decisao) like "%{}%";'
    self.stj_campos = [['texto_decisao']]
    self.segunda_inst_query = 'SELECT tribunal, numero, assunto, classe, data_decisao, orgao_julgador, julgador, texto_decisao, relatorio, fundamentacao, dispositivo, polo_ativo, polo_passivo, origem from jurisprudencia_2_inst.jurisprudencia_2_inst where lower(texto_decisao) like "%{}%";'
    self.segunda_inst_campos = [['tribunal', 'numero', 'assunto', 'classe', 'data_decisao', 'orgao_julgador', 'julgador', 'texto_decisao', 'relatorio', 'fundamentacao', 'dispositivo', 'polo_ativo', 'polo_passivo', 'origem']]
    self.dicionario_tribunais = {
      'stf':
      [
      self.stf_query,
      self.stf_campos
      ],
      'stj':
      [
      self.stj_query,
      self.stj_campos
      ],
      'segunda_inst':
      [
      self.segunda_inst_query,
      self.segunda_inst_campos
      ]
    }

  def query_tribunais(self,termos,tribunal=None):
    dados = []
    if tribunal:
      cursor = cursorConexao()
      termos_parsed = self.parse_query_operadores(termos)
      if termos_parsed != termos:
        cursor.execute(self.dicionario_tribunais[tribunal][0].split(' where ')[0]+termos_parsed)
      else:
        cursor.execute(self.dicionario_tribunais[tribunal][0].format(termos))
      dados.extend(list(cursor.fetchall()))
    return dados

  def query_csv(self,dados,cabecalho):
    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerows(cabecalho)
    cw.writerows(dados)
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=relatorio.csv"
    output.headers["Content-type"] = "text/csv"
    return output

  def parse_query_operadores(self, texto, field='texto_decisao'):
    text = texto
    if len(text.split(' e ')) > 1 or len(text.split(' ou ')) > 1:
      texto_e = text.split(' e ')
      if len(texto_e) > 1:
        texto_final = ' where ('
        for i in range(len(texto_e)-1):
          texto_final += 'lower({}) like "%{}%" and '.format(field,texto_e[i])
        texto_final += 'lower({}) like "%{}%");'.format(field,texto_e[-1])
        return texto_final
      texto_ou = text.split(' ou ')
      if len(texto_ou) > 1:
        texto_final = ' where ('
        for i in range(len(texto_ou)-1):
          texto_final += 'lower({}) like "%{}%" or '.format(field,texto_ou[i])
        texto_final += 'lower({}) like "%{}%");'.format(field,texto_ou[-1])
        return texto_final
    else:
      return text

  def query_padrao(self, tribunal=None, termos=None, query_text=None):
    cursor = cursorConexao()
    if query_text:
      cursor.execute(query_text)
    else:
      if termos:
        self.query_tribunais(termos,tribunal=tribunal)
    return cursor.fetchall()
