import re, pandas as pd
from crawlers.common.conexao_local import cursorConexao
from common_nlp.parserTextoJuridico import parserTextoJuridico

class extracao_variaveis():
	"""docstring for extracao_variaveis"""
	def __init__(self):
		self.var_bool = {
			"Privado": r"suplementar|seguro-sa.de|ANS|plano de sa.de|cooperativa m.dica",
			"Público": r"Secretaria|Minist.rio|Prefeitura|Munic.pio|Estado",
			"Representação": r"defensor|Defensoria",
			"ANS": r"ANS|Agencia Nacional de Saude",
			"Pedido Administrativo": r"administrativa|administrativo",
			"Coletiva relatório": r"A..o Civil P.blica|Mandado de Segurança Coletivo|A..o Popular",
			"Coletiva fundamentação": r"coletivo|coletiva|difusos|estrutural",
			"Medicamento": r"medicamento|farmaco",
			"Medicamentos selecionados": r"Teriparatide|Clopidogrel|insulin|rituximabe|infliximabe|bevacizumabe|sunitinib|adalimubabe|etanercept|rituximab|infliximab|bevacizumab|adalimubab|Carbamazepina|Pimecrolimo|asparte",
			"Medicamentos não incorporados": r"insulin.{1,3}glargin",
			"Diabetes": r"Diabetes",
			"HIV": r"antiretroviral|dolutegravir|efavirenz",
			"Hepatite C": r"veruprevir|ritonavir|ombitasvir|dasabuvir",
			"Mucopolissacaridose": r"laronidase|idursulfase|galsulfase",
			"Dietas": r"dieta|alimento|suplemento|enteral|f.rmula nutricional",
			"Insumo ou materiais": r"material|seringas|tiras|insumos|bomba",
			"Procedimentos": r"procedimento|procedimento cirurgico|cirurgia",
			"Exames": r"exame|ultrassom|resson.ncia|diagn.stico por imagem|ultrassonografia|radiografia|medicina|nuclear|tomografia",
			"Internação": r"interna..o",
			"Vagas": r"vaga",
			"Leitos": r"leito|unidade de isolamento|UTI|unidade de terapia intensiva|UCI|unidade de cuidados intermedi.rios",
			"Orteses, Proteses, Meios auxiliares de locomoção": r"ortese|protese|cadeira de rodas",
			"Transplante": r"transplante",
			"Imunização": r"vacina|imuniza..o|imunobiol.gicos|imunoglobinas",
			"Pericia médica judicial": r"per.cia|perit.|laudo pericial|laudo medico",
			"Dever do Estado": r"dever do Estado|dever Constitucional|assistencia terapeutica integral|art. 196|artigo 196|direito a saude|direito a vida|inciso II do art. 198|inciso II do artigo 198",
			"Anvisa": r"Anvisa",
			"Protocolos Clínicos": r"Protocolo|PCDT",
			"RENAME": r"RENAME|Medicamento.{1,3}Essencia|Política Nacional de Medicamentos|Política Nacional de Assistência Farmacêutica|1.897, de 26 de junho de 2017|Portaria n. 01/GM/MS, de 2 de janeiro de 2015|Componente Básico da Assistência Farmacêutica|Componente Estratégico da Assistência Farmacêutica|Componente Especializado da Assistência Farmacêutica|Relação Nacional de Insumos|Relação Nacional de Medicamentos de Uso Hospitalar",
			"RENUME": r"RENUME",
			"RENASE": r"RENASE",
			"RENEM":r"RENEM|Relacao Nacional de Equipamentos e Materiais permanentes financiaveis pelo SUS",
			"Pedido médico - bool":r"pedido médico|prescrição médica|requerimento médico|indicação médica|receita médica",
			"CONITEC - Bool" : r"CONITEC|Comissao Nacional de Incorporacao de Tecnologias no SUS|Camara Tecnica do Ministerio da Saude|lei 12.401",
			"NAT - Bool": r"N.cleo de Apoio T.cnico|NAT|NAT\-Jus",
			"Registro Nacional de Implantes": r"RNI|Registro Nacional de Implantes",
			"Medicamento importado": r"importado|importa..o",
			"Erro Médico": r"erro m.dico|neglig.ncia|imper.cia|imprud.ncia",
			"Sanções - bool": r"inibitoria|multa aplicada|aplicacao de multa|imposicao multa cominatoria|astreintes|ASTREINTE|bloqueio|sequestro de verba publica|prisão|responsabilização pessoal|BLOQUEIO DE VERBAS|pena de constricao de valores|ARTIGO 538 DO CPC|sancionatório-coercitivo",
			'medicamentos sem registro sanitário ou com uso "off-label"':r"Food and Drug Administration|FDA|European Medicines Agency",
			"Secretaria Estadual": r"Secretaria.{1,20}Est.{1,20}Sa.de|Secretaria.{1,20}Sa.de.{1,10}Estad|SES",
			"Secretaria Municipal": r"Secretaria.{1,20}Munic.{1,20}Sa.de|Secretaria.{1,20}Sa.de.{1,10}Munic|SMS",
			"Excentricidades" : r'Achocolatado diet|Água de coco|Suco de cramberry|Agua mineral|Leite de vaca integral e desnatado–líquido e em pó|Bebida à base de soja (Tipo Ades/ Sollys)|Bebida láctea sabor chocolate (tipoToddynho)|Granola|Açúcar mascavo|Bala de glicose líquida|instantânea|Mucilagem para o preparo de mingau|Papinhas infantis|Iogurte com fitoesteróis|Sopas Herbalife|Sabonete neutro|Shampoo neutro|Condicionador infantil para cabelos claros|Lenços umedecidos|Pomada contra assadura (tipoHipoglós)|Fraldas|Talco|Hasteflexivel (“cotonete”)|Águas termais|Hidratante “Davene”|Hidratantes importados|Absorventes intimos|Imunossupressor para cachorro|Fosfoetanolamina',
			"Hipossuficiência" : r"pessoa carente|insuficiência de renda|baixa renda",
			"Insumos" : r'água para injetáveis|álcool etílico|diafragma|dispositivo intrauterino plástico com cobre|gel lubrificante|glutaral|hipoclorito de sódio|iodo + iodeto de potássio|lancetas para punção digital|preservativo feminino|preservativo masculino|seringas com agulha acoplada para aplicação de insulina|tiras reagentes de medida de glicemia capilar',
			"Doenças prevalentes - S CODES" : r'diabetes mellitus insulino-dependente|diabetes mellitus não especificado|diabetes mellitus não insulino-dependente|intolerância a lactose|distúrbios do metabolismo de lipoproteínas e outras dislipidemias|doença de Alzheimer|distúrbios do sono|paralisia cerebral|epilepsia|esclerose múltipla|hipertensão essencial|acidente vascular cerebral não especificado como hemorrágico ou isquêmico|insuficiência cardíaca|sequelas de doenças cerebrovasculares|varizes dos membros inferiores|transtornos hipercinéticos|episódios depressivos|esquizofrenia|transtornos mentais e comportamentais devidos ao uso de múltiplas drogas e ao uso de outras substancias psicoativas|transtorno depressivo recorrente|osteoporose sem fratura patológica|gonartrose|outras artroses|osteoporose com fratura patológica|artrite reumatóide soro positiva',
			"Indicativo da existência de multa" : r'(imposição|aplicação|fixação|substitu).{1,15}multa'
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
				if re.search(v, texto):
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