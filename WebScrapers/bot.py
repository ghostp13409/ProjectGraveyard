from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Firefox('./')
driver.get("https://mdcomputers.in/cooler-master-mm711-rgb-ambidextrous-mm-711-kkol1.html")
#print(driver.page_source)
driver.find_element_by_id('button-checkout').click()
driver.maximize_window()