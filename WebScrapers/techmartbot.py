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
URL = ['https://techmartunbox.com/product/asus-dual-rtx-3070-oc-8gb-gaming-graphics-card/',
       'https://techmartunbox.com/product/msi-rtx-3070-ventus-3x-oc-8gb-graphics-card-2/',
       'https://techmartunbox.com/product/adata-xpg-gammix-d30-8gb-8gbx1-ddr4-3000mhz/',
       'https://techmartunbox.com/product/inno3d-rtx-3070-twin-x2-oc-8gb-graphics-card/',
       'https://techmartunbox.com/product/galax-rtx-3080-sg-1-click-oc-10gb-graphics-card/',
       'https://techmartunbox.com/product/msi-rtx-3080-ventus-3x-oc-10gb-graphics-card/']
       
postUrl = 'https://maker.ifttt.com/trigger/Crypto_Alert/with/key/your_key'
postSmsUrl = 'https://maker.ifttt.com/trigger/Crypto_sms_alert/with/key/your_key'
inStock = False

try:
    while not inStock:
        f = open("techmartlog.txt", "a")
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
