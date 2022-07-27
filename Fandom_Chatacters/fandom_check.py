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

def create_csv_file(r, all_categories):
    tree = html.fromstring(r.content)

    name = tree.xpath('//*[@id="mw-content-text"]/div[1]/p/i/a')
    title = name[0].text
    file_name = title.replace(" ", "_")
    with open(f"{file_name}.csv","w", encoding="utf-8" )as file:
        writer = csv.writer(file , delimiter=';')
        writer.writerow([title])
        writer.writerow(all_categories)


def collect_all_category(soup2, all_list):
    # try:
    #     name = soup2.find(id = "firstHeading")
    #     print(name.text.strip())
    # except:
    #     print("No Name")

    list1 = soup2.find_all(class_="pi-data-label pi-secondary-font")
    for category in list1:
        if category.text not in all_list:
            all_list.append(category.text)
    # try:
    #     region = soup2.find(role = "region")
    #     print(region.find())
    # except:
    #     print("No region")

def passing_urls(list_of_characters_url, status, list_of_categories):
    all_list = []
    if status == 0:
        for character_url in list_of_characters_url:
            r2 = requests.get(
                character_url, headers=headers, cookies=cookies
            )
            src2 = r2.text
            soup2 = BeautifulSoup(src2, "lxml")
            collect_all_category(soup2, all_list)
        return all_list
    elif status == 1:
        for character_url in list_of_characters_url:
            r2 = requests.get(
                character_url, headers=headers, cookies=cookies
            )
            src2 = r2.text
            soup2 = BeautifulSoup(src2, "lxml")
            print(character_url)
            for i in list_of_categories:
                list_of_curently_category = soup2.find_all(class_= "pi-data-label pi-secondary-font")
                exist = False
                for i3 in list_of_curently_category:
                    if i3.text == i:
                        exist = True
                        break

                if exist:
                    for i2 in list_of_curently_category:
                        if i == i2.text:
                            print(i, "=", i2.find_next_sibling().text)
                            break
                else:
                    print(i, "None")



main_url =url[:url.find(".com")+4]
if r.status_code == 200:
    src = r.text
    soup = BeautifulSoup(src, "lxml")

    list_of_all_characters = soup.find_all(class_ = "category-page__member-link")
    list_of_characters_url = []
    for character in list_of_all_characters:
        if "category" not in character["title"].lower():
            list_of_characters_url.append(main_url+ character["href"])
    print(list_of_characters_url)

list_of_categories = passing_urls(list_of_characters_url, 0, None)
create_csv_file(r, list_of_categories)
passing_urls(list_of_characters_url, 1, list_of_categories)
