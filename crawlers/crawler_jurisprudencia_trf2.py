import time, ssl, os, urllib.request, subprocess, urllib.parse, urllib.error, http.cookiejar
from bs4 import BeautifulSoup
from crawler_jurisprudencia_tj import crawler_jurisprudencia_tj
import requests

class crawler_jurisprudencia_trf2():
    """Crawler especializado em retornar textos da jurisprudência de segunda instância de Maranhão"""
    def __init__(self):
        crawler_jurisprudencia_tj.__init__(self)
        ssl._create_default_https_context = ssl._create_unverified_context 

    def download_diario_retroativo(self):
        cookies = {
            'ASP.NET_SessionId': 'ducbpu55dmctl145abeqmafg',
        }

        headers = {
            'Connection': 'keep-alive',
            'Cache-Control': 'no-cache',
            'Origin': 'http://dje.trf2.jus.br',
            'X-MicrosoftAjax': 'Delta=true',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': '*/*',
            'Referer': 'http://dje.trf2.jus.br/DJE/Paginas/Externas/ListaDiarios.aspx',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.9,pt-BR;q=0.8,pt;q=0.7,es-ES;q=0.6,es;q=0.5,la;q=0.4',
        }

        data = {
            'ctl00$ScriptManager': 'ctl00$ContentPlaceHolder$ctrListaDiarios$UpdatePanel1|ctl00$ContentPlaceHolder$ctrListaDiarios$FiltraPesquisaDiarios$btnFiltrar',
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__LASTFOCUS': '',
            '__EVENTVALIDATION': '/wEW2wEC2rPkfgK97+StDwKU4OG5CQLMuv/zCQK8gbrEBAKw7pCqCAKs7pCqCAK37tCpCAK37typCAKs7q3jDgKIluKLDgKHxt2UBQL7l4TYBwKlsuziDwKPjaXHCAKOja3kDAKGmbzlBQL9o6r8BgL9o76hDgL9o4KGCQL9o5ZrAv2j+s8LAv2jzrQDAv2j0pkKAv2jpv4FAv2jyhUC/aPe+gsC2MzM0QwC2MzQtgQC2Mykmw8C2MyIwAYC2MycpQ4C2MzgiQkC2Mz0bgLYzNjTCwLYzOzqBgLYzPDPAQK31e6mAwK31fKLCgK31cbwBQK31arVDAK31b66BAK31YKfDwK31ZbEBgK31fqoDgK31Y7ADAK31ZKlBAKS/oC8CQKS/pRhApL++MULApL+zKoDApL+0I8KApL+pPQFApL+iNkMApL+nL4EApL+oNUCApL+tLoKArmUwH0CsKSvoAQCsaSnAwK5sLaCCQLCiqCbCgLCirTGAgLCiojhBQLCipyMDALCivCoBwLCisTTDwLCitj+BgLCiqyZCQLCisDyDALCitSdBwLn5cY2Aufl2tEIAuflrvwDAuflgqcKAufllsICAufl6u4FAufl/okMAufl0rQHAufl5o0KAufl+qgNAoj85MEPAoj8+OwGAoj8zJcJAoj8oDICiPy03QgCiPyI+AMCiPycowoCiPzwzwICiPyEJwKI/JjCCAKt14rbBQKt156GDAKt1/KiBwKt18bNDwKt19roBgKt166TCQKt14I+Aq3XltkIAq3XqrIOAq3Xvt0GAoa9ypoMArG0i6QMArW0y6cMArS0y6cMAre0y6cMAra0y6cMArG0y6cMApP1rPALAoHJg7QKAuu/kMYOAvGR3v0GApuaoe0KAuu/jOQMAs3x2b4DAp+anUgC67+oig4C6YjmgwYCmpqZlAsC67+ksA4C2ZTixAYCmpqV9wQC67+gzg8C3aSM+QwCmZrx6Q0CseqRygoClbyang0CyqWftAoC/ZCqwQYCh734qwICyqWjlgoCqY2u+AECh73c0AoCyqXHgAsClaniugcChb2A/gUCyqWr2goCjZWm+gQCiL3kkgwCyqXPvAkCqY/6vAICir3otwMC27zKjwQCp+au3QkChv/k4wkCmb+58AUC34K9uw4C2Iq+rAoCmb/90g0Cj4LzuAEC2IrivgUCmb+BVAKy64a3CgKRysWhCwKZv8XsCgLDxaTaCgKRyqnGCAKZv6neDwKShJ2hCAKC3+z4DgLGioDdBALPgst1Ao2bqfEHAqGg57ENApKR8Y4KAo2bvfYOAom3jYcMAv61/K8CAo2bsecIAt2N+t0CAuPMsowJAo2bxcQPAvHVtPYPAv61xJQJAo2bufALAuX3qtgLAuPMmq0GAob6kuAIAuLWz90GAob/0IgBAqrgqcANAv2S7kMCoejPwwoCquDtogUCrZKkwQMCoejz1QUCquDxowgC0Pu3vwwC2qfXuAsCquC1vAIC4dXV4gwC2qe73QgCquCZrgcCsJTOqQoCy7z+jw8Cz/e8YALmxffvDgKG0vi4CwK4/Ow3Asa+m6cEAobSjL4CAqCTk40PArLjpsgMAobSgK8MAvTp/+MFApf63KQDAobSlIwDAoiyuvwCArLj7qwDAobSiLgPAvzTsN4OApf6xEUCvKaY4AcCqpfE/QwChv+8rQgC3Yz02A8CwZWRnQkCoMLJjg4CxbmOhgKRE0DCAVOGp/uDxHt1x28ddZFwbg==',
            'ctl00$ContentPlaceHolder$ctrListaDiarios$FiltraPesquisaDiarios$ddlAreaJudicial': '4',
            'ctl00$ContentPlaceHolder$ctrListaDiarios$FiltraPesquisaDiarios$tbxDataInicial': '04/01/2011',
            'ctl00$ContentPlaceHolder$ctrListaDiarios$FiltraPesquisaDiarios$meeDataInicial_ClientState': '',
            'ctl00$ContentPlaceHolder$ctrListaDiarios$FiltraPesquisaDiarios$tbxDataFinal': '31/12/2015',
            'ctl00$ContentPlaceHolder$ctrListaDiarios$FiltraPesquisaDiarios$meeDataFinal_ClientState': '',
            'ctl00$ContentPlaceHolder$ctrListaDiarios$FiltraPesquisaDiarios$ddlRegistrosPaginas': '100',
            'ctl00$ContentPlaceHolder$ctrListaDiarios$FiltraPesquisaDiarios$btnFiltrar': 'Pesquisar'
        }

        link = 'http://dje.trf2.jus.br/DJE/Paginas/Externas/ListaDiarios.aspx'
        response = requests.post(link, headers=headers, cookies=cookies, data=data)
        arq = open('links_trf2.txt','w')
        arq.write(str(response.text))
        arq.close()

    def parse_links(self):
        texto = '\n'.join([line for line in open('links_trf2.txt','r')])
        soup = BeautifulSoup(texto,'lxml')
        for script in soup(["script", "style"]):
            script.extract()
        arq = open('texto_links_trf2.txt','w')
        arq.write(soup.get_text())
        arq.close()

if __name__ == '__main__':
	c = crawler_jurisprudencia_trf2()
	# try:
	# 	c.download_trf3()
	# except Exception as e:
	# 	print(e)

	c.parse_links()