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


def download_decisoes_tarf():
    crawler = crawlerJus()
    driver = webdriver.Chrome(crawler.chromedriver)
    driver.get("http://www.legislacao.sefaz.rs.gov.br/Site/Search.aspx?a=&CodArea=4")
    ini_link = "http://www.legislacao.sefaz.rs.gov.br/Site/"
    xpath_next = '//*[@id="LinkNext"]'
    if input("Selecione direito"):
        pass
    counter = 0
    while True:
        try:
            html = driver.page_source
            pag = BeautifulSoup(html, "html.parser")
            links_baixar = []
            for l in pag.find_all("a", href=True):
                if re.search(r"javascript\:goDocument\(\d+,''", l["href"]):
                    numeros = re.search(r"\((\d+)\,", l["href"])
                    if numeros:
                        links_baixar.append(
                            "http://www.legislacao.sefaz.rs.gov.br/Site/Document.aspx?inpKey={}&inpCodDispositive=&inpDsKeywords=direito".format(
                                numeros.group(1)
                            )
                        )
            for link_ in links_baixar:
                req = urllib.request.Request(
                    link_, headers={"User-Agent": "Mozilla/5.0"}
                )
                html = urllib.request.urlopen(req, timeout=30).read()
                pag = BeautifulSoup(html, "html.parser")
                for l in pag.find_all("frame", {"id": "FrameDoc"}):
                    link_ = ini_link + l["src"]
                    req_ = urllib.request.Request(
                        link_, headers={"User-Agent": "Mozilla/5.0"}
                    )
                    html_ = urllib.request.urlopen(req_, timeout=30).read()
                    soup = BeautifulSoup(html_, "html.parser")
                    for script in soup(["script", "style"]):
                        script.extract()
                    text = re.sub(r"\s+", " ", soup.get_text())
                    arq = open(
                        str("{}/RS/{}.txt".format(path, counter)), "w", encoding="utf-8"
                    )
                    arq.write(text)
                    arq.close()
                    counter += 1
            time.sleep(3)
            driver.find_element_by_xpath(xpath_next).click()
            time.sleep(3)
        except Exception as e:
            print(e)
            break


if __name__ == "__main__":
    download_decisoes_tarf()
