import requests
from bs4 import BeautifulSoup
import lxml

headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
           "Accept-Language": "en-US,en;q=0.9"}
cookies = {"CONSENT": "YES+cb.20210720-07-p0.en+FX+410"}

url = "https://thelastofus.fandom.com/wiki/Category:The_Last_of_Us_Part_II_characters"

r = requests.get(
    url, headers=headers, cookies=cookies
)


def find_elements(soup2):
    try:
        name = soup2.find(id = "firstHeading")
        print(name.text.strip())
    except:
        print("No Name")
    # try:
    #     region = soup2.find(role = "region")
    #     print(region.find())
    # except:
    #     print("No region")

def passing_urls(list_of_characters_url):
    for character_url in list_of_characters_url:
        r2 = requests.get(
            character_url, headers=headers, cookies=cookies
        )
        src2 = r2.text
        soup2 = BeautifulSoup(src2, "lxml")
        find_elements(soup2)
        print(character_url)


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

passing_urls(list_of_characters_url)

