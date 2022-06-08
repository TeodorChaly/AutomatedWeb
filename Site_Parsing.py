from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium import webdriver
import datetime
import time
import os

PATH = "C:\Go\chromedriver.exe"


# Entering site that you want to pars


def filtering(driver, item, rarity):
    time.sleep(1)
    re_rarity = rarity
    re_item = item

    # Finding a type
    filter_res = driver.find_element(By.CLASS_NAME, "filter-options")
    filter_res2 = filter_res.find_elements(By.CLASS_NAME, "dropdown-menu")

    for i in filter_res2:
        if check_exists_by_xpath('/html/body/main/div[3]/div[1]/div[2]/ul/li[2]/span', driver ):
            slide_elements = driver.find_element(By.XPATH, "/html/body/main/div[3]/div[1]/div[2]/ul/li[2]/span")
            slide_elements.click()

        if i.get_attribute("dropdown-label") == "typeDropdown":  # Type of item
            filter_res3 = i.find_elements(By.CLASS_NAME, "dropdown-choice")
            list_item = []
            for i5 in filter_res3:
                title = i5.get_attribute("filter-value")
                list_item.append(title)
            if item != "all" and item in list_item:
                for i2 in filter_res3:
                    title = i2.get_attribute("filter-value")
                    if title == item:
                        actions = ActionChains(driver)
                        actions.move_to_element(i2).perform()
                        driver.execute_script("arguments[0].click();", i2)
                        break
            elif item not in list_item and item != "all":
                re_item = str(input("Enter correct item: "))
                filtering(driver, re_item, rarity)
            else:
               pass
        if i.get_attribute("dropdown-label") != "typeDropdown":  # Type of rarity
            choose_rearity = driver.find_element(By.XPATH, "/html/body/main/div[3]/div[1]/div[2]/ul/li[3]")
            choose_rearity.click()
            filter_res3 = i.find_elements(By.CLASS_NAME, "dropdown-choice")
            list_rarity = []
            for i5 in filter_res3:
                title = i5.get_attribute("filter-value")
                list_rarity.append(title)
            if rarity != "all" and rarity in list_rarity:
                for i2 in filter_res3:
                    title = i2.get_attribute("filter-value")
                    if title == rarity:
                        actions = ActionChains(driver)
                        actions.move_to_element(i2).perform()
                        driver.execute_script("arguments[0].click();", i2)
                        break
            elif rarity not in list_rarity and rarity != "all":  # If entered text is incorrect, input for rewriting
                re_rarity = str(input("Enter correct rarity: "))
                filtering(driver, item, re_rarity)
            else:
               pass


    # Click button for filter search
    filter_accept = driver.find_element(By.XPATH, "/html/body/main/div[3]/div[1]/div[2]/div/button")
    filter_accept.click()
    return re_item, re_rarity

def check_exists_by_xpath(xpath, driver):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True


def getting_pages(driver):
    filter_res = driver.find_element(By.CLASS_NAME, "filter-results.items-row")
    posts = filter_res.find_elements(By.CLASS_NAME, "item-responsive")
    list_of_pages = []
    for post in posts:  # Getting all links in all posts
        print(post.text)
        title = post.find_element(By.TAG_NAME, "a").get_attribute("href")
        list_of_pages.append(title)
    return list_of_pages


def scroll_down_page(driver):
    SCROLL_PAUSE_TIME = 0.5

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def other_page_visit(driver, list_of_pages, item, rarity):
    dict_of_most_rare = {}
    dict_of_info = {}
    for i in list_of_pages:
        driver.get(i)
        if check_exists_by_xpath("/html/body/main/div[4]/div/div[2]/div[2]/div/div[1]", driver):
            all_info = driver.find_element(By.CLASS_NAME, "col-md-7.col-12")
            name = "Name: " + all_info.find_element(By.TAG_NAME, "h1").text
            item_rarity = "Rarity: " + all_info.find_element(By.XPATH, "/html/body/main/div[4]/div/div[2]/div[2]/div/div[1]/h3/span[1]").text
            item_type = "Type: " + all_info.find_element(By.XPATH, "/html/body/main/div[4]/div/div[2]/div[2]/div/div[1]/h3/span[2]").text
            item_price = "Price: " + all_info.find_element(By.CLASS_NAME, "item-price").text
            item_link = "Link: " + i
            date = all_info.find_elements(By.CLASS_NAME, "shop-data-container")

            count = 0
            for i2 in date:
                data2 = i2.find_elements(By.TAG_NAME, "p")
                for i3 in data2:
                    count = count + 1

            if count == 3 and check_exists_by_xpath("/html/body/main/div[4]/div/div[2]/div[2]/div/div[1]/div/p[2]", driver):
                item_release_date = all_info.find_element(By.XPATH, "/html/body/main/div[4]/div/div[2]/div[2]/div/div[1]/div/p[1]").text
                item_last_seen = all_info.find_element(By.XPATH, "/html/body/main/div[4]/div/div[2]/div[2]/div/div[1]/div/p[2]").text
                item_occurrences = all_info.find_element(By.XPATH, "/html/body/main/div[4]/div/div[2]/div[2]/div/div[1]/div/p[3]").text
            else:
                item_release_date = all_info.find_element(By.XPATH, "/html/body/main/div[4]/div/div[2]/div[2]/div/div[1]/div/p[2]").text
                item_last_seen = all_info.find_element(By.XPATH, "/html/body/main/div[4]/div/div[2]/div[2]/div/div[1]/div/p[3]").text
                item_occurrences = all_info.find_element(By.XPATH, "/html/body/main/div[4]/div/div[2]/div[2]/div/div[1]/div/p[4]").text

            if check_exists_by_xpath("/html/body/main/div[4]/div/div[2]/div[2]/div/div[2]/div[1]/table/tbody/tr[1]/td[2]/span", driver):
                if all_info.find_element(By.XPATH, "/html/body/main/div[4]/div/div[2]/div[2]/div/div[2]/div[1]/table/tbody/tr[1]/td[2]/span").text == "Today":
                    item_last = 0
                else:
                    item_last = int(all_info.find_element(By.XPATH, "/html/body/main/div[4]/div/div[2]/div[2]/div/div[2]/div[1]/table/tbody/tr[1]/td[2]/span").text)
            else:
                item_last = -1

            dict_of_most_rare[name] = item_last
            dict_of_info[name] = [item_price, item_rarity, item_type, item_release_date, item_last_seen, item_occurrences, item_link]
            print(dict_of_info[name])
            print( name, "\n", item_rarity, "\n", item_type, "\n", item_price, "\n",
                  item_release_date, "\n", item_last_seen, "\n", item_occurrences)
            print()
        else:
            pass

    filter_dict = filter_last_day(dict_of_most_rare)
    adding_file(filter_dict, dict_of_info, item, rarity)


def filter_last_day(dict_of_most_rare):
    new_dict = {}
    dict_len = len(dict_of_most_rare)
    i0 = 0
    while i0 <= dict_len:
        for i in dict_of_most_rare:
            if dict_of_most_rare[i] == max(dict_of_most_rare.values()):
                new_dict[i] = dict_of_most_rare[i]
                dict_of_most_rare.pop(i)
                break
        i0 += 1
    return new_dict


def adding_file(filter_dict, dict_of_info, item, rarity):
    # Creating folder for results
    if os.path.exists('Results') == False:
        folder = "Results"
        os.mkdir(folder)
    else:
        folder = "Results"

    f = open(folder + '/' + "Res_" + item + "_" + rarity, 'w', encoding="utf-8")
    f.write("Ranking (by most rare " + item + ") in " + rarity + " category")
    print(filter_dict)
    f.write("\n")
    for i3 in filter_dict:
        for i4 in dict_of_info:
            if i3 == i4 and i4:
                f.write("\n")
                print(i3)
                print(filter_dict[i3])
                print(str(i3))
                print(str(filter_dict[i3]))
                print()
                if filter_dict[i3] == -1:
                    f.write(str(i3) + " (Never append in shop)")
                elif filter_dict[i3] == 0:
                    f.write(str(i3) + " (Today)")
                else:
                    f.write(str(i3) + " (" + str(filter_dict[i3]) + " days absent)")
                f.write("\n")
                for key in dict_of_info[i4]:
                    f.write(key)
                    f.write("\n")

    f.close()


def main():
    driver = webdriver.Chrome(PATH)
    driver.get("https://fnbr.co/list")

    item = "outfit".lower()
    rarity = "marvel".lower()

    time.sleep(2)
    # Loading page and accept cookies
    if check_exists_by_xpath("/html/body/div[1]/div/div/div/div[2]/div/button[1]", driver):
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div/button[1]").click()
    else:
        pass

    start = datetime.datetime.now()

    item, rarity = filtering(driver, item, rarity)
    scroll_down_page(driver)
    list_of_pages = getting_pages(driver)
    other_page_visit(driver, list_of_pages, item, rarity)

    end = datetime.datetime.now()
    print('totally time is ', end - start)


main()
