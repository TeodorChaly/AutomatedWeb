from selenium import webdriver
import time

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

PATH = "C:\Go\chromedriver.exe"
driver = webdriver.Chrome(PATH)

driver.get("http://www.google.com")
def accept_cookies():
    accept_button = driver.find_element(By.ID, 'L2AGLb')
    accept_button.click()
def search():
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys("webdriver")
    search_box.send_keys(Keys.RETURN)

accept_cookies()
search()



time.sleep(10)

driver.close()
driver.quit()