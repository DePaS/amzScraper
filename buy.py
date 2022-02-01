import bs4
from urllib.request import urlopen  # for Python 3: from urllib.request import urlopen
from bs4 import BeautifulSoup

userUrl = input('Enter the desired link:')
soup = BeautifulSoup(urlopen(userUrl), 'html.parser')
avoid = '/gp/video/ssoredirect/'
allLinks = soup.find_all('a', {"class": "a-link-normal s-link-style a-text-normal"})
pages = soup.find('span', {"class": "s-pagination-item s-pagination-disabled"}).getText()
x = 1
open('links.txt', 'w').close()
print("file cleared and number of pages: " + pages)
if len(allLinks) == 0:
    print('the link is wrong or not an Amazon link')
else:
    for x in range(1, int(pages) + 1):
        soup2 = BeautifulSoup(urlopen(userUrl + "&page=" + str(x)), 'html.parser')
        print("page number: " + str(x))
        for a in soup2.find_all('a', {"class": "a-link-normal s-link-style a-text-normal"}):
            if avoid not in a['href']:
                f = open('links.txt', 'a')
                f.write('https://www.amazon.it' + a['href'] + '/?smid=A11IL2PNWYJU7H' + '\r\n')
                print("Found the URL:", a['href'])
        x += 1
