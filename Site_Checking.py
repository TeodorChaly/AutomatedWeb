from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys
from selenium import webdriver
import time
import sys
import os

PATH = "C:\Go\chromedriver.exe"
option = webdriver.ChromeOptions()
option.headless = True
option.add_argument(
    "user-agent= Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/600.5.17 (KHTML, like Gecko) Version/8.0.5 Safari/600.5.17")
option.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(PATH, chrome_options=option)


def check_exists_by_xpath(xpath, driver_1):
    try:
        driver_1.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True


def finding_element_by_opening(driver_1, element, double_element, triple_element):
    list_of_types = driver_1.find_elements(By.TAG_NAME, "h2")
    list_of_link = []
    for i in list_of_types:
        link = i.find_element(By.TAG_NAME, "a").get_attribute("href")
        list_of_link.append(link)
    for i in list_of_link:
        count = 0
        element_link = ""
        driver_1.get(i)
        name_category = driver_1.find_elements(By.CLASS_NAME, "a_category")
        for i2 in name_category:
            if i2.text == element:
                element_link = i2.get_attribute("href")
                count += 1
                break
        if count != 0:
            if double_element != "":
                element_link = preparing(driver_1, element_link, double_element)
                if triple_element != "":
                    element_link = preparing(driver_1, element_link, triple_element)
            return element_link


def preparing(driver_1, element_link, element_num):
    driver_1.get(element_link)
    name_category = driver_1.find_elements(By.CLASS_NAME, "a_category")
    for i2 in name_category:
        if i2.text == element_num:
            element_link = i2.get_attribute("href")
            return element_link
    return element_link


def page_detail_scanning(driver_1, link):
    driver_1.get(link)
    list_of_description = driver_1.find_elements(By.CLASS_NAME, "ads_opt")
    list_of_name_description = driver_1.find_elements(By.CLASS_NAME, "ads_opt_name")
    dict_of_full_description = {}
    print()
    i0 = 0
    i_0 = 0
    for i in list_of_name_description:
        i0 += 1
        dict_of_full_description[i.text] = i0
    for i2 in list_of_description:
        i_0 += 1
        for i3 in dict_of_full_description:
            if dict_of_full_description[i3] == i_0:
                dict_of_full_description[i3] = i2.text

    for i4 in dict_of_full_description:
        print(i4, dict_of_full_description[i4])

    price_money = None
    price_name = None
    price_name_list = driver_1.find_elements(By.CLASS_NAME, "ads_opt_name_big")
    price_money_list = driver_1.find_elements(By.CLASS_NAME, "ads_price")
    for i5 in price_name_list:
        price_name = i5.text
    for i6 in price_money_list:
        price_money = i6.text

    if price_name is not None:
        print(price_name, price_money)
    else:
        pass
    print(link)
    print("-------")
    return None


def checking_pages(driver_1):
    list_of_all_pages = driver_1.find_elements(By.CLASS_NAME, "navi")
    list_of_pages = []
    list_of_new_links = []
    new_list_of_elem = []
    for i in list_of_all_pages:
        if i.text.isdigit():
            list_of_pages.append(i.get_attribute("href"))

    if len(list_of_pages) == 0:
        list_of_sells = driver_1.find_elements(By.CLASS_NAME, "am")
        for i in list_of_sells:
            href = i.get_attribute("href")
            new_list_of_elem.append(href)
            checking_new_link(href, list_of_new_links)
        driver_1.get(driver_1.current_url)
    else:
        list_of_sells = driver_1.find_elements(By.CLASS_NAME, "am")
        for i in list_of_sells:
            href = i.get_attribute("href")
            new_list_of_elem.append(href)
            checking_new_link(href, list_of_new_links)

        for i2 in list_of_pages:
            driver_1.get(i2)
            list_of_sells = driver_1.find_elements(By.CLASS_NAME, "am")
            for i in list_of_sells:
                href = i.get_attribute("href")
                new_list_of_elem.append(href)
                checking_new_link(href, list_of_new_links)

    return new_list_of_elem, list_of_new_links


def checking_file_exist():
    if not os.path.exists('Old_Data/Old_results.txt'):
        if os.path.exists('Old_Data/'):
            open('Old_Data/Old_results.txt', "w")
        elif not os.path.exists('Old_Data/'):
            os.mkdir("Old_Data")
            open('Old_Data/Old_results.txt', "w")


def checking_new_link(href, list_of_new_links):
    f = open('Old_Data/Old_results.txt')
    list_of_saved_links = []
    list_of_links = []
    for i in f.readlines():
        list_of_saved_links.append(i)
    if href + "\n" not in list_of_saved_links:
        list_of_links.append(href)
        list_of_new_links.append(href)
        adding_element(href)
        return True
    else:
        return False


def adding_element(href):
    old_results = open('Old_Data/Old_results.txt', "a+", encoding="utf-8")
    old_results.write(href + "\n")


def deleting_elements(list_of_elem):
    f = open('Old_Data/Old_results.txt', "r")
    lines = f.readlines()
    f.close()
    f = open("Old_Data/Old_results.txt", "w")
    delete_element = []
    for i in lines:
        if i[:-1] not in list_of_elem:
            delete_element.append(i)
    for line in lines:
        if line not in delete_element:
            f.write(line)

    if len(delete_element) != 0:
        print(delete_element)


def search_filter(finding_dict, day_filter_text, day_filter_enter):
    search = driver.find_element(By.XPATH, "/html/body/div[2]/div/span[2]/b[3]/a")
    search.click()
    selected_element = driver.find_element(By.XPATH, "/html/body/div[4]/div/table/tbody/tr/td/div[1]/table/tbody/tr/td/form/table/tbody")
    selected_elements = selected_element.find_elements(By.TAG_NAME, "tr")

    for i in selected_elements:
        list2 = i.find_elements(By.CLASS_NAME, "td6")
        for i2 in list2:
            for i3 in finding_dict:
                if i3 == i2.text:
                    a = i.find_elements(By.CLASS_NAME, "in1")
                    b = i.find_elements(By.CLASS_NAME, "in1s")
                    c = i.find_elements(By.CLASS_NAME, "in3")
                    d = i.find_elements(By.CLASS_NAME, "td7")

                    if len(a) != 0:
                        filtering(a, 1, finding_dict[i3])
                    elif len(d) != 0:
                        for i4 in d:
                            print(i4.text, finding_dict[i3])
                            if finding_dict[i3] == i4.text:
                                i4.click()
                    elif len(c) != 0:
                        filtering(c, 3, finding_dict[i3])
                    elif len(b) != 0:
                        filtering(b, 2, finding_dict[i3])
                    else:
                        print("wrong")  # Помарка
            if i2.text == day_filter_text:
                all_options = i.find_elements(By.TAG_NAME, "option")
                for options in all_options:
                    if options.text == day_filter_enter:
                        options.click()

    enter = driver.find_element(By.ID, "sbtn")
    enter.click()


def today_filter():
    drop_box = driver.find_element(By.ID, "today_cnt_sl")
    drop_box.click()
    today_choose = driver.find_element(By.XPATH, "/html/body/div[4]/div/table/tbody/tr/td/div[1]/table/tbody/tr/td/div/div[2]/select/option[2]")
    today_choose.click()


def filtering(object_element, type_of_element, enter_text):
    if type_of_element == 1:
        object_element[0].send_keys(Keys.DELETE)
        object_element[0].send_keys(enter_text)
    elif type_of_element == 2:
        all_options = object_element[0].find_elements(By.TAG_NAME, "option")
        for options in all_options:
            if enter_text == options.text:
                options.click()
                break
    else:
        for i in object_element:
            for i2 in enter_text:
                if i2.lower() in i.get_attribute("name"):
                    object_element[0].send_keys(Keys.DELETE)
                    i.send_keys(enter_text[i2])
                    break
                if i2.lower() in i.get_attribute("name"):
                    object_element[0].send_keys(Keys.DELETE)
                    i.send_keys(enter_text[i2])
                    break


def main():
    url = "https://www.ss.lv/"

    language = "lv"

    element = "Vieglie auto"
    double_element = "Audi"
    triple_element = ""

    if language == "ru":
        day_filter_text, day_filter_enter = "Искать за период: ", "Среди сегодняшних объявлений"
    else:
        day_filter_text, day_filter_enter = "Meklēt par periodu: ", "Starp šodienas sludinājumiem"

    finding_elem_one, one = "Cena: ", ""
    finding_elem_two, two = "Izlaiduma gads:", {"Min": "", "Max": ""}
    finding_elem_three, three = "", ""

    finding_dict = {finding_elem_one: one, finding_elem_two: two, finding_elem_three: three}

    if language.lower() == "lv":
        url += "lv"
    elif language.lower() == "ru":
        url += "ru"

    driver.get(url)

    cookies = driver.find_element(By.XPATH, "/html/body/div[5]/div/div/table/tbody/tr/td[2]/button")
    cookies.click()

    print("Finding all links")
    if element != "":
        link = finding_element_by_opening(driver, element, double_element, triple_element)
    else:
        print("Nothing is entered (in first element)")
        driver.close()
        sys.exit()

    print("File exist checking")
    checking_file_exist()

    print("Filtering search")
    driver.get(link)

    search_filter(finding_dict, day_filter_text, day_filter_enter)

    while True:
        # print("Checking pages")
        new_list, new_elements_to_show = checking_pages(driver)
        # print(new_elements_to_show)
        # print("Deleting not necessary elements")
        deleting_elements(new_list)
        # print("Checking every page")
        if len(new_elements_to_show) != 0:
            back_url = driver.current_url
            for i2 in new_elements_to_show:
                page_detail_scanning(driver, i2)
                print("New!!")
            driver.get(back_url)

        print("-------")
        time.sleep(30)
        # print("+++++++")


if __name__ == "__main__":
    main()

# Отослать смс
