from datetime import datetime
import pickle, pandas as pd, jellyfish, re

def encontra_string_semelhante(lista_nomes, stringAnalisada, nCaracteres):
	maior_semelhanca = 0
	item_normalizado = ''
	if nCaracteres:
		for item in lista_nomes:
			ratio_s = jellyfish.jaro_distance(stringAnalisada[:nCaracteres],item[:nCaracteres])
			if ratio_s > maior_semelhanca:
				maior_semelhanca = ratio_s
				item_normalizado = item
		if maior_semelhanca > 0.7:
			return item_normalizado
		else:
			return encontra_string_semelhante(lista_nomes, stringAnalisada, nCaracteres - 15)
	else:
		return 'Outros'


def main():
	lista_trf = ['.','agencias / orgaos de regulacao','planos de saude','seguro','servicos hospitalares','controle social e conselhos de saude','convenio medico com o sus','doacao e transplante de orgaos; tecidos e partes do corpo humano','financiamento do sus','fornecimento de medicamentos','genetica / celulas tronco','hospitais e outras unidades de saude','reajuste da tabela do sus','repasse de verbas do sus','ressarcimento ao sus','saude mental','terceirizacao do sus','tratamento medico-hospitalar','vigilancia sanitária e epidemiologica','assistencia a saude','unidade de terapia intensiva (uti) ou unidade de cuidados intensivos (uci)','internacao','tratamento ambulatorial','taxa de saude suplementar']
	lista_tj = ['.','saude','controle social e conselhos de saude','convenio medico com o sus','doacao e transplante de orgaos; tecidos e partes do corpo humano','financiamento do sus','fornecimento de medicamentos','genetica / celulas tronco','hospitais e outras unidades de saude','reajuste da tabela do sus','repasse de verbas do sus','ressarcimento ao sus','saude mental','internacao compulsoria ','internacao involuntaria ','internacao voluntaria','terceirizacao do sus','tratamento medico-hospitalar','unidade de terapia intensiva (uti) ou unidade de cuidados intensivos (uci)','tratamento medico-hospitalar e/ou fornecimento de medicamentos','vigilancia sanitaria e epidemiologica','medicamento / tratamento / cirurgia de eficacia nao comprovada','prescricao por medico nao vinculado ao sus','planos de saude','seguro','servicos hospitalares']
	lista_classe = ['processo de conhecimento','processos cautelares','procedimentos cautelares','cautelar inominada','tutela antecipada antecedente','tutela cautelar antecedente','procedimento de conhecimento','procedimento de cumprimento de sentenca/decisao','acao civil publica','procedimento ordinario','tutela','cautelar inominada','peticao civel','procedimento comum','procedimento sumario','cumprimento de sentenca','cumprimento de sentenca contra a fazenda publica','cumprimento provisorio de decisao','cumprimento provisorio de sentenca','execucao contra a fazenda publica','acao civil coletiva','acao civil publica','acao popular','mandado de injuncao','mandado de seguranca civel','mandado de seguranca coletivo','tutela','tutela antecipada antecedente','tutela cautelar antecedente','procedimento de liquidacao','liquidacao de sentenca pelo procedimento comum','liquidacao provisoria de sentenca pelo procedimento comum','.','processo de conhecimento','procedimentos cautelares','cautelar inominada','tutela antecipada antecedente','tutela cautelar antecedente','procedimento de conhecimento','procedimento de cumprimento de sentenca/decisao','procedimento de liquidacao','execucao de titulo extrajudicial','agravos','apelacao / remessa necessaria','apelacao civel','remessa necessaria civel','execucao de medida de seguranca','agravo de instrumento em recurso especial','agravo de instrumento em recurso extraordinario','agravo regimental','apelacao em mandado de seguranca','recurso em sentido estrito/recurso ex officio','mandado de seguranca infancia civel','pedido de efeito suspensivo à apelacao','procedimento conciliatorio','procedimento comum','procedimentos especiais','cumprimento de sentenca','cumprimento de sentenca contra a fazenda publica','cumprimento provisorio de decisao','cumprimento provisorio de sentenca','liquidacao de sentenca pelo procedimento comum','liquidacao provisoria de sentenca pelo procedimento comum','execucao contra a fazenda publica','agravo de instrumento','agravo de instrumento em recurso extraordinario','agravo regimental','procedimentos especiais de jurisdicao contenciosa','acao civil publica','acao popular','mandado de injuncao','mandado de seguranca civel','mandado de seguranca coletivo','procedimentos especiais de jurisdicao contenciosa','acao civil publica','acao popular','mandado de injuncao','mandado de seguranca civel','mandado de seguranca coletivo','.','pedido de mediacao pre-processual','processo civel e do trabalho ','processo cautelar','processo de conhecimento','processo de execucao','recursos','tutela provisoria','medidas cautelares','medidas garantidoras','medidas preparatorias','procedimento comum','processo especial','recursos','procedimento de conhecimento','procedimento de cumprimento de sentenca/decisao','tutela antecipada antecedente','tutela cautelar antecedente','peticao civel','assistencia judiciaria','procedimento do juizado especial civel','procedimentos especiais','cumprimento de sentenca','cumprimento provisorio de sentenca','excecao de coisa julgada','assistencia judiciaria','procedimentos especiais de jurisdicao contenciosa','.','outros procedimentos','processo cautelar','processo de conhecimento','medidas cautelares','medidas garantidoras','processo especial','cautelar inominada','procedimento de conhecimento','agravos','recurso de medida cautelar','recurso inominado','agravo de instrumento em recurso extraordinario','recurso de medida cautelar','recurso em sentido estrito/recurso ex officio','peticao civel','procedimentos especiais','agravo de instrumento','agravo de instrumento em recurso extraordinario','procedimentos especiais de jurisdicao contenciosa','mandado de seguranca civel','.','processo de conhecimento','processo de execucao','recursos','procedimento de conhecimento','execucao de titulo judicial','peticao civel','excecoes','procedimento do juizado especial civel','execucao contra a fazenda publica','.','outros procedimentos','recursos','questoes e processos incidentes','incidentes','incidentes','pedido de uniformizacao de interpretacao de lei','pedido de uniformizacao de interpretacao de lei']
	lista_partes = ['.','ace seguros','adm administradora de beneficios','aduseps associacao de defesa dos usuario','advance planos de saude','advogado','agemed saude','agf brasil seguros','alianca administradora de beneficios','allcare administradora de beneficios','allianz','ameplan assistencia medica','amhpla cooperativa de assistencia medica','amico saude','amil assistencia medica','asl assistencia a saude ltda','associacao','azul companhia de seguros gerais ','banco bradesco','banco do brasil','banco itau','banco santander','banestes seguros','bradesco saude','bradesco vida e previdencia ','brasil telecom','bv financeira','caixa beneficente dos','caixa de assistencia dos','caixa seguradora','camed operadora de plano de saude ltda','celesc distribuicao','celpe','centro de estudos juridicos da defensor','centro trasmontano de sao paulo','companhia de seguros alianca do brasil','defensor','defensoria publica','diretor do departamento regional','empresa federal de seguros s.a','estado de/do','excelsior med','fazenda publica','federal de seguros','fundacao municipal de saude','geap','generali brasil seguros','globex','golden cross','green line sistema de saude','grupo hospitalar do rio de janeiro','hapvida','hdi seguros','hospital','instituto de previdencia dos servidores ','instituto de recursos humanos do estado ','intermedica sistema de saude','ipsemg instituto previdencia servidores ','irmandade da santa casa de misericordia ','itau seguros','juizo','liberty seguros','light','mapfre vera cruz seguradora','maritima saude seguros','medial saude','medisanitas brasil assistencia integral ','mediservice operadora de planos de saude','memorial saude','ministerio publico','municipio','oi s.a','omint servicos de saude','operadora ideal saude ltda','ops - planos de saude','petroleo brasileiro s.a petrobras ','plano hospital samaritano','porto seguro','prevent senior','promotor','promotoria','qualicorp administradora de beneficios','real hospital portugues de beneficencia ','sao bernardo saude','secretario','seguradora lider dos consorcios','semeg saude ltda ','sociedade beneficente','sul america','telemar','telemar norte','tim','tnl pcs','tokio marine seguradora s a ','unibanco aig seguros','unicard','unihosp servicos de saude','unilife saude','unimed','vara','vision med assistencia medica','viva planos de saude','vivo','volkswagen do brasil','zurich']
	path_trf = '/media/danilo/USB/Dados_cnj/TRF_FINAL.xlsx'
	path_tj = '/media/danilo/USB/Dados_cnj/LAI_completa_proc_unico.csv'
	path_tj_final = '/media/danilo/USB/LAI_completa_proc_unico.csv'
	# dicionario_assuntos = {path_trf : lista_trf, path_tj : lista_cnj}
	dicionario_assuntos_tj = {path_tj : lista_tj}
	dicionario_assuntos = {path_trf : lista_trf}
	# print('Comecei assuntos trf')
	# for k,v in dicionario_assuntos.items():
	# 	df = pd.read_excel(k)
	# 	assunto_n = []
	# 	for index, row in df.iterrows():
	# 		try:
	# 			assunto_n.append(encontra_string_semelhante(v, row['assunto'], 30))
	# 		except:
	# 			assunto_n.append('Outros')
	# 	assunto_nm = pd.Series(assunto_n, name='assunto_normalizado', index=df.index)
	# 	df['assunto_normalizado'] = assunto_nm
		# df = df.applymap(lambda x: x.encode('unicode_escape').decode('utf-8') if isinstance(x, str) else x)
	# 	df.to_excel(k.split('/')[-1])
	print('Comecei tj')
	for k,v in dicionario_assuntos_tj.items():
		df = pd.read_csv(k,sep=';',nrows=10,encoding='latin1')
		assunto_n = []
		lista_aux = []
		lista_aux_parte_ativa = []
		lista_aux_parte_passiva = []
		for index, row in df.iterrows():
			try:
				assunto_n.append(encontra_string_semelhante(v, row['assunto2'], 30))
			except:
				assunto_n.append('Outros')
			try:
				lista_aux.append(encontra_string_semelhante(lista_classe, row['classe'], 30))
			except:
				lista_aux.append('Outros')

			try:
				lista_aux_parte_ativa.append(encontra_string_semelhante(i, row['parte_ativa2'], 30))
			except:
				lista_aux_parte_ativa.append('Outros')
			
			try:
				lista_aux_parte_passiva.append(encontra_string_semelhante(i, row['parte_passiva2'], 30))
			except:
				lista_aux_parte_passiva.append('Outros')

		lista_aux_parte_passiva = pd.Series(lista_aux_parte_passiva, name='parte_passiva_normalizada', index=df.index)
		df['parte_passiva_normalizada'] = lista_aux_parte_passiva
		lista_aux_parte_ativa = pd.Series(lista_aux_parte_ativa, name='parte_ativa_normalizada', index=df.index)
		df['parte_ativa_normalizada'] = lista_aux_parte_ativa
		lista_aux = pd.Series(lista_aux, name='classe_normalizada', index=df.index)
		df['classe_normalizada'] = lista_aux
		assunto_nm = pd.Series(assunto_n, name='assunto_normalizado', index=df.index)
		df['assunto_normalizado'] = assunto_nm
		df = df.applymap(lambda x: x.encode('unicode_escape').decode('utf-8') if isinstance(x, str) else x)
		df.to_csv(k.split('/')[-1])
	
if __name__ == '__main__':
	main()