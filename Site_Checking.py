from selenium.webdriver.common.by import By
from selenium import webdriver
import time

PATH = "C:\Go\chromedriver.exe"
option = webdriver.ChromeOptions()
# option.headless = True
option.add_argument("user-agent= Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/600.5.17 (KHTML, like Gecko) Version/8.0.5 Safari/600.5.17")
option.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(PATH, chrome_options=option)

# driver.quit()


def finding_element_by_opening(driver, element, double_element,triple_element):
    list_of_types = driver.find_elements(By.TAG_NAME, "h2")
    list_of_link = []
    for i in list_of_types:
        link = i.find_element(By.TAG_NAME, "a").get_attribute("href")
        list_of_link.append(link)
    for i in list_of_link:
        count = 0
        element_link = ""
        driver.get(i)
        name_category = driver.find_elements(By.CLASS_NAME, "a_category")
        for i2 in name_category:
            if i2.text == element:
                element_link = i2.get_attribute("href")
                count += 1
                break
        if count != 0:
            if double_element != "":
                element_link = preparing(driver, element_link, double_element)
                if triple_element != "":
                    element_link = preparing(driver, element_link, triple_element)
            time.sleep(3)
            return element_link


def preparing(driver, element_link, element_num):
    driver.get(element_link)
    name_category = driver.find_elements(By.CLASS_NAME, "a_category")
    for i2 in name_category:
        if i2.text == element_num:
            element_link = i2.get_attribute("href")
            return element_link
    return element_link

def main():
    url = "https://www.ss.lv/ru"
    driver.get(url)

    language = "RU"
    element = "Квартиры"
    double_element = "Рига"
    triple_element = "Центр"

    link = finding_element_by_opening(driver, element, double_element, triple_element)
    print(link)
    time.sleep(3)

    driver.close()


if __name__ == "__main__":
    main()
