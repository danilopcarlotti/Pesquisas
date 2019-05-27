import re

def busca(re_exp,text,ngroup=1,args=None):
	if args:
		result = re.search(re_exp,text,flags=args)
	else:
		result = re.search(re_exp,text)
	try:
		result = result.group(ngroup).strip().replace('\\','').replace('/','').replace('"','')
	except:
		result = ''
	return result