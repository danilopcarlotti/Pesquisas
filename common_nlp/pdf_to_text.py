from tikapp import TikaApp
import os
import subprocess
import sys
sys.path.append(os.path.dirname(os.getcwd()))
from common.recursive_folders import recursive_folders

class pdf_to_text():
    """Converts pdf to text with TikaApp"""
    def __init__(self):
        pass
    
    def convert_Tika(self,fname):
        tika_client = TikaApp(file_jar=os.getcwd()+'/tika-app-1.20.jar')
        return tika_client.extract_only_content(fname)

if __name__ == '__main__':
    path = sys.argv[1]
    p = pdf_to_text()
    r = recursive_folders()
    lista_arquivos = set(r.find_files(path))
    for arq in lista_arquivos:
        if arq[-3:] == 'pdf' and arq.replace('pdf','txt') not in lista_arquivos:
            print(arq)
            texto = p.convert_Tika(arq)
            arq = open(arq.replace('pdf','txt'),'w')
            arq.write(texto)
            arq.close()
