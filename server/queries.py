import csv, io, sys
from conexao import cursorConexao

class Queries():
  def __init__(self):
    self.stf_query = 'SELECT processo, polo_ativo, polo_passivo, autuacao, numero_origem, relator, ramo_direito, assunto, tribunal_origem, texto_decisao FROM stf.dados_processo inner join stf.decisoes on dados_processo.id = decisoes.id_processo where lower(texto_decisao) like "%{}%" limit 10000;'
    self.stf_campos = [['processo','polo_ativo','polo_passivo','autuacao','numero_origem','relator','ramo_direito','assunto','tribunal_origem','texto_decisao']]
    self.stj_query = 'SELECT texto_decisao FROM stf.decisoes where lower(texto_decisao) like "%{}%" limit 10000;'
    self.justica_estadual = 'SELECT texto FROM justica_estadual.{} where lower(texto) like "%{}%" limit 10000;'
    # self.segunda_inst_query = 'SELECT id, tribunal, texto_decisao from jurisprudencia_2_inst.jurisprudencia_2_inst where classificado is not NULL order by rand() limit 1;'
    self.segunda_inst_query = 'SELECT id, tribunal, texto_decisao from jurisprudencia_2_inst.jurisprudencia_2_inst where classe is not NULL limit 1;'
    self.dicionario_tribunais = {'stf':[self.stf_query,self.stf_campos]}

  def query_operadores(self,termos,tribunais=None,tribunal=None):
    if tribunal:
      dados = []
      cursor = cursorConexao()
      si = io.StringIO()
      cw = csv.writer(si)
      termos_parsed = self.parse_query_operadores(termos)
      if termos_parsed:
        cursor.execute(self.dicionario_tribunais[tribunal][0].split(' where ')[0]+termos_parsed)
      else:
        cursor.execute(self.dicionario_tribunais[tribunal][0].format(termos))
      dados.extend(list(cursor.fetchall()))
      cw.writerows(self.dicionario_tribunais[tribunal][1])
      cw.writerows(dados)
      output = make_response(si.getvalue())
      output.headers["Content-Disposition"] = "attachment; filename=relatorio_insper_cnj.csv"
      output.headers["Content-type"] = "text/csv"
      return output

  def parse_query_operadores(self, texto, field='texto_decisao'):
    text = texto.lower()
    if len(text.split(' e ')) > 1 or len(text.split(' ou ')) > 1:
      texto_e = text.split(' e ')
      if len(texto_e) > 1:
        texto_final = ' where ('
        for i in range(len(texto_e)-1):
          texto_final += 'lower({}) like "%{}%" and '.format(field,texto_e[i])
        texto_final += 'lower({}) like "%{}%") limit 10000;'.format(field,texto_e[-1])
        return texto_final
      texto_ou = text.split(' ou ')
      if len(texto_ou) > 1:
        texto_final = ' where ('
        for i in range(len(texto_ou)-1):
          texto_final += 'lower({}) like "%{}%" or '.format(field,texto_ou[i])
        texto_final += 'lower({}) like "%{}%") limit 10000;'.format(field,texto_ou[-1])
        return texto_final
    else:
      return text

  def query_padrao(self, query_text=None):
    cursor = cursorConexao()
    if query_text != None:
      cursor.execute(query_text)
    else:
      cursor.execute(self.segunda_inst_query)
    return cursor.fetchall()
