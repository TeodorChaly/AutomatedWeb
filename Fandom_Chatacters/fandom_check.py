import requests
from bs4 import BeautifulSoup
from lxml import html
import csv

headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
           "Accept-Language": "en-US,en;q=0.9"}
cookies = {"CONSENT": "YES+cb.20210720-07-p0.en+FX+410"}


url = "https://thelastofus.fandom.com/wiki/Category:The_Last_of_Us_Part_II_characters"

r = requests.get(
    url, headers=headers, cookies=cookies
)


def csv_adder(character_info):
    global file_name
    with open(f"{file_name}.csv", "a", encoding="utf-8", newline="")as file:
        writer = csv.writer(file, delimiter=';')
        list_cat = []
        for category in character_info:
            list_cat.append(character_info[category])
        writer.writerow(list_cat)
        file.flush()


def create_csv_file(r, all_categories):
    global file_name
    tree = html.fromstring(r.content)
    title = "No Name"
    all_categories.append("URL")
    try:
        name = tree.xpath('//*[@id="mw-content-text"]/div[1]/p/i/a')
        title = name[0].text
    except:
        pass
    try:
        name = tree.xpath('//*[@id="mw-content-text"]/div[1]/p/a')
        title = name[0].text
    except:
        pass
    file_name = title.replace(" ", "_")
    with open(f"{file_name}.csv", "w", encoding="utf-8", newline="")as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow([title])
        writer.writerow(all_categories)


def collect_all_category(soup2, all_list):
    list1 = soup2.find_all(class_="pi-data-label pi-secondary-font")
    for category in list1:
        if category.text not in all_list:
            all_list.append(category.text)


def passing_urls(list_of_characters_url, status, list_of_categories):
    all_list = []
    count = 0
    if status == 0:
        for character_url in list_of_characters_url:
            r2 = requests.get(
                character_url, headers=headers, cookies=cookies
            )
            src2 = r2.text
            soup2 = BeautifulSoup(src2, "lxml")
            collect_all_category(soup2, all_list)
            count += 1
            print(len(list_of_characters_url) * 2 - count)
        return all_list
    elif status == 1:
        for character_url in list_of_characters_url:
            r2 = requests.get(
                character_url, headers=headers, cookies=cookies
            )
            src2 = r2.text
            soup2 = BeautifulSoup(src2, "lxml")

            mega_category_dict = {}
            count += 1
            print(len(list_of_characters_url) - count)
            for i in list_of_categories:
                list_of_curently_category = soup2.find_all(class_="pi-data-label pi-secondary-font")
                exist = False

                for i3 in list_of_curently_category:
                    if i3.text == i:
                        exist = True
                        break

                if exist:
                    for i2 in list_of_curently_category:
                        if i == i2.text:
                            mega_category_dict[i] = i2.find_next_sibling().text
                            break
                else:
                    mega_category_dict[i] = "-"
            mega_category_dict["URL"] = character_url
            csv_adder(mega_category_dict)

def how_many_pages(url):
    hrefs = []
    while True:
        hrefs.append(url)
        r = requests.get(
            url, headers=headers, cookies=cookies
        )
        print(url)
        src = r.text
        soup = BeautifulSoup(src, "lxml")
        try:
            next_url = soup.find(class_="category-page__pagination-next wds-button wds-is-secondary")
            url = next_url['href']
        except:
            break
    return hrefs

list_of_characters_url = []
main_url = url[:url.find(".com") + 4]
if r.status_code == 200:
    hrefs = how_many_pages(url)
    for href in hrefs:
        r = requests.get(
            href, headers=headers, cookies=cookies
        )
        src = r.text
        soup = BeautifulSoup(src, "lxml")
        list_of_all_characters = soup.find_all(class_="category-page__member-link")
        for character in list_of_all_characters:
            if "category" not in character["title"].lower():
                list_of_characters_url.append(main_url + character["href"])

file_name = ""

list_of_categories = passing_urls(list_of_characters_url, 0, None)
create_csv_file(r, list_of_categories)
print(list_of_characters_url)
passing_urls(list_of_characters_url, 1, list_of_categories)
