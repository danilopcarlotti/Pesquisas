import os
import re
import sys
import time
from selenium import webdriver
from download_path import path

sys.path.append(os.path.dirname(os.getcwd()))
# from common.recursive_folders import recursive_folders
from crawlers.crawlerJus import crawlerJus


def download_decisoes_tit():
    crawler = crawlerJus()
    driver = webdriver.Chrome(crawler.chromedriver)
    for i in range(1, 3):
        driver.get(
            "https://www.fazenda.sp.gov.br/VDTIT/ConsultarVotos.aspx?instancia={}".format(
                i
            )
        )
        if input("Faça a pesquisa e aperte um numero:"):
            pass
        next_page = True
        counter = 11
        while next_page:
            for counter_p in range(10):
                for index in range(3, 9):
                    script_download = 'javascript:WebForm_DoPostBackWithOptions(new WebForm_PostBackOptions("ctl00$ConteudoPagina$gdvEntidade$ctl0{}$lnkArquivo", "", true, "", "", false, true))'.format(
                        index
                    )
                    driver.execute_script(script_download)
                    time.sleep(2)
                script_counter = "javascript:__doPostBack('ctl00$ConteudoPagina$gdvEntidade','Page${}')".format(
                    counter_p
                )
                driver.execute_script(script_counter)
                time.sleep(5)
            script_str = "javascript:__doPostBack('ctl00$ConteudoPagina$gdvEntidade','Page${}')".format(
                counter // 10
            )
            try:
                driver.execute_script(script_str)
                time.sleep(2)
                counter += 10
            except:
                next_page = False
            break


if __name__ == "__main__":
    download_decisoes_tit()
