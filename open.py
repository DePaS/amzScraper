import bs4
from urllib.request import urlopen
from bs4 import BeautifulSoup
from pathlib import Path

txt = Path('links.txt').read_text()
txt = txt.replace('\n', '')

while txt != '':
    link = txt.split("?smid=A11IL2PNWYJU7H", 1)[0] #prendo il link valido
    rest = txt.split("?smid=A11IL2PNWYJU7H", 1)[1] #prendo tutto il resto meno il primo link
    txt = rest
    soup = BeautifulSoup(urlopen(link), 'html.parser')
    isAmazon = soup.find("div",{"class": "tabular-buybox-text a-spacing-none"}).findChild().getText()
    if isAmazon == 'Amazon':
        f = open('working.txt', 'a')
        f.write(link + '?smid=A11IL2PNWYJU7H' + '\r\n')
else:
    print("There is no link to check")
