from common.conexao_local import cursorConexao
from common_nlp.pdf_to_text import pdf_to_text
from common.download_path import path
from crawler_jurisprudencia_tjac import crawler_jurisprudencia_tjac
from crawler_jurisprudencia_tjal import crawler_jurisprudencia_tjal
from crawler_jurisprudencia_tjam import crawler_jurisprudencia_tjam
from crawler_jurisprudencia_tjap import crawler_jurisprudencia_tjap
from crawler_jurisprudencia_tjba import crawler_jurisprudencia_tjba
from crawler_jurisprudencia_tjce import crawler_jurisprudencia_tjce
from crawler_jurisprudencia_tjdf import crawler_jurisprudencia_tjdf
from crawler_jurisprudencia_tjes import crawler_jurisprudencia_tjes
from crawler_jurisprudencia_tjgo import crawler_jurisprudencia_tjgo
from crawler_jurisprudencia_tjma import crawler_jurisprudencia_tjma
from crawler_jurisprudencia_tjmg import crawler_jurisprudencia_tjmg
from crawler_jurisprudencia_tjms import crawler_jurisprudencia_tjms
from crawler_jurisprudencia_tjmt import crawler_jurisprudencia_tjmt
from crawler_jurisprudencia_tjpa import crawler_jurisprudencia_tjpa
from crawler_jurisprudencia_tjpb import crawler_jurisprudencia_tjpb
from crawler_jurisprudencia_tjpe import crawler_jurisprudencia_tjpe
from crawler_jurisprudencia_tjpi import crawler_jurisprudencia_tjpi
from crawler_jurisprudencia_tjpr import crawler_jurisprudencia_tjpr
from crawler_jurisprudencia_tjrj import crawler_jurisprudencia_tjrj
from crawler_jurisprudencia_tjrn import crawler_jurisprudencia_tjrn
from crawler_jurisprudencia_tjro import crawler_jurisprudencia_tjro
from crawler_jurisprudencia_tjrr import crawler_jurisprudencia_tjrr
from crawler_jurisprudencia_tjrs import crawler_jurisprudencia_tjrs
from crawler_jurisprudencia_tjsc import crawler_jurisprudencia_tjsc
from crawler_jurisprudencia_tjse import crawler_jurisprudencia_tjse
from crawler_jurisprudencia_tjsp import crawler_jurisprudencia_tjsp
from crawler_jurisprudencia_tjto import crawler_jurisprudencia_tjto
from crawler_jurisprudencia_trf1 import crawler_jurisprudencia_trf1
from crawler_jurisprudencia_trf3 import crawler_jurisprudencia_trf3
from crawler_jurisprudencia_trf4 import crawler_jurisprudencia_trf4
from crawler_jurisprudencia_trf5 import crawler_jurisprudencia_trf5
from crawler_jurisprudencia_stf import crawler_jurisprudencia_stf
from crawler_jurisprudencia_stj import crawler_jurisprudencia_stj
import argparse

def acre(termo=None):
	c = crawler_jurisprudencia_tjac()
	print('comecei ',c.__class__.__name__)
	try:
		if termo:
			c.download_tj(termo=termo)
		else:
			c.download_tj()
	except Exception as e:
		print(e)

def alagoas(termo=None):
	c = crawler_jurisprudencia_tjal()
	print('comecei ',c.__class__.__name__)
	cursor = cursorConexao()
	for l in c.lista_anos:
		try:
			print(l,'\n')
			if termo:
				crawler_jurisprudencia_tj.download_tj_ESAJ_recaptcha(c,crawler_jurisprudencia_tj,'01/01/'+l,'31/12/'+l, termo=termo)
			else:
				crawler_jurisprudencia_tj.download_tj_ESAJ_recaptcha(c,crawler_jurisprudencia_tj,'01/01/'+l,'31/12/'+l)
		except Exception as e:
			print(e)
	cursor.execute('SELECT id, ementas from justica_estadual.jurisprudencia_al;')
	dados = cursor.fetchall()
	for id_p, dado in dados:
		try:
			c.parser_acordaos(dado, cursor)
		except:
			print(id_p)

def amazonas(termo=None):
	c = crawler_jurisprudencia_tjam()
	cursor = cursorConexao()
	print('comecei ',c.__class__.__name__)
	try:
		for l in range(3,len(c.lista_anos)):
			print(c.lista_anos[l],'\n')
			for m in range(len(c.lista_meses)):
				try:
					if termo:
						if m == 1:
							crawler_jurisprudencia_tj.download_tj_ESAJ(c,crawler_jurisprudencia_tj,'01'+c.lista_meses[m]+c.lista_anos[l],'28'+c.lista_meses[m]+c.lista_anos[l],termo=termo)
						elif m in [0,2,4,6,7,9,11]:
							crawler_jurisprudencia_tj.download_tj_ESAJ(c,crawler_jurisprudencia_tj,'01'+c.lista_meses[m]+c.lista_anos[l],'31'+c.lista_meses[m]+c.lista_anos[l],termo=termo)
						else:
							crawler_jurisprudencia_tj.download_tj_ESAJ(c,crawler_jurisprudencia_tj,'01'+c.lista_meses[m]+c.lista_anos[l],'30'+c.lista_meses[m]+c.lista_anos[l],termo=termo)
					else:
						if m == 1:
							crawler_jurisprudencia_tj.download_tj_ESAJ(c,crawler_jurisprudencia_tj,'01'+c.lista_meses[m]+c.lista_anos[l],'28'+c.lista_meses[m]+c.lista_anos[l])
						elif m in [0,2,4,6,7,9,11]:
							crawler_jurisprudencia_tj.download_tj_ESAJ(c,crawler_jurisprudencia_tj,'01'+c.lista_meses[m]+c.lista_anos[l],'31'+c.lista_meses[m]+c.lista_anos[l])
						else:
							crawler_jurisprudencia_tj.download_tj_ESAJ(c,crawler_jurisprudencia_tj,'01'+c.lista_meses[m]+c.lista_anos[l],'30'+c.lista_meses[m]+c.lista_anos[l])
				except Exception as e:
					print(e)
	except Exception as e:
		print(e)
	cursor.execute('SELECT id,ementas from justica_estadual.jurisprudencia_am where id > 29237 limit 10000000;')
	lista_links = cursor.fetchall()
	c.download_acordao_am(lista_links)
	p = pdf_to_text()
	for arq in os.listdir(path+'/am_2_inst'):
		c.parser_acordaos(path+'/am_2_inst/'+arq, cursor, p)

def amapa(termo=None):
	c = crawler_jurisprudencia_tjap()
	print('comecei ',c.__class__.__name__)
	try:
		if termo:
			c.download_tj(termo=termo)
		else:
			c.download_tj()
	except:
		print('finalizei com erro\n')

def bahia(termo=None):
	c = crawler_jurisprudencia_tjba()	
	print('comecei ',c.__class__.__name__)
	try:
		if termo:
			c.download_tj(termo=termo)
		else:
			c.download_tj()
	except Exception as e:
		print('finalizei com erro ',e)
	cursor = cursorConexao()
	p = pdf_to_text()
	for arq in os.listdir(path+'/ba_2_inst'):
		c.parser_acordaos(path+'/ba_2_inst/'+arq, cursor, p)

def ceara(termo=None):
	c = crawler_jurisprudencia_tjce()
	print('comecei ',c.__class__.__name__)
	try:
		for l in range(len(c.lista_anos)):
			print(c.lista_anos[l],'\n')
			try:
				if termo:
					crawler_jurisprudencia_tj.download_tj_ESAJ_recaptcha(c,crawler_jurisprudencia_tj,'0101'+c.lista_anos[l],'3112'+c.lista_anos[l],termo=termo)
				else:
					crawler_jurisprudencia_tj.download_tj_ESAJ_recaptcha(c,crawler_jurisprudencia_tj,'0101'+c.lista_anos[l],'3112'+c.lista_anos[l],termo='processo')
			except Exception as e:
				print(e)
	except Exception as e:
		print('finalizei o ano com erro ', e)
	cursor = cursorConexao()
	cursor.execute('SELECT ementas from justica_estadual.jurisprudencia_ce;')
	dados = cursor.fetchall()
	for ementa in dados:
		c.parser_acordaos(ementa[0], cursor)

def distrito_federal(termo=None):
	c = crawler_jurisprudencia_tjdf()
	print('comecei ',c.__class__.__name__)
	try:
		c.download_tj(50000) #número atualizado em jun 2018
	except Exception as e:
		print(e)
	subprocess.Popen('cd %s;for A in *.doc; do libreoffice --headless --convert-to docx $A; done; for A in *.doc; do rm $A; done;' % (path+'/df_2_inst/',), shell=True)
	cursor = cursorConexao()
	for arq in os.listdir(path+'/df_2_inst'):
		if re.search(r'docx',arq):
			try:
				c.parser_acordaos(path+'/df_2_inst/'+arq, cursor)
			except Exception as e:
				print(arq, e)

def espirito_santo(termo=None):
	c = crawler_jurisprudencia_tjes()
	cursor = cursorConexao()
	print('comecei ',c.__class__.__name__)
	try:
		c.download_tj()
	except Exception as e:
		print('finalizei com erro ',e)
	cursor.execute('SELECT ementas from justica_estadual.jurisprudencia_es;')
	dados = cursor.fetchall()
	for dado in dados:
		c.parser_acordaos(dado[0], cursor)

def goias(termo=None):
	c = crawler_jurisprudencia_tjgo()
	cursor = cursorConexao()
	print('comecei ',c.__class__.__name__)
	try:
		if termo:
			c.download_tj(termo=termo)
		else:
			c.download_tj()
	except Exception as e:
		print(e)
	cursor.execute('SELECT ementas from justica_estadual.jurisprudencia_go;')
	dados = cursor.fetchall()
	for dado in dados:
		c.parser_acordaos(dado[0], cursor)

def maranhao(termo=None):
	c = crawler_jurisprudencia_tjma()
	cursor = cursorConexao()
	try:
		for a in c.lista_anos:
			for m in range(len(c.lista_meses)):
				if termo:
					if m == 1:
						c.download_tj('01'+c.lista_meses[m]+a,'28'+c.lista_meses[m]+a, termo=termo)
					elif m in [0,2,4,6,7,9,11]:
						c.download_tj('01'+c.lista_meses[m]+a,'31'+c.lista_meses[m]+a, termo=termo)
					else:
						c.download_tj('01'+c.lista_meses[m]+a,'30'+c.lista_meses[m]+a, termo=termo)
				else:
					if m == 1:
						c.download_tj('01'+c.lista_meses[m]+a,'28'+c.lista_meses[m]+a)
					elif m in [0,2,4,6,7,9,11]:
						c.download_tj('01'+c.lista_meses[m]+a,'31'+c.lista_meses[m]+a)
					else:
						c.download_tj('01'+c.lista_meses[m]+a,'30'+c.lista_meses[m]+a)
	except Exception as e:
		print(e)
	cursor.execute('SELECT id, ementas from justica_estadual.jurisprudencia_ma;')
	dados = cursor.fetchall()
	for id_d, dado in dados:
		try:
			c.parser_acordaos(dado, cursor)
		except Exception as e:
			print(id_d, e)

def minas_gerais(termo=None):
	c = crawler_jurisprudencia_tjmg()
	print('comecei ',c.__class__.__name__)
	try:
		for a in c.lista_anos:
			for m in range(len(c.lista_meses)):
				if termo:
					if m == 1:
						c.download_tj('01'+c.lista_meses[m]+a,'14'+c.lista_meses[m]+a,termo=termo)
						c.download_tj('15'+c.lista_meses[m]+a,'28'+c.lista_meses[m]+a,termo=termo)
					elif m in [0,2,4,6,7,9,11]:
						c.download_tj('01'+c.lista_meses[m]+a,'14'+c.lista_meses[m]+a,termo=termo)
						c.download_tj('15'+c.lista_meses[m]+a,'31'+c.lista_meses[m]+a,termo=termo)
					else:
						c.download_tj('01'+c.lista_meses[m]+a,'14'+c.lista_meses[m]+a,termo=termo)
						c.download_tj('15'+c.lista_meses[m]+a,'30'+c.lista_meses[m]+a,termo=termo)
				else:
					if m == 1:
						c.download_tj('01'+c.lista_meses[m]+a,'14'+c.lista_meses[m]+a)
						c.download_tj('15'+c.lista_meses[m]+a,'28'+c.lista_meses[m]+a)
					elif m in [0,2,4,6,7,9,11]:
						c.download_tj('01'+c.lista_meses[m]+a,'14'+c.lista_meses[m]+a)
						c.download_tj('15'+c.lista_meses[m]+a,'31'+c.lista_meses[m]+a)
					else:
						c.download_tj('01'+c.lista_meses[m]+a,'14'+c.lista_meses[m]+a)
						c.download_tj('15'+c.lista_meses[m]+a,'30'+c.lista_meses[m]+a)
	except Exception as e:
		print('finalizei com erro ',e)

	cursor = cursorConexao()
	cursor.execute('SELECT ementas from justica_estadual.jurisprudencia_mg;')
	dados = cursor.fetchall()
	for dado in dados:
		c.parser_acordaos(dado[0], cursor)

def mato_grosso(termo=None):
	c = crawler_jurisprudencia_tjmt()	
	cursor = cursorConexao()
	p = pdf_to_text()
	print('comecei ',c.__class__.__name__)
	try:
		c.download_tj(termo=termo)
	except Exception as e:
		print(e)
	for arq in os.listdir(path+'/mt_2_inst'):
		try:
			c.parser_acordaos(path+'/mt_2_inst/'+arq, cursor, p)
		except Exception as e:
			print(e)

def mato_grosso_sul(termo=None):
	c = crawler_jurisprudencia_tjms()
	cursor = cursorConexao()
	print('comecei ',c.__class__.__name__)
	try:
		for l in range(len(c.lista_anos)):
			print(c.lista_anos[l],'\n')
			try:
				if termo:
					crawler_jurisprudencia_tj.download_tj_ESAJ_recaptcha(c,crawler_jurisprudencia_tj,'0101'+c.lista_anos[l],'3112'+c.lista_anos[l], termo=termo)
				else:
					crawler_jurisprudencia_tj.download_tj_ESAJ_recaptcha(c,crawler_jurisprudencia_tj,'0101'+c.lista_anos[l],'3112'+c.lista_anos[l])
			except Exception as e:
				print(e)
	except Exception as e:
		print(e)
	cursor.execute('SELECT ementas from justica_estadual.jurisprudencia_ms;')
	dados = cursor.fetchall()
	for dado in dados:
		c.parser_acordaos(dado[0], cursor)

def para(termo=None):
	c = crawler_jurisprudencia_tjpa()
	print('comecei ',c.__class__.__name__)
	for a in c.lista_anos:
		try:
			if termo:
				for m in range(len(c.lista_meses)):
					for i in range(1,8):
						try:
							c.download_tj('0'+str(i)+'/'+c.lista_meses[m]+'/'+a,'0'+str(i+1)+'/'+c.lista_meses[m]+'/'+a, termo=termo)
						except Exception as e:
							print(e)		
					for i in range(10,27):
						try:
							c.download_tj(str(i)+'/'+c.lista_meses[m]+'/'+a,str(i+1)+'/'+c.lista_meses[m]+'/'+a, termo=termo)
						except Exception as e:
							print(e)
			else:
				for m in range(len(c.lista_meses)):
					for i in range(1,8):
						try:
							c.download_tj('0'+str(i)+'/'+c.lista_meses[m]+'/'+a,'0'+str(i+1)+'/'+c.lista_meses[m]+'/'+a)
						except Exception as e:
							print(e)		
					for i in range(10,27):
						try:
							c.download_tj(str(i)+'/'+c.lista_meses[m]+'/'+a,str(i+1)+'/'+c.lista_meses[m]+'/'+a)
						except Exception as e:
							print(e)
		except Exception as e:
			print(e)
	cursor = cursorConexao()
	cursor.execute('SELECT ementas from justica_estadual.jurisprudencia_pa;')
	dados = cursor.fetchall()
	for dado in dados:
		c.parser_acordaos(dado[0], cursor)

def paraiba(termo=None):
	c = crawler_jurisprudencia_tjpb()
	cursor = cursorConexao()
	p = pdf_to_text()
	print('comecei ',c.__class__.__name__)
	try:
		for a in c.lista_anos:
			for m in range(len(c.lista_meses)):
				if termo:
					if m == 1:
						c.download_tj('01'+c.lista_meses[m]+a,'14'+c.lista_meses[m]+a,termo=termo)
						c.download_tj('15'+c.lista_meses[m]+a,'28'+c.lista_meses[m]+a,termo=termo)
					elif m in [0,2,4,6,7,9,11]:
						c.download_tj('01'+c.lista_meses[m]+a,'14'+c.lista_meses[m]+a,termo=termo)
						c.download_tj('15'+c.lista_meses[m]+a,'31'+c.lista_meses[m]+a,termo=termo)
					else:
						c.download_tj('01'+c.lista_meses[m]+a,'14'+c.lista_meses[m]+a,termo=termo)
						c.download_tj('15'+c.lista_meses[m]+a,'30'+c.lista_meses[m]+a,termo=termo)
				else:
					if m == 1:
						c.download_tj('01'+c.lista_meses[m]+a,'14'+c.lista_meses[m]+a)
						c.download_tj('15'+c.lista_meses[m]+a,'28'+c.lista_meses[m]+a)
					elif m in [0,2,4,6,7,9,11]:
						c.download_tj('01'+c.lista_meses[m]+a,'14'+c.lista_meses[m]+a)
						c.download_tj('15'+c.lista_meses[m]+a,'31'+c.lista_meses[m]+a)
					else:
						c.download_tj('01'+c.lista_meses[m]+a,'14'+c.lista_meses[m]+a)
						c.download_tj('15'+c.lista_meses[m]+a,'30'+c.lista_meses[m]+a)
	except Exception as e:
		print(e)
	cursor.execute('SELECT id,ementas from justica_estadual.jurisprudencia_pb where id > 37630 limit 10000000;')
	lista_links = cursor.fetchall()
	for i,l in lista_links:
		try:
			c.download_acordao_pb(str(i),l)
		except Exception as e:
			print(e,i)
	for arq in os.listdir(path+'/pb_2_inst'):
		try:
			c.parser_acordaos(path+'/pb_2_inst/'+arq, cursor, p)
		except Exception as e:
			print(arq)
			print(e)

def parana(termo=None):
	c = crawler_jurisprudencia_tjpr()
	print('comecei ',c.__class__.__name__)
	try:
		if termo:
			c.download_tj(termo=termo)
		else:
			c.download_tj()
	except Exception as e:
		print(e)
	cursor = cursorConexao()
	cursor.execute('SELECT ementas from justica_estadual.jurisprudencia_pr;')
	dados = cursor.fetchall()
	for dado in dados:
		c.parser_acordaos(dado[0], cursor)

def pernambuco(termo=None):
	# 'Nao ha precedentes disponiveis'
	pass

def piaui(termo=None):
	c = crawler_jurisprudencia_tjpi()
	cursor = cursorConexao()
	print('comecei ',c.__class__.__name__)
	try:
		if termo:
			c.download_tj(termo=termo)
		else:
			c.download_tj()
	except Exception as e:
		print(e)
	cursor.execute('SELECT ementas from justica_estadual.jurisprudencia_pi;')
	dados = cursor.fetchall()
	for dado in dados:
		c.parser_acordaos(dado[0], cursor)

def rio_de_janeiro(termo=None):
	c = crawler_jurisprudencia_tjrj()
	cursor = cursorConexao()
	print('comecei ',c.__class__.__name__)
	try:
		for l in c.lista_anos:
			print(l,'\n')
			if termo:
				c.download_tj(l,l,termo=termo)
			else:
				c.download_tj(l,l)
	except Exception as e:
		print(e)
	p = pdf_to_text()
	for arq in os.listdir(path+'/rj_2_inst'):
		try:
			c.parser_acordaos(path+'/rj_2_inst/'+arq, cursor, p)
		except:
			print(arq)

def rio_grande_do_norte(termo=None):
	c = crawler_jurisprudencia_tjrn()
	print('comecei ',c.__class__.__name__)
	try:
		for l in range(len(c.lista_anos)):
			print(c.lista_anos[l],'\n')
			for m in range(len(c.lista_meses)):
				try:
					if termo:
						if m == 1:
							c.download_tj('01'+c.lista_meses[m]+c.lista_anos[l],'28'+c.lista_meses[m]+c.lista_anos[l],termo=termo)
						elif m in [0,2,4,6,7,9,11]:
							c.download_tj('01'+c.lista_meses[m]+c.lista_anos[l],'31'+c.lista_meses[m]+c.lista_anos[l],termo=termo)
						else:
							c.download_tj('01'+c.lista_meses[m]+c.lista_anos[l],'30'+c.lista_meses[m]+c.lista_anos[l],termo=termo)
					else:
						if m == 1:
							c.download_tj('01'+c.lista_meses[m]+c.lista_anos[l],'28'+c.lista_meses[m]+c.lista_anos[l])
						elif m in [0,2,4,6,7,9,11]:
							c.download_tj('01'+c.lista_meses[m]+c.lista_anos[l],'31'+c.lista_meses[m]+c.lista_anos[l])
						else:
							c.download_tj('01'+c.lista_meses[m]+c.lista_anos[l],'30'+c.lista_meses[m]+c.lista_anos[l])
				except Exception as e:
					print(e)
	except Exception as e:
		print('finalizei o ano com erro ',e)

	cursor = cursorConexao()
	cursor.execute('SELECT ementas from justica_estadual.jurisprudencia_rn limit 1000000')
	dados = cursor.fetchall()
	for dado in dados:
		c.parser_acordaos(dado[0], cursor)

def rio_grande_do_sul(termo=None):
	c = crawler_jurisprudencia_tjrs()
	cursor = cursorConexao()
	print('comecei ',c.__class__.__name__)
	try:
		for l in range(len(c.lista_anos)):
			print(c.lista_anos[l],'\n')
			for m in range(len(c.lista_meses)):
				for i in range(1,8):
					try:
						if termo:
							c.download_tj('0'+str(i)+c.lista_meses[m]+c.lista_anos[l],'0'+str(i+1)+c.lista_meses[m]+c.lista_anos[l],termo=termo)
						else:
							c.download_tj('0'+str(i)+c.lista_meses[m]+c.lista_anos[l],'0'+str(i+1)+c.lista_meses[m]+c.lista_anos[l])
					except Exception as e:
						print(e)		
				for i in range(10,27):
					try:
						if termo:
							c.download_tj(str(i)+c.lista_meses[m]+c.lista_anos[l],str(i+1)+c.lista_meses[m]+c.lista_anos[l],termo=termo)
						else:
							c.download_tj(str(i)+c.lista_meses[m]+c.lista_anos[l],str(i+1)+c.lista_meses[m]+c.lista_anos[l])
					except Exception as e:
						print(e)
	except Exception as e:
		print(e)
	cursor.execute('SELECT id, ementas from justica_estadual.jurisprudencia_rs;')
	links = cursor.fetchall()
	c.parser_acordaos(links)

def rondonia(termo=None):
	c = crawler_jurisprudencia_tjro()
	cursor = cursorConexao()
	print('comecei ',c.__class__.__name__)
	try:
		for l in range(len(c.lista_anos)):
			print(c.lista_anos[l])
			try:
				if termo:
					c.download_tj(c.lista_anos[l], termo=termo)
				else:
					c.download_tj(c.lista_anos[l])
			except Exception as e:
				print(e)
	except Exception as e:
		print(e)
	cursor.execute('SELECT ementas from justica_estadual.jurisprudencia_ro;')
	dados = cursor.fetchall()
	for dado in dados:
		c.parser_acordaos(dado[0], cursor)

def roraima(termo=None):
	c = crawler_jurisprudencia_tjrr()	
	cursor = cursorConexao()
	print('comecei ',c.__class__.__name__)
	try:
		if termo:
			c.download_tj(termo=termo)
		else:
			c.download_tj()
	except Exception as e:
		print(e)
	cursor.execute('SELECT ementas from justica_estadual.jurisprudencia_rr;')
	dados = cursor.fetchall()
	for dado in dados:
		c.parser_acordaos(dado[0], cursor)

def santa_catarina(termo=None):
	c = crawler_jurisprudencia_tjsc()
	cursor = cursorConexao()
	print('comecei ',c.__class__.__name__)
	for a in c.lista_anos:
		print(a)
		for m in range(len(c.lista_meses)):
			if termo:
				try:
					c.download_tj('01/'+c.lista_meses[m]+'/'+a,'14/'+c.lista_meses[m]+'/'+a, termo=termo)
				except Exception as e:
					print(e,c.lista_meses[m])
				try:
					c.download_tj('15/'+c.lista_meses[m]+'/'+a,'28/'+c.lista_meses[m]+'/'+a, termo=termo)
				except Exception as e:
					print(e,c.lista_meses[m])
			else:
				try:
					c.download_tj('01/'+c.lista_meses[m]+'/'+a,'14/'+c.lista_meses[m]+'/'+a)
				except Exception as e:
					print(e,c.lista_meses[m])
				try:
					c.download_tj('15/'+c.lista_meses[m]+'/'+a,'28/'+c.lista_meses[m]+'/'+a)
				except Exception as e:
					print(e,c.lista_meses[m])
	cursor.execute('SELECT id,ementas from justica_estadual.jurisprudencia_sc;')
	lista_links = cursor.fetchall()
	for i,l in lista_links:
		c.download_acordao_sc(l, i, cursor)
	cursor.execute('SELECT texto from justica_estadual.jurisprudencia_sc;')
	dados = cursor.fetchall()
	for dado in dados:
		c.parser_acordaos(dado[0], cursor)

def sao_paulo_1(termo=None):
	c = crawler_jurisprudencia_tjsp()
	cursor = cursorConexao()
	print('comecei 1a instancia ',c.__class__.__name__)
	try:
		for l in range(len(c.lista_anos)):
			print(c.lista_anos[l],'\n')
			for m in range(len(c.lista_meses)):
				try:
					if termo:
						if m == 1:
							c.download_1_inst('01'+c.lista_meses[m]+c.lista_anos[l],'28'+c.lista_meses[m]+c.lista_anos[l], termo=termo)
						elif m in [0,2,4,6,7,9,11]:
							c.download_1_inst('01'+c.lista_meses[m]+c.lista_anos[l],'31'+c.lista_meses[m]+c.lista_anos[l], termo=termo)
						else:
							c.download_1_inst('01'+c.lista_meses[m]+c.lista_anos[l],'30'+c.lista_meses[m]+c.lista_anos[l], termo=termo)
					else:
						if m == 1:
							c.download_1_inst('01'+c.lista_meses[m]+c.lista_anos[l],'28'+c.lista_meses[m]+c.lista_anos[l])
						elif m in [0,2,4,6,7,9,11]:
							c.download_1_inst('01'+c.lista_meses[m]+c.lista_anos[l],'31'+c.lista_meses[m]+c.lista_anos[l])
						else:
							c.download_1_inst('01'+c.lista_meses[m]+c.lista_anos[l],'30'+c.lista_meses[m]+c.lista_anos[l])
				except Exception as e:
					print(e)
	except Exception as e:
		print(e)
	for i in range(0,1500000,10000): # jun 2018
		print(1500000-i)
		cursor.execute('SELECT sentencas FROM justica_estadual.jurisprudencia_sp_1_inst limit %s,10000;' % str(i))
		dados = cursor.fetchall()
		for dado in dados:
			c.parse_sp_dados_1_inst(dado[0], cursor)

def sao_paulo_2(termo=None):
	c = crawler_jurisprudencia_tjsp()
	cursor = cursorConexao()
	print('comecei 2a instancia',c.__class__.__name__)
	try:
		for l in range(len(c.lista_anos)):
			print(c.lista_anos[l],'\n')
			for m in range(len(c.lista_meses)):
				try:
					if termo:
						crawler_jurisprudencia_tj.download_tj_ESAJ(c,crawler_jurisprudencia_tj,'01'+c.lista_meses[m]+c.lista_anos[l],'28'+c.lista_meses[m]+c.lista_anos[l],termo=termo)
					else:
						crawler_jurisprudencia_tj.download_tj_ESAJ(c,crawler_jurisprudencia_tj,'01'+c.lista_meses[m]+c.lista_anos[l],'28'+c.lista_meses[m]+c.lista_anos[l],termo='a')
				except Exception as e:
					print(e)
	except Exception as e:
		print(e)
	cursor.execute('SELECT ementas FROM justica_estadual.jurisprudencia_sp;')
	dados = cursor.fetchall()
	c.download_acordao_sp(dados)
	c.parse_sp_dados_2_inst(cursor)

def sergipe(termo=None):
	c = crawler_jurisprudencia_tjse()
	cursor = cursorConexao()
	print('comecei ',c.__class__.__name__)
	try:
		if termo:
			c.download_tj(termo=termo)
		else:
			c.download_tj()			
	except Exception as e:
		print(e)
	cursor.execute('SELECT ementas from justica_estadual.jurisprudencia_se;')
	dados = cursor.fetchall()
	for dado in dados:
		c.parser_acordaos(dado[0], cursor)

def superior_tribunal_de_justica(termo=None):
	c = crawler_jurisprudencia_stj()
	print('comecei ',p.__class__.__name__)
	if termo:
		c.baixarDadosProcesso(termo=termo)
	else:
		c.baixarDadosProcesso()
	c.baixarVotos()

def supremo_tribunal_federal(termo=None):
	c = crawler_jurisprudencia_stf()
	cursor = cursorConexao()
	print('comecei ',c.__class__.__name__)
	c.baixa_decisoes_proc()
	cursor.execute('SELECT id, link_pagina from stf.decisoes;')
	link_decisoes = cursor.fetchall()
	c.baixarDadosProcesso(link_decisoes)
	cursor.execute('SELECT id, link_dados from stf.dados_processo limit 1000000;')
	links_pai = cursor.fetchall()
	links_pai_d = {}
	for id_p,link in links_pai:
		links_pai_d[int(link.split('incidente=')[1])] = int(id_p)
	cursor.execute('SELECT id, link_pagina from stf.texto_decisoes limit 1000000;')
	links = cursor.fetchall()
	for id_l,link_pag in links:
		try:
			cursor.execute('UPDATE stf.texto_decisoes set id_processo = ("%s") where id = ("%s")' % (links_pai_d[int(link_pag.split('incidente=')[1])],id_l))
		except Exception as e:
			print(e)

def tocantins(termo=None):
	c = crawler_jurisprudencia_tjto()
	cursor = cursorConexao()
	print('comecei ',c.__class__.__name__)
	try:
		c.download_tj()
	except Exception as e:
		print(e)
	cursor.execute('SELECT id,ementas from justica_estadual.jurisprudencia_to;')
	lista_links = cursor.fetchall()
	for i,l in lista_links:
		try:
			c.download_acordao_to(str(i),l)
		except Exception as e:
			print(e,i)
	c.parser_acordaos()

def trf1(termo=None):
	c = crawler_jurisprudencia_trf1()
	print('comecei ',c.__class__.__name__)
	try:
		if termo:
			c.download_tj(termo=termo)
		else:
			c.download_tj()
	except Exception as e:
		print(e)
	cursor = cursorConexao()
	cursor.execute('SELECT ementas from justica_federal.jurisprudencia_trf1;')
	dados = cursor.fetchall()
	for dado in dados:
		c.parser_acordaos(dado[0], cursor)

def trf3(termo=None):
	c = crawler_jurisprudencia_trf3()
	print('comecei ',c.__class__.__name__)
	try:
		if termo:
			c.download_trf3(termo=termo)
		else:
			c.download_trf3()
	except Exception as e:
		print(e)

def trf4(termo=None):
	c = crawler_jurisprudencia_trf4()
	cursor = cursorConexao()
	print('comecei ',c.__class__.__name__)
	try:
		for l in range(len(c.lista_anos)):
			for m in range(len(c.lista_meses)):
				for i in range(1,9):
					try:
						if termo:
							c.download_trf4('0'+str(i)+c.lista_meses[m]+c.lista_anos[l],'0'+str(i+1)+c.lista_meses[m]+c.lista_anos[l],termo=termo)
						else:
							c.download_trf4('0'+str(i)+c.lista_meses[m]+c.lista_anos[l],'0'+str(i+1)+c.lista_meses[m]+c.lista_anos[l])
					except Exception as e:
						print(e)		
				for i in range(10,27):
					try:
						if termo:
							c.download_trf4(str(i)+c.lista_meses[m]+c.lista_anos[l],str(i+1)+c.lista_meses[m]+c.lista_anos[l],termo=termo)
						else:
							c.download_trf4(str(i)+c.lista_meses[m]+c.lista_anos[l],str(i+1)+c.lista_meses[m]+c.lista_anos[l])
					except Exception as e:
						print(e)
	except Exception as e:
		print(e)
	cursor.execute('SELECT ementas FROM justica_federal.jurisprudencia_trf4;')
	dados = cursor.fetchall()
	for ementa in dados:
		c.parser_acordaos(ementa[0],cursor)

def trf5(termo=None):
	c = crawler_jurisprudencia_trf5()
	try:
		for l in range(len(c.lista_anos)):
			print(c.lista_anos[l],'\n')
			for m in range(len(c.lista_meses)):
				for i in range(1,9):
					try:
						if termo:
							c.download_trf5('0'+str(i)+c.lista_meses[m]+c.lista_anos[l],'0'+str(i+1)+c.lista_meses[m]+c.lista_anos[l],termo=termo)
						else:
							c.download_trf5('0'+str(i)+c.lista_meses[m]+c.lista_anos[l],'0'+str(i+1)+c.lista_meses[m]+c.lista_anos[l])
					except Exception as e:
						print(e)		
				for i in range(10,27):
					try:
						if termo:
							c.download_trf5(str(i)+c.lista_meses[m]+c.lista_anos[l],str(i+1)+c.lista_meses[m]+c.lista_anos[l],termo=termo)
						else:
							c.download_trf5(str(i)+c.lista_meses[m]+c.lista_anos[l],str(i+1)+c.lista_meses[m]+c.lista_anos[l])
					except Exception as e:
						print(e)
	except Exception as e:
		print(e)

	cursor = cursorConexao()
	cursor.execute('SELECT ementas FROM justica_federal.jurisprudencia_trf5;')
	dados = cursor.fetchall()
	for ementa in dados:
		c.parser_acordaos(ementa[0],cursor)

lista_funcoes_jurisprudencia = [acre, alagoas, amapa, amazonas, bahia, ceara, distrito_federal, espirito_santo, goias,
maranhao, mato_grosso, mato_grosso_sul, minas_gerais, para, parana, paraiba, pernambuco, piaui, rio_de_janeiro, 
rio_grande_do_norte, rio_grande_do_sul, rondonia, roraima, santa_catarina, sergipe, sao_paulo_1, sao_paulo_2,
tocantins, superior_tribunal_de_justica, supremo_tribunal_federal]

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Script para download de jurisprudência dos tribunais disponíveis')
	parser.add_argument('-t',type=str,default=False,help='termo a ser utilizado como referencia na pesquisa',dest='t')
	
	def main_termo(termo):
		for func in lista_funcoes_jurisprudencia:
			func(termo)
	def main():
		for func in lista_funcoes_jurisprudencia:
			func()
	
	args = parser.parse_args()
	if args.t:
		main_termo(args.t)
	else:
		main()