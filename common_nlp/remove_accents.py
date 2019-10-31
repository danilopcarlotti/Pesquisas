def remove_accents(texto):
	dicionario_acentos = {'Á':'A','Ã':'A','À':'A','á':'a','ã':'a','à':'a','É':'E','é':'e','Í':'I','í':'i',
	'Ó':'O','ó':'o','Õ':'O','õ':'o','Ú':'U','ú':'u','ç':'c','Ç':'Ç',';':'',',':'','/':'','\\':'','{':'','}':''
	,'(':'',')':'','-':'','_':''}
	texto = str(texto)
	for k,v in dicionario_acentos.items():
		texto = texto.replace(k,v)
	return texto
