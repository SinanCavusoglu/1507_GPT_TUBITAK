import os
key_words = "key_words.txt"
with open(key_words, "r") as text:
    text_list = text.readlines()
    text_list = [text.strip("\n").strip().capitalize() for text in text_list]
    text_list = list(set(text_list))
    text_list.sort()
os.remove(key_words)
with open(key_words, "w") as text:
    for i in text_list[:-1]:
        text.write(i)
        text.write("\n")
    text.write(text_list[-1])        