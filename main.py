import requests
from bs4 import BeautifulSoup
import lxml

headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
           "Accept-Language":"en-US,en;q=0.9"}
cookies = {"CONSENT": "YES+cb.20210720-07-p0.en+FX+410"}

text = "what jobs allow you to travel".replace(" ", "+")
r = requests.get(
    f"https://www.google.com/search?q={text}&oq=wha&aqs=chrome.1.69i57j35i39j0i67j0i433i512j0i131i433i512j0i512j69i60j69i61.1408j0j7&sourceid=chrome&ie=UTF-8", headers=headers, cookies=cookies
)

with open("results.txt", "w", encoding="utf-8") as file:
    print("Create results file")


lenght = sum(1 for line in open('what-travel.txt', 'r', encoding="utf-8"))


with open("results.txt", "a", encoding="utf-8") as file_append:
    file_read = open('what-travel.txt')
    count = 0

    for line in file_read:
        count +=1
        question = line.strip().replace(" ", "+")

        r = requests.get(
            f"https://www.google.com/search?q={question}&oq=wha&aqs=chrome.1.69i57j35i39j0i67j0i433i512j0i131i433i512j0i512j69i60j69i61.1408j0j7&sourceid=chrome&ie=UTF-8",
            headers=headers, cookies=cookies
        )
        if r.status_code == 200:
            with open('page_code.html', 'w', encoding="utf-16") as f:

                f.write(r.text)
                f.close()
            with open("page_code.html", encoding="utf-16") as file_html_read:
                src = file_html_read.read()

            soup = BeautifulSoup(src, "lxml")
            question = question.replace("+", " ")
            try:
                answer_text = soup.find(class_ ="hgKElc")
                url = soup.find(class_="yuRUbf").find("a")["href"]
                output_res = question + "|" + answer_text.text + "|" + url + "\n"
                file_append.write(output_res)
                print(f"Осталось {lenght - count} файлов, ответ {answer_text.text }")
            except Exception:
                try:
                    answer_text = soup.find(class_ = "i8Z77e")
                    if answer_text == None:
                        answer_text = soup.find(class_ = "X5LH0c")
                    url = soup.find(class_="yuRUbf").find("a")["href"]
                    output_res = question+"|"+answer_text.text + "|"+ url + "\n"
                    file_append.write(output_res)
                    print(f"Осталось {lenght - count} файлов, ответ {answer_text.text }")
                except Exception:
                    output_res = question + "|Don't exists"
                    file_append.write(output_res)
                    print(f"Осталось {lenght - count} файлов, ответ Don t exists, вопрос {question}")

        else:
            print("Server error")

