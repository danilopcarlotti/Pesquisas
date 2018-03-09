import re

def busca(re_exp,text,ngroup=1,args=None):
	if args:
		result = re.search(re_exp,text,args)
	else:
		result = re.search(re_exp,text)
	if result:
		result = result.group(ngroup)
	else:
		result = ''
	return result.strip()