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
URL = ['https://www.primeabgb.com/online-price-reviews-india/zotac-gaming-geforce-rtx-3080-trinity-10gb-gddr6x-graphic-card-zt-a30800d-10p/',
       'https://www.primeabgb.com/online-price-reviews-india/gigabyte-geforce-rtx-3080-eagle-oc-10g-10gb-graphic-card-gv-n3080eagle-oc-10gd/'
       'https://www.primeabgb.com/online-price-reviews-india/asus-geforce-gtx-1050-ti-cerberus-gtx1050ti-o4g-4gb-graphic-card/',
       'https://www.primeabgb.com/online-price-reviews-india/zotac-gaming-geforce-rtx-3080-trinity-oc-10gb-gddr6x-graphic-card-zt-a30800j-10p/',
       'https://www.primeabgb.com/online-price-reviews-india/galax-geforce-rtx-3080-sg-1-click-oc-10gb-gddr6x-graphic-card-38nwm3md99nn/',
       'https://www.primeabgb.com/online-price-reviews-india/inno3d-geforce-rtx-3080-ichill-x3-10gb-gddr6x-graphic-card-c30803-106xx-1810va37/',
       'https://www.primeabgb.com/online-price-reviews-india/msi-geforce-rtx-3070-ventus-2x-oc-8gb-gddr6-graphic-card/',
       'https://www.primeabgb.com/online-price-reviews-india/colorful-igame-geforce-rtx-3070-ultra-oc-v-8gb-gddr6-256-bit-gaming-graphics-card/']
       
postUrl = 'https://maker.ifttt.com/trigger/Crypto_Alert/with/key/your_key'
postSmsUrl = 'https://maker.ifttt.com/trigger/Crypto_sms_alert/with/key/your_key'
inStock = False

try:
    while not inStock:
        f = open("primeabgblog.txt", "a")
        for link in URL:           
            # Page content from Website URL
            page = requests.get( link )
            print(link.split('/')[-2].replace('-',' ').replace('.html','').upper())
            f.write(link.split('/')[-2].replace('-',' ').replace('.html','').upper())
            
            # parse html content
            soup = BeautifulSoup( page.content , 'html.parser')
            
            stock_info = soup.find_all('p', class_ = 'stock out-of-stock')
            if(not stock_info):
                inStock = True
                requests.post(postUrl)
                requests.post(postSmsUrl+"?value1="+link)
                driver = webdriver.Firefox('./')
                driver.get(link)
                driver.find_element_by_name('add-to-cart').click()
                driver.maximize_window()
        
            now = datetime.now()
            if(inStock):
                print("Availability:  In Stock", now)          
                f.write("Availability:  In Stock" + str(now) + "\n")
                break
            else:
                print("Availability:  Out of Stock", now)          
                f.write("Availability:  Out of Stock" + str(now) + "\n")
                
        countdown(random.randrange(60,360))
        print("\n")
        f.write("\n")
        f.close()

except (KeyboardInterrupt or inStock):
    print("Done!!")
