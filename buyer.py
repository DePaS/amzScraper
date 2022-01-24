import selenium
import selenium.webdriver as webdriver
import time
from time import sleep
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import InvalidArgumentException


options = Options()
options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
options.firefox_profile = r'C:\Users\depas\AppData\Roaming\Mozilla\Firefox\Profiles\3lojtj6a.default-release'
options.executable_path = r'C:\Users\depas\AppData\Local\Programs\Python\Python310\geckodriver.exe'
options.headless = True

firefox = webdriver.Firefox(options=options)
x = 1
y = 1
index = 1
userUrl = input('Enter the desired link:')
#firefox.get('https://www.amazon.it/s?i=computers&bbn=460090031&rh=n%3A460090031%2Cp_36%3A1631637031&page=' + '&page=' + str(x))
firefox.get(userUrl + '&page=' + str(x))
for index in range(1, 40):
    try:
        pages = firefox.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div[1]/div/span[3]/div[2]/div[' + str(index) + ']/span/div/span/span[4]').text
        break
    except NoSuchElementException:
        index += 1
        pass

lastPage = int(pages) + 1
for x in range(1, int(lastPage)):
    #firefox.get('https://www.amazon.it/s?i=computers&bbn=460090031&rh=n%3A460090031%2Cp_36%3A1631637031&page=' + '&page=' + str(x))
    firefox.get(userUrl + '&page=' + str(x))
    print('pagina: ' + str(x))
    for y in range(1, 32):
                try:
                    vendor = firefox.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div[1]/div/span[3]/div[2]/div[' + str(y) + ']/div/span/div/div/div[2]/div[1]/h2/a').get_attribute('href')
                except NoSuchElementException:
                    try:
                        vendor = firefox.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div[1]/div/span[3]/div[2]/div[' + str(y) + ']/div/span/div/div/div/div/div[2]/div[1]/h2/a')
                        vendor = 'sponsor'
                        print(vendor + ' - ' + str(y))
                        pass
                    except NoSuchElementException:
                        vendor = 'empty'
                        pass

                if vendor != 'sponsor' and vendor != 'empty':
                    print(y)
                    f = open('links.txt', 'a')
                    link = vendor.split("ref=", 1)[0]
                    f.write(link + '?smid=A11IL2PNWYJU7H' + '\r\n')
                    print(link)
                    y += 1

                    x += 1
