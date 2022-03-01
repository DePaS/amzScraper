from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from PyQt5 import QtGui
from pathlib import Path
import webbrowser
import sys

def window():


    #####################################################################################################################################
    # first function
    #####################################################################################################################################
    def scrap_products():
        user_input_url = win.textbox.text()
        print(user_input_url)
        try:
            options = Options()
            options.add_argument('--headless')
            options.add_argument("--no-sandbox");
            options.add_argument("--disable-gpu");
            options.add_argument("--disable-crash-reporter");
            options.add_argument("--disable-extensions");
            options.add_argument("--disable-in-process-stack-traces");
            options.add_argument("--disable-logging");
            options.add_argument("--disable-dev-shm-usage");
            options.add_argument("--log-level=3");
            options.add_argument("--output=/dev/null");
            driver = webdriver.Chrome(options=options)
            #user_url = input('Enter the desired link:')
            user_url = user_input_url
            driver.get(user_url)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            avoid = '/gp' #/video/ssoredirect/' or '/gp/slredirect/'
            all_links = soup.find_all('a', {"class": "a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"})
            pages = soup.find('span', {"class": "s-pagination-item s-pagination-disabled"}).getText()
            x = 1
            global num_links
            num_links = 1
            open('links.txt', 'w').close()
            #print("file cleared and number of pages: " + pages)
            #print('cosa sto trovando: '  + str(all_links))
            if len(all_links) != 0:
                for x in range(1, int(pages) + 1):
                    user_url += "&page=" + str(x)
                    driver.get(user_url)
                    soup2 = BeautifulSoup(driver.page_source, 'html.parser')
                    #print("page number: " + str(x))
                    for a in soup2.find_all('a', {"class": "a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"}):
                        if avoid not in a['href']: #inserisco tutti i link nel file, tranne i link sponsorizzati o pubblicitari
                            url_finale = a['href'].split('/ref', 1)[0]
                            f = open('links.txt', 'a')
                            f.write('https://www.amazon.it' + url_finale + '/?smid=A11IL2PNWYJU7H' + '\r\n')
                            print("Found the URL:", url_finale)
                            num_links += 1
                    x += 1
                #text2
                print(num_links)
                text2.setText('Links found are: ' + str(num_links))# + num_of_links)
                text2.setStyleSheet('color: red;')
            else:
                print('the link is wrong or not an Amazon link')
        except:
            print('please enter a valid url')
            text2.setText('Please enter a valid Amazon.it url')# + num_of_links)
            text2.setStyleSheet('color: red;')
        
    #####################################################################################################################################
    # second function
    #####################################################################################################################################
    def max_tetto():
        user_input_max_budget = win.textbox2.text()
        print(user_input_max_budget)
        global isError 
        isError = True
        try:
            global user_input
            #user_input = input("inserisci un numero:")
            user_input = user_input_max_budget
            user_input = user_input.replace(',', '.')
            global max_price
            max_price = float(user_input)
            global max_budget
            max_budget = True
            print(user_input_max_budget)
            return max_budget
        except ValueError:
            print(user_input_max_budget)
            if user_input.isspace() or not user_input:
                max_budget = False
                print(user_input_max_budget)
                return max_budget
            else:
                print(user_input_max_budget + 'piu')
                text2.setStyleSheet('color: red;')
                text2.setText('Please return an integer or float')
                isError = False
                return isError
                #return max_tetto()
    
    #####################################################################################################################################
    # third function
    #####################################################################################################################################
    def check_links():
        text2.setStyleSheet('color: red;')
        text2.setText('This might take a while please standby')
        options = Options()
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
        txt = Path('links.txt').read_text()
        txt = txt.replace('\n', '')
        open('amazon_products.txt', 'w').close()
        max_tetto()
        if isError:
            while txt != '':
                app.processEvents()
                link = txt.split("?smid=A11IL2PNWYJU7H", 1)[0]  # prendo il link valido
                rest = txt.split("?smid=A11IL2PNWYJU7H", 1)[1]  # prendo tutto il resto meno il primo link
                link = link + "?smid=A11IL2PNWYJU7H"
                txt = rest
                try:
                    driver.get(link)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    isAmazon = soup.find_all("div", {"class": "tabular-buybox-text a-spacing-none"})
                    compareAmazon = isAmazon[1].findChild().getText()
                    if compareAmazon == 'Amazon':
                        if max_budget:
                            is_price_whole = soup.find_all("span", {"class": "a-price-whole"})
                            is_price_decimal = soup.find_all("span", {"class": "a-price-fraction" })
                            compare_price_whole = is_price_whole[0].getText()
                            compare_price_whole_total = compare_price_whole.split(',', 1)[0]
                            if len(compare_price_whole_total) > 3:
                                compare_price_whole_first = compare_price_whole_total.split('.', 1)[0]
                                compare_price_whole_second = compare_price_whole_total.split('.', 1)[1]
                                compare_price_whole_total = compare_price_whole_first + compare_price_whole_second
                            compare_price_decimal = is_price_decimal[1].getText()
                            compare_price = compare_price_whole_total + '.' + compare_price_decimal
                            compare_price = float(compare_price) 
                            if compare_price <= max_price:
                                f = open('amazon_products.txt', 'a')
                                f.write(link + '\r\n')
                            else:
                                print('il prezzo è troppo alto')
                        else:
                            f = open('amazon_products.txt', 'a')
                            f.write(link + '\r\n')
                            print('vendor is Amazon')
                    else:
                        print('vendor is not Amazon: ' + compareAmazon)
                except:
                    print('Link is not valid')
            else:
                text2.setText('Scraping done, results are in the amazon_products.txt')
                driver.quit()
                print("There is no link to check")

    #####################################################################################################################################
    # fourth function
    #####################################################################################################################################

    def is_integer(): 
        link_open = win.textbox3.text()
        #link_open = input('Input how many links to open, leave blank for all:')
        global link_num
        link_num = 9999
        global limited
        try:
            link_num = int(link_open)
            print(link_num)
            limited = True
            return limited
        except:
            if link_open.isspace() or not link_open:
                limited = True
                return limited
            else: 
                limited = False
                text2.setStyleSheet('color: red;')
                text2.setText('Please return an integer or leave it blank to open all links')
                win.textbox3.setText('')
                return limited

    #####################################################################################################################################
    # fifth function
    #####################################################################################################################################
    def open_links():
        text2.setText('')
        txt = Path('amazon_products.txt').read_text()
        txt = txt.replace('\n', '')
        x = 1
        is_integer()
        if limited:
            while txt != '':
                    if x > link_num:
                        if link_num == 0:
                            text2.setStyleSheet('color: red;')
                            text2.setText("You can't input 0")
                            win.textbox3.setText('')
                        break
                    print('link numero: ' + str(x))
                    link = txt.split("?smid=A11IL2PNWYJU7H", 1)[0]  # prendo il link valido
                    rest = txt.split("?smid=A11IL2PNWYJU7H", 1)[1]  # prendo tutto il resto meno il primo link
                    link = link + "?smid=A11IL2PNWYJU7H"
                    txt = rest
                    webbrowser.open(link)
                    x += 1
            else:
                print('vuoto no link to open')
        else:
            print('no link to open')
    #####################################################################################################################################
    # sixth function
    #####################################################################################################################################

    app = QApplication(sys.argv)
    win = QMainWindow()
    #win.setGeometry(660, 390, 600, 300)
    win.setFixedSize(600, 300)
    win.setWindowTitle("Amazon scraper")
    win.setWindowIcon(QtGui.QIcon('amazon.ico'))
    wid = QtWidgets

    # linkbox
    win.textbox = QLineEdit(win)
    win.textbox.move(80, 40)
    win.textbox.resize(440, 30)
    global user_input_url
    
    #text1
    text1 = wid.QLabel(win)
    text1.setText('Paste desired Amazon.it link here:')
    text1.move(80, 10)
    text1.resize(300, 30)

    #text2
    text2 = wid.QLabel(win)
    #text2.setText('SAMPLE TEXT ERROR')
    text2.move(78, 145)
    text2.resize(400, 30)

    #text3
    text3 = wid.QLabel(win)
    text3.setText('Input max budget filter or leave blank')
    text3.move(100, 140)
    text3.resize(300, 30)
    text3.setStyleSheet('color: gray; font-size: 10px;')

    #text4
    text4 = wid.QLabel(win)
    text4.setText('Return an integer or leave it blank to open all links')
    text4.move(325, 140)
    text4.resize(300, 30)
    text4.setStyleSheet('color: gray; font-size: 10px;')

    #button start scraping
    b1 = wid.QPushButton(win)
    b1.setText('Start Scraping')
    b1.move(100, 80)
    b1.resize(130, 30)
    b1.clicked.connect(scrap_products)

    #button scrap amazon vendor
    b2 = wid.QPushButton(win)
    b2.setText('Sold by Amazon')
    b2.move(155, 120)
    b2.resize(130, 30)
    b2.clicked.connect(check_links)

    #button open links
    b3 = wid.QPushButton(win)
    b3.setText('Open links')
    b3.move(355, 120)
    b3.resize(130, 30)
    b3.clicked.connect(open_links)

    #input b3 
    win.textbox3 = QLineEdit(win)
    win.textbox3.move(325, 125)
    win.textbox3.resize(20, 20)

    #input b2 
    win.textbox2 = QLineEdit(win)
    win.textbox2.move(100, 125)
    win.textbox2.resize(50, 20)

    win.show()
    sys.exit(app.exec_())

window()