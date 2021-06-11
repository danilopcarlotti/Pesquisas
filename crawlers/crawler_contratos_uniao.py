import sys, re, threading, time
from crawlerJus import crawlerJus
from bs4 import BeautifulSoup
from common.conexao_local import cursorConexao

link_licitacoes = "http://compras.dados.gov.br/licitacoes/v1/licitacoes.json?offset=%s"
link_fornecedores = (
    "http://compras.dados.gov.br/fornecedores/v1/fornecedores.json?offset=%s"
)
