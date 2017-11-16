from crawler_jurisprudencia_tjma import crawler_jurisprudencia_tjma
from selenium import webdriver

c = crawler_jurisprudencia_tjma()
driver = webdriver.Chrome(c.chromedriver)