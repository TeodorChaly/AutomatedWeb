import deepl


auth_key = "KEY"  # Replace with your key
translator = deepl.Translator(auth_key)
language = "RU"

file_read = open('results.txt')

length = sum(1 for line in open('results.txt', 'r', encoding="utf-8"))
count = 0

with open(f"translated_file_to_{language.lower()}.txt", "w", encoding="utf-8") as file:
    print("Create results of translate file")

with open(f"translated_file_to_{language.lower()}.txt", "a", encoding="utf-8") as file_append:
    for text_to_translate in file_read:
        print(length-count)
        count+=1
        try:
            list_of_split_text = text_to_translate.replace("\n", "").split("|")
            question = translator.translate_text(list_of_split_text[0], target_lang=language)
            answer = translator.translate_text(list_of_split_text[1], target_lang=language)
            url = list_of_split_text[2]
            full_text = str(question) + "|" + str(answer) + "|" + url + "\n"
            file_append.write(full_text)
            file_append.flush()
        except:
            print("Question unkorektly")
