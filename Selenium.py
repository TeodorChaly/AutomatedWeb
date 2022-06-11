from selenium import webdriver
import time

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

PATH = "C:\Go\chromedriver.exe"
option = webdriver.ChromeOptions()
#option.headless = True
option.add_argument("user-agent= Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/600.5.17 (KHTML, like Gecko) Version/8.0.5 Safari/600.5.17")
option.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(PATH, chrome_options = option)



def accept_cookies(class_name):
    accept_button = driver.find_element(By.CLASS_NAME, class_name)
    accept_button.click()


def search():
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys("webdriver")
    search_box.send_keys(Keys.RETURN)


def size_of_window():
    driver.maximize_window()
    time.sleep(3)
    driver.minimize_window()
    time.sleep(3)
    driver.set_window_size(1200, 1200)


def screen_shoot():
    driver.get_screenshot_as_file("Images/image.png")
    driver.save_screenshot("Images/image.png")

    elem = driver.find_element(By.CLASS_NAME, "lnXdpd")
    elem.screenshot("Images/elem_image.png")


def user_agent():
    driver.get("https://n5m.ru/usagent.html")
    option1 = webdriver.ChromeOptions()
    option1.add_argument("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/600.5.17 (KHTML, like Gecko) Version/8.0.5 Safari/600.5.17")
    browser = webdriver.Chrome(PATH, options=option1)
    driver.get("https://n5m.ru/usagent.html")


def using_proxy():
    PROXY = "122.139.91.109:8000"
    options = webdriver.ChromeOptions()
    options.add_argument('--proxy-server=%s' % PROXY)
    browser = webdriver.Chrome(PATH, chrome_options=options)
    browser.get("https:/google.com")
    time.sleep(3)

def web_driver_mode(option):
    driver.get("https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html")
    time.sleep(3)


def auto_reg():
    driver.get("https://www.instagram.com/")
    print("acept")
    driver.implicitly_wait(1)
    accept_cookies("aOOlW.bIiDR")
    input_gmail = driver.find_element(By.NAME, "username")
    input_gmail.send_keys("Gmail")
    print("gmail")

    input_password = driver.find_element(By.NAME, "password")
    input_password.send_keys("Password")
    print("pasword")
    input_password.send_keys(Keys.ENTER)

# using_proxy()
# user_agent()
# accept_cookies()
# screen_shoot()
# size_of_window()
# search()




#auto_reg()
#web_driver_mode(option)

time.sleep(3)


driver.close()
driver.quit()
