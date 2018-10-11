import urllib.request, json, pandas as pd, time

url = 'https://www.bec.sp.gov.br/BEC_API/API/pregao_encerrado/OC_encerrada/20090101/20181008/%s'
df = pd.read_excel('/home/danilo/Downloads/OCs_para query Pregoeiros.xlsx')
minimo = 53071
contador = 0
for index, row in df.iterrows():
	if contador < minimo:
		contador += 1
	else:
		try:
			req = urllib.request.Request(url % (row['Numero da OC'],))
			r = urllib.request.urlopen(req,timeout=3).read()
			filejson = open('/home/danilo/Downloads/BEC_json/dados_bec_sp_%s.json' % (row['Numero da OC'],), 'w')
			json.dump(json.loads(r.decode('utf-8')), filejson, ensure_ascii=False)
			time.sleep(0.5)
		except Exception as e:
			print(e)
			print(row['Numero da OC'])


