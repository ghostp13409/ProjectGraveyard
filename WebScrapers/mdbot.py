# Import Module
from bs4 import BeautifulSoup
import requests
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import random
from timer import *

# Website URL
URL = ['https://mdcomputers.in/colorful-igame-geforce-rtx-3080-ultra-oc-10g-v.html',
       'https://mdcomputers.in/asus-tuf-rtx3080-10g-gaming.html'
       'https://mdcomputers.in/asus-gt-710-2gb-ddr5-90yv0al3-m0ia00.html']
       
postUrl = 'https://maker.ifttt.com/trigger/Crypto_Alert/with/key/your_key'
postSmsUrl = 'https://maker.ifttt.com/trigger/Crypto_sms_alert/with/key/your_key'
inStock = False

try:
    while not inStock:
        f = open("mdlog.txt", "a")
        for link in URL:           
            # Page content from Website URL
            page = requests.get( link )
            print(link.split('/')[-1].replace('-',' ').replace('.html','').upper())
            f.write(link.split('/')[-1].replace('-',' ').replace('.html','').upper())
            
            # parse html content
            soup = BeautifulSoup( page.content , 'html.parser')
            
            stock_info = soup.find_all('div', class_ = 'stock')
            if(stock_info[0].text=="Availability:  In Stock"):
                inStock = True
                requests.post(postUrl)
                requests.post(postSmsUrl+"?value1="+link)
                driver = webdriver.Firefox('./')
                driver.get(link)
                driver.find_element_by_id('button-checkout').click()
                driver.maximize_window()
        
            now = datetime.now()
            print(stock_info[0].text, now)           
            f.write(stock_info[0].text + " " + str(now) + "\n")
        countdown(random.randrange(60,360))
        print("\n")
        f.write("\n")
        f.close()

except (KeyboardInterrupt or inStock):
    print("Done!!")
