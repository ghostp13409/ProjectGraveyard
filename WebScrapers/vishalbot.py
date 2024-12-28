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
URL = ['https://www.vishalperipherals.in/index.php?route=product/product&product_id=2809']
       
postUrl = 'https://maker.ifttt.com/trigger/Crypto_Alert/with/key/your_key'
postSmsUrl = 'https://maker.ifttt.com/trigger/Crypto_sms_alert/with/key/your_key'
inStock = False

try:
    while not inStock:
        f = open("vishallog.txt", "a")
        for link in URL:           
            # Page content from Website URL
            page = requests.get( link )
            print("GIGABYTE GEFORCE RTX 3080 10GB VISION OC")
            f.write("GIGABYTE GEFORCE RTX 3080 10GB VISION OC")
            
            # parse html content
            soup = BeautifulSoup( page.content , 'html.parser')
            
            stock_info = soup.find_all('li', class_ = 'product-stock out-of-stock')
            if(not stock_info):
                inStock = True
                requests.post(postUrl)
                requests.post(postSmsUrl+"?value1="+link)
                driver = webdriver.Firefox('./')
                driver.get(link)
                driver.find_element_by_class_name('btn-text').click()
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
