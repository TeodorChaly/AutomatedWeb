from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium import webdriver
import time

PATH = "C:\Go\chromedriver.exe"


# Entering site that you want to pars


def filtering(driver,item, rarity ):
    time.sleep(1)

    # Finding a type
    filter_res = driver.find_element(By.CLASS_NAME, "filter-options")
    filter_res2 = filter_res.find_elements(By.CLASS_NAME, "dropdown-menu")

    for i in filter_res2:
        slide_elements = driver.find_element(By.XPATH, "/html/body/main/div[3]/div[1]/div[2]/ul/li[2]/span")
        slide_elements.click()
        if i.get_attribute("dropdown-label") == "typeDropdown": # Type of item
            filter_res3 = i.find_elements(By.CLASS_NAME, "dropdown-choice")
            for i2 in filter_res3:
                title = i2.get_attribute("filter-value")
                if title == item:
                    i2.click()
                    break
        if i.get_attribute("dropdown-label") != "typeDropdown":  # Type of rarity
            choose_rearity = driver.find_element(By.XPATH, "/html/body/main/div[3]/div[1]/div[2]/ul/li[3]")
            choose_rearity.click()
            filter_res3 = i.find_elements(By.CLASS_NAME, "dropdown-choice")
            for i2 in filter_res3:
                title = i2.get_attribute("filter-value")
                if title == rarity:
                    i2.click()
                    break

    # Click button for filter search
    filter_accept = driver.find_element(By.XPATH, "/html/body/main/div[3]/div[1]/div[2]/div/button")
    filter_accept.click()
    time.sleep(1)


def check_exists_by_xpath(xpath,driver):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True

def getting_pages(driver):
    filter_res = driver.find_element(By.CLASS_NAME, "filter-results.items-row")
    posts = filter_res.find_elements(By.CLASS_NAME, "item-responsive")
    list_of_pages = []
    for post in posts:
        title = post.find_element(By.TAG_NAME, "a").get_attribute("href")
        list_of_pages.append(title)
    return list_of_pages
def main():
    driver = webdriver.Chrome(PATH)
    driver.get("https://fnbr.co/list")

    item = "outfit".lower()
    rarity = "dark".lower()

    # Loading page and accept cookies
    time.sleep(2)
    if check_exists_by_xpath("/html/body/div[1]/div/div/div/div[2]/div/button[1]", driver):
        accept = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div/button[1]")
        accept.click()
    else:
        pass


    filtering(driver, item, rarity)
    list_of_pages = getting_pages(driver)
    for i in list_of_pages:
        driver.get(i)
        all_info = driver.find_element(By.CLASS_NAME, "col-md-7.col-12")
        name = all_info.find_element(By.TAG_NAME, "h1").text
        item_price = all_info.find_element(By.CLASS_NAME, "item-price").text
        print("Name: ", name, "\nPrice: ",item_price)
        print()







main()
