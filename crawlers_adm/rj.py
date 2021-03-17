import os
import re
import sys
import time
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
from download_path import path

sys.path.append(os.path.dirname(os.getcwd()))
# from common.recursive_folders import recursive_folders
from crawlers.crawlerJus import crawlerJus


def download_decisoes_smf():
    for counter in range(1, 3811, 10):
        print(counter)
        try:
            req = urllib.request.Request(
                "http://smfweb.rio.rj.gov.br/results.aspx?k=direito&start1={}".format(
                    counter
                ),
                headers={"User-Agent": "Mozilla/5.0"},
            )
            html = urllib.request.urlopen(req, timeout=30).read()
            pag = BeautifulSoup(html, "html.parser")
            links_baixar = []
            for l in pag.find_all("a", href=True):
                if re.search(r"\.pdf", l["href"]):
                    links_baixar.append(l["href"])
            for link_ in links_baixar:
                response = urllib.request.urlopen(link_, timeout=60)
                file = open(path + "/RJ/" + link_.split("/")[-1], "wb")
                file.write(response.read())
                file.close()
            time.sleep(2)
        except Exception as e:
            print(e)
            break


if __name__ == "__main__":
    download_decisoes_smf()
