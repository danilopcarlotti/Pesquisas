import re, pandas as pd
from crawlers.common.conexao_local import cursorConexao
from common_nlp.parserTextoJuridico import parserTextoJuridico

class extracao_variaveis():
	"""docstring for extracao_variaveis"""
	def __init__(self):
		self.var_bool = {
			"Privado": r"suplementar|seguro-sa.de|ANS|plano de sa.de|cooperativa m.dica",
			"Público": r"Secretaria|Minist.rio|Prefeitura|Munic.pio|Estado|SUS|Sistema .nico de Sa.de",
			"Representação": r"defensor|Defensoria",
			"ANS": r"ANS|Agencia Nacional de Sa.de",
			"Pedido Administrativo": r"administrativa|administrativo",
			"Coletiva relatório": r"A..o Civil P.blica|Mandado de Segurança Coletivo|A..o Popular",
			"Coletiva fundamentação": r"coletivo|coletiva|difusos|estrutural",
			"Medicamento": r"medicamento|f.rmaco",
			"Medicamentos selecionados (mais demandados)": r"Teriparatide|Clopidogrel|insulin|rituximabe|infliximabe|bevacizumabe|sunitinib|adalimubabe|etanercept|rituximab|infliximab|bevacizumab|adalimubab|Carbamazepina|Pimecrolimo|asparte",
			"Medicamentos não incorporados": r"insulin.{1,3}glargin",
			"Diabetes": r"Diabetes",
			"HIV": r"HIV|AIDS|antiretroviral|dolutegravir|efavirenz",
			"Hepatite C": r"hepatite c|veruprevir|ritonavir|ombitasvir|dasabuvir",
			"Mucopolissacaridose": r"laronidase|idursulfase|galsulfase",
			"Dietas": r"dieta|alimento|suplemento|enteral|f.rmula nutricional",
			"Insumo ou materiais": r"material|seringas|tiras|insumos|bomba",
			"Procedimentos": r"procedimento|procedimento cirurgico|cirurgia",
			"Exames": r"exame|ultrassom|resson.ncia|diagn.stico por imagem|ultrassonografia|radiografia|medicina|nuclear|tomografia",
			"Internação": r"interna..o",
			"Vagas": r"vaga",
			"Consultas": r"consulta.{1,20}m.dic",
			"Leitos": r"leito|unidade de isolamento|UTI|unidade de terapia intensiva|UCI|unidade de cuidados intermedi.rios",
			"Orteses, Proteses, Meios auxiliares de locomoção": r".rtese|pr.tese|cadeira de rodas|stent",
			"Máfia das próteses": r"m.fia",
			"Transplante": r"transplante",
			"Imunização": r"vacina|imuniza..o|imunobiol.gicos|imunoglobinas",
			"Pericia médica judicial": r"per.cia|perit.|laudo pericial|laudo m.dico",
			"Dever do Estado": r"dever do Estado|dever Constitucional|assist.ncia terapeutica integral|art. 196|artigo 196|direito a sa.de|direito a vida|inciso II do art. 198|inciso II do artigo 198",
			"Anvisa": r"Anvisa|ag.ncia nacional de vigil.ncia sanit.ria",
			"Protocolos Clínicos": r"Protocolo|PCDT",
			"RENAME": r"RENAME|Medicamento.{1,3}Ess.ncia|Pol.tica Nacional de Medicamentos|Pol.tica Nacional de Assist.ncia Farmac.utica|Portaria.{1,15}1.897|Portaria n. 01/GM/MS|Componente B.sico da Assist.ncia Farmac.utica|Componente Estrat.gico da Assist.ncia Farmac.utica|Componente Especializado da Assist.ncia Farmac.utica|Rela..o Nacional de Insumos|Rela..o Nacional de Medicamentos de Uso Hospitalar",
			"RENUME": r"RENUME|Rela..o municipal de medicamentos",
			"RENASE": r"RENASE|Rel..o nacional de servi.os",
			"RENEM":r"RENEM|Rela..o Nacional de Equipamentos e Materiais permanentes financi.veis pelo SUS",
			"Pedido médico - bool":r"pedido m.dico|prescri..o m.dica|requerimento m.dico|indica..o m.dica|receita m.dica",
			"CONITEC - Bool" : r"CONITEC|Comiss.o Nacional de Incorpora..o de Tecnologias|C.mara T.cnica do Minist.rio da Sa.de|lei 12.401",
			"NAT - Bool": r"N.cleo de Apoio T.cnico|NAT",
			"Registro Nacional de Implantes": r"RNI|Registro Nacional de Implantes",
			"Medicamento importado": r"importado|importa..o",
			"Erro Médico": r"erro m.dico|neglig.ncia|imper.cia|imprud.ncia",
			"Sanções - bool": r"inibit.ria|multa aplicada|aplica..o de multa|imposi..o multa cominat.ria|astreintes|ASTREINTE|bloqueio|sequestro de verba p.blica|pris.o|responsabiliza..o pessoal|BLOQUEIO DE VERBAS|pena de constri..o de valores|ARTIGO 538 DO CPC|sancionat.rio\-coercitivo",
			'medicamentos sem registro sanitário no Brasil':r"Food and Drug Administration|FDA|European Medicines Agency",
			"off-label": r"off-label",
			"Secretaria Estadual": r"Secretaria.{1,20}Est.{1,20}Sa.de|Secretaria.{1,20}Sa.de.{1,10}Estad|SES",
			"Secretaria Municipal": r"Secretaria.{1,20}Munic.{1,20}Sa.de|Secretaria.{1,20}Sa.de.{1,10}Munic|SMS",
			"Excentricidades" : r'Achocolatado diet|.gua de coco|Suco de cramberry|.gua mineral|Leite.{1,20}pasteurizado|Bebida . base de soja|Bebida l.ctea sabor chocolate|Toddynho|Granola|A..car mascavo|Bala de glicose líquida|instant.nea|Mucilagem para o preparo de mingau|Papinhas infantis|Iogurte com fitoester.is|Sopas Herbalife|Sabonete neutro|Shampoo neutro|Condicionador infantil para cabelos claros|Lenços umedecidos|Pomada contra assadura (tipoHipogl.s)|Fraldas|Talco|Hasteflexivel \(“cotonete”\)|.guas termais|Hidratante “Davene”|Hidratantes importados|Absorventes .ntimos|Imunossupressor para cachorro|Fosfoetanolamina',
			"Insuficiência de renda" : r"pessoa carente|insufici.ncia de renda|baixa renda",
			"Hipossuficiência": r"hipossufici",
			"Insumos" : r'.gua para injet.veis|.lcool et.lico|diafragma|dispositivo intrauterino pl.stico com cobre|gel lubrificante|glutaral|hipoclorito de s.dio|iodo.{1,15}iodeto de pot.ssio|lancetas para pun..o digital|preservativo feminino|preservativo masculino|seringas com agulha acoplada para aplica..o de insulina|tiras reagentes de medida de glicemia capilar',
			"Doenças prevalentes - S CODES" : r'diabetes mellitus insulino-dependente|diabetes mellitus n.o especificado|diabetes mellitus n.o insulino-dependente|intoler.ncia . lactose|dist.rbios do metabolismo de lipoprote.nas e outras dislipidemias|Alzheimer|dist.rbios do sono|paralisia cerebral|epilepsia|esclerose m.ltipla|hipertens.o essencial|acidente vascular cerebral n.o especificado como hemorr.gico ou isqu.mico|insufici.ncia card.aca|sequela.{1,10}doen.a.{1,10}cerebrovascular|varizes dos membros inferiores|transtornos hipercin.ticos|epis.dios depressivos|esquizofrenia|transtornos mentais e comportamentais devidos ao uso de m.ltiplas drogas e ao uso de outras subst.ncias psicoativas|transtorno depressivo recorrente|osteoporose sem fratura patol.gica|gonartrose|outras artroses|osteoporose com fratura patol.gica|artrite reumat.ide soro positiva',
			"Medicamentos prevalentes - S CODES" : r'Insulina glargina|Insulina asparte|Metilfenidato|Ranibizumabe|Insulina lispro|Ácido acetilsalicílico|Clopidogrel|Levotiroxina|Glicosamina + condroitina |Cloridrato de cinacalcete|Boceprevir 200 mg |Sinvastatina|Insulina detemir|Omeprazol|Insulina glulisina |Hialuronato de sódio |Pregabalina |Metformina + vildagliptina|Rosuvastatina|Ácido zoledrônico',
			"Indicativo da existência de multa" : r'(imposi..o|aplica..o|fixa..o|substitu).{1,15}multa',
			"ADPF 45": r"ADPF.{1,10}45",
			"Súmula 75, 182, 469 STJ": r"S.mula.{1,10}(75|182|469)",
			"CNJ": r"CNJ|Conselho nacional de justi.a"
		}
		self.var_bool['Rename - remédio'] = '|'.join([i.replace(' + ','.{1,20}').strip() for i in open('rename.txt','r')])
		self.var_bool['Medicamentos atenção básica'] = '|'.join([i.replace(' + ','.{1,20}').strip() for i in open('medicamentos_atencao_basica.txt','r')])
		self.var_bool['Medicamentos componente especializado'] = '|'.join([i.replace(' + ','.{1,20}').strip() for i in open('medicamentos_componente_especializado.txt','r')])
		self.var_bool['Medicamentos estratégicos'] = '|'.join([i.replace(' + ','.{1,20}').strip() for i in open('medicamentos_estrategicos.txt','r')])
		self.parser = parserTextoJuridico()

	def variaveis_textos(self, dicionario, dados):
		rows = []
		index = []
		index_counter = 1
		for id_p, texto, tribunal, data_decisao, polo_ativo, polo_passivo, origem in dados:
			est_ou_fed = 'estadual'
			if re.search(r'trf',tribunal):
				est_ou_fed = 'federal'
			ano_processo = re.search(r'\d{4}',str(data_decisao))
			if ano_processo:
				ano_processo = ano_processo.group(0)
			else:
				ano_processo = ''
			dicionario_df = {'numero':id_p, 'ano': ano_processo, 'tribunal':tribunal, 'data_decisao':data_decisao,'polo_ativo':polo_ativo,'polo_passivo':polo_passivo,'origem':origem,'estadual_federal':est_ou_fed,'resultado':self.parser.indicaResultado(texto,'Recurso'),'justica_gratuita':self.parser.justica_gratuita(texto)}
			for k,v in dicionario.items():
				if re.search(v, texto, re.DOTALL):
					dicionario_df[k] = 1
				else:
					dicionario_df[k] = 0
			rows.append(dicionario_df)
			index.append(index_counter)
			index_counter += 1
		data_frame = pd.DataFrame(rows, index=index)
		return data_frame

def main():
	ext = extracao_variaveis()
	df_saude = pd.read_csv('relatorio_cnj.csv', sep=';', quotechar='"', encoding = 'utf8')
	dados = []
	for row in df_saude.itertuples():
		dados.append((getattr(row,'numero'),getattr(row,'texto_decisao'),getattr(row,'tribunal'),getattr(row,'data_decisao'),getattr(row,'polo_ativo'),getattr(row,'polo_passivo'),getattr(row,'origem')))
	df = ext.variaveis_textos(ext.var_bool, dados)
	df['data_decisao'] = pd.to_datetime(df['data_decisao'], format='%d/%m/%Y', errors='coerce')
	df.to_csv('relatorio_booleano_cnj_03_out_2018.csv',quotechar='"', index= False)

if __name__ == '__main__':
	main()
