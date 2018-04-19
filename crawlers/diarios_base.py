import re

re_final_am = r'(\nPROCESSO DIGITAL: |\nDe ordem d[oa]|\nDespacho proferido pel|\n\d+ - Apelação n|\nProcesso n\. (?=\d{7})|\nProcesso :(?=\d{7})|\n\d+\. PROCESSO:(?=\d{7})|\nAutos n(?=\s*?\d{7})|\n\s*?ADV:)'
re_final_ac = r'(Acórdão n|\n\d+\. Classe|\n\d+ - (?=\d{7})|\nADV:|\nProcesso: |\nProcesso (?=\d+)|\nAutos n\.º|IV - ADMINISTRATIVO)'
re_final_ce = r'(\n.*?DESPACHO DE RELATORES|\n.*?DEC\s*?ISÃO MONOCRÁT\s?ICA|\n.*?EMENTA E CONCLUSÃO|\n.*?PORTAR\s*?IA|\n.*?CONFL\s*?ITO DE JUR\s*?ISD|\n.*?EMBARGOS DE DECLARAÇÃO|\n.*?APELAÇÃO|\nD\s*?ISTR\s*?IBU\s*?IÇÃO|\n[Nn]º (?=\d\d\d\d+))'
re_final_ma = r'(\nREQUERIMENTO DE |\nPETIÇÃO N|\nHABEAS CORPUS N|\nPORTARIA-TJ|\n\d{1,3}-PROCESSO|\nACÓRDÃO N|\nProcesso [Nn]º|\nProcesso:)'
re_final_pb = r'(\nAPELAÇÃO|\nEMBARGOS DE|\nAGRAVO|\nCONFLITO NEGATIVO|\nMANDADO DE SEGUR|\nRECURSO EM SENTIDO|\nREEXAME|\nRELATOR\(A\):|\nCOMARCA D|\nProcesso:|\nAgravo de Instrumento)'
re_final_pi = r'(\nPROCESSOS N|\n\d{1,3}\.\d{1,3}\. HABEAS CORPUS|\n\d{1,3}\.\d{1,3}\. AGRAVO DE INSTRUMENTO N|\n\d{1,3}\.\d{1,3}\. REEXAME NECESSÁRIO N|\n\d{1,3}\.\d{1,3}\. APELAÇÃO|\n\d{1,3}\.\d{1,3}\. MANDADO DE SEGURANÇA|\n\d{1,3}\.\d{1,3}\. DESPACHO|\n\d{1,3}\.\d{1,3}\. EDITAL |\n\d{1,3}\.\d{1,3}\. AVISO|\n\d{1,3}\.\d{1,3}\. ATO ORDINATÓRIO|\n\d{1,3}\.\d{1,3}\. SENTENÇA|\n\d{1,3}\.\d{1,3}\. AC.RDÃO)'
re_final_rn = r'(\nAPELAÇÃO|\nEMBARGOS DE|\nAGRAVO|\nCONFLITO NEGATIVO|\nMANDADO DE SEGUR|\nEXECUÇÃO N|\nEmbargos de|\nAgravo Interno|\nMandado de Segurança|\nApelação|\nExecução|\nAção Rescisória|\nADV:|\nAgravo de Instrumento)'
re_final_ro = r'(\nOrigem:|\nMandado de Segurança|\nNúmero do Processo|\nProcesso n|\nProc\.:|\nProcesso:)'
re_final_sc = r'(\n\s*ADV:|\nProcesso\s*(?=\d{7})|\n\d*\s*\.*\s*?Recurso |\n\d*\s*\.*\s*?Ag\s*ra\s*vo |\n\d*\s*\.*\s*?Embargo|\n\d*\s*\.*\s*?Apelação |\nRecurso |\n\s*N.\s*:(?=\d{4,7}))'
re_final_stf = r'(\nHABEAS CORPUS\s*?(?=\d+)|\nAGRAVO DE INSTRUMENTO\s*?(?=\d+)|\nMANDADO DE SEGURANÇA\s*?(?=\d+)|\nRECLAMAÇÃO\s*?(?=\d.\d+)|\nRECURSO EXTRAORDINÁRIO COM AGRAVO (?=\d+)|\nRECURSO EXTRAORDINÁRIO (?=\d+)|\nAG\.REG\.|\nEMB\.DECL\. (?=\d+)|\nAÇÃO DIRETA DE INCONSTITUCIONALIDADE (?=\d+)|\nAÇÃO ORIGINÁRIA (?=\d+)|\nAÇÃO PENAL (?=\d+)|\nMEDIDA CAUTELAR NA RECLAMAÇÃO (?=\d+)|\nMEDIDA CAUTELAR NA RECLAMAÇÃO (?=\d+)|\nCUMPRIMENTO DE SENTENÇA NA AÇÃO (?=\d+)|\nEXECUÇÃO CONTRA A FAZENDA (?=\d+)|\nEXTRADIÇÃO (?=\d+)|\nRECURSO ORDINÁRIO (?=\d+)|\nSEGUNDO AG\.REG\. (?=\d+))'
re_final_stj = r'(\nMANDADO DE SEGURANÇA [Nn]º|\nRECURSO ESPECIAL [Nn]º|\nAGRAVO EM RECURSO ESPECIAL [Nn]º|\nAgInt no RECURSO ESPECIAL [Nn]º|\nAgInt no RCD na MEDIDA CAUTELAR [Nn]º|\nEDcl no AgRg no RECURSO ESPECIAL [Nn]º|\nAgRg no AGRAVO EM RECURSO ESPECIAL [Nn]º|\nAgRg no RECURSO ESPECIAL [Nn]º|\nRECURSO EM HABEAS CORPUS [Nn]º|\nHABEAS CORPUS [Nn]º)'
re_final_to = r'(\nAutos|\nAUTOS N|\nProcesso N|\n\d+- Ação:|\nAÇÃO|\nEDITAL DE CITAÇÃO|\nEDITAL DE INTIMAÇÃO|\nPROCESSO N)'
re_final_trf4 = r'(\nAPELAÇÃO CÍVEL Nº|\nAPELAÇÃO.*?REMESSA NECESSÁRIA Nº|\nAGRAVO DE INSTRUMENTO Nº|\nEMBARGOS DE DECLARAÇÃO |\nEXECUÇÃO FISCAL Nº|\nPROCEDIMENTO COMUM Nº|\nEXECUÇÃO DE SENTENÇA CONTRA FAZENDA |\nEXECUÇÃO DE TÍTULO |\nEXECUÇÃO H\s*?IPOTECÁ|\nAÇÃO PENAL Nº|\nMON\s*?ITÓR\s*?IA Nº|\nREMESSA NECESSÁRIA CÍVEL Nº|\nAPELAÇÃO.*?REEXAME NECESSÁRIO Nº)'
re_num_cnj = r'\d{7}\s*-\s*\d{2}\s*\.\s*\d{4}\s*\.\s*\d{1}\s*\.\s*\d{2}\s*\.\s*\d{4}'
re_num_stf_stj = r'\d.*?( -)'
re_num_trf_trt =r'\d{7}\s*?-\d{2}\s*?\.\d{4}\s*?\.\d{1}\s*?\.\d{2}\s*?\.\d{4}|\d{7}\s*?-\d{2}\s*?\.\d{4}\s*?\.\d{3}\s*?\.\d{4}|\d{15}'

diarios = [
      ['sp',
      r'(\n\s*Processo|\n\s*?N.\s*(?=\d{7}|\n(?=.*)Processo D\s*ig\s*i\s*ta\s*l))(.*?)(\n\s*Processo|\n\s*?N.\s*(?=\d{7}|\n(?=.*)Processo D\s*ig\s*i\s*ta\s*l))'
      ],
      ['stf',
      r'{}(.*?){}'.format(re_final_stf,re_final_stf)
      ],
      ['stj',
      r'{}(.*?){}'.format(re_final_stj,re_final_stj)
      ],
      ['trf4',
      r'{}(.*?){}'.format(re_final_trf4,re_final_trf4)
      ],
      ['trf3',
      r'{}(.*?){}'.format(re_final_trf4,re_final_trf4)
      ],
      ['trf1',
      r'{}(.*?){}'.format(re_final_trf4,re_final_trf4)
      ],
      ['trt',
      r'(\nProcesso Nº|\nPROCESSO Nº|\nProcesso RO|\nPROCESSO N\.)(.*?)(\nProcesso Nº|\nPROCESSO Nº|\nProcesso RO|\nPROCESSO N\.)'
      ],
      ['rs',
      r'(\nEDITAL DE|\n(?=\d{7})-|\n.*?CNJ.*?\d{5,7}-?)(.*?)(\nEDITAL DE|\n(?=\d{7})-|\n.*?CNJ.*?\d{5,7}-?)'
      ],
      ['rn',
      r'{}(.*?){}'.format(re_final_rn,re_final_rn)
      ],
      ['pb',
      r'{}(.*?){}'.format(re_final_pb,re_final_pb)
      ],
      ['ms',
      r'\nProcesso (?=\d+)(.*?)\nProcesso (?=\d+)',
      ],
      ['ac',
      r'{}(.*?){}'.format(re_final_pb,re_final_pb)
      ],
      ['al',
      r'\nADV:(.*?)\nADV:',
      ],
      ['ce',
      r'{}(.*?){}'.format(re_final_ce,re_final_ce)
      ],
      ['to',
      r'{}(.*?){}'.format(re_final_to,re_final_to)
      ],
      ['pi',
      r'{}(.*?){}'.format(re_final_pi,re_final_pi)
      ],
      ['ro',
      r'{}(.*?){}'.format(re_final_ro,re_final_ro)
      ],
      ['ma',
      r'{}(.*?){}'.format(re_final_ma,re_final_ma)
      ],
      ['pa',
      r'\nPROCESSO:(.*?)\nPROCESSO:',
      ],
      ['go',
      r'(\n\s*?PROTOCOLO\s*?\:|\nNR\. PROTOCOLO|\n\s*?PROCESSO\s*?\:)(.*?)(\n\s*?PROTOCOLO\s*?\:|\nNR\. PROTOCOLO|\n\s*?PROCESSO\s*?\:)'
      ],
      ['ap',
      r'(\nDISTRIBUIÇÃO|\nN. do processo\:|\nVARA\:)(.*?)(\nDISTRIBUIÇÃO|\nN. do processo\:|\nVARA\:)'
      ],
      ['rr',
      r'\n\d{3} - (?=\d{7})(.*?)\n\d{3} - (?=\d{7})',
      ],
      ['am',
      r'{}(.*?){}'.format(re_final_am,re_final_am)
      ],
      ['pr',
      r'\n\d{1,4} \. Processo[\:/](.*?)\n\d{1,4} \. Processo[\:/]'
      ],
      ['trf2',
      r'{}(.*?){}'.format(re_final_trf4,re_final_trf4)
      ],
      ['sc',
      r'{}(.*?){}'.format(re_final_sc,re_final_sc)
      ],
      ['df',
      r'\n\d{3}\. (?=\d{4})(.*?)\d{3}\. (?=\d{4})'
      ],
      ['mg',
      r'\n\d{5} - (?=\d{7})(.*?)\n\d{5} - (?=\d{7})'
      ],
      ['rj',
      r'\nProc\.(.*?)\nProc\.'
      ],
      ['mt',
      r'(\nProtocolo|\nIntimação)(.*?)(\nProtocolo|\nIntimação)'
      ],
      ['pe',
      r'(\nProtocolo|\nProcesso)(.*?)(\nProtocolo|\nProcesso)'
      ],
      ['ba',
      r'(DIREITO (?=\d{7}-\d{2}\.)|\nIntimação)(.*?)(DIREITO (?=\d{7}-\d{2}\.)|\nIntimação)'
      ],
      ['trf5',
      r'(\nPROTOCOLO N|\n\d{4}\s*?\.\s*Processo)(.*?)(\nPROTOCOLO N|\n\d{4}\s*?\.\s*Processo)'
      ],
      ['se',
      r'(\nNO\. PROCESSO|\nNO\. ACORDÃO|\nPROC\.\:)(.*?)(\nNO\. PROCESSO|\nNO\. ACORDÃO|\nPROC\.\:)'
      ]
  ]

for a in arqs_i:
	for d in diarios:
		nome_arq = re.search(r""+d[0]+"\d+\.txt",a)
		if nome_arq != None:
			# definir forma de processamento dos diários para inserção na base após transformação do diário em txt
			break