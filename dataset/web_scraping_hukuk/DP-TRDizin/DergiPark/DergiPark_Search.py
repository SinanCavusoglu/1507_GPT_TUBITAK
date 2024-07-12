import os
import time

import pandas as pd

import requests
from bs4 import BeautifulSoup

def key_word_list(file_dir):
    # Prepare the key-words list
    with open(file_dir, "r") as file:
        words_list = [word.strip("\n") for word in file.readlines()]
    return words_list 

def total_page_num(str_search):
    # Return max number of pages
    url = f'https://dergipark.org.tr/tr/search/1?q=%28title%3A+%22{str_search}%22+OR+journal%3A+%22{str_search}%22%29+AND+%28pubyear%3A+%28%3E%3D2008%29%29&section=articles'
    page = requests.get(url, timeout=999)
    soup = BeautifulSoup(page.text, "lxml")
    page_slider = soup.find("ul", class_ = "kt-pagination__links mx-auto")
    max_number = page_slider.find_all("li")[-2].text if page_slider else 0
    return int(max_number) 

def box_extract(box):
    # Extract Article Info
    article_url = box.find("h5", class_ = "card-title").find("a")["href"]                   # Box URL
    article_name = box.find("h5", class_ = "card-title").find("a").text.strip()             # Article Name
    
    return article_url, article_name

def article_extract(article_url):
    # Extract Article PDF
    page_article = requests.get(article_url, timeout=999)
    soup_article = BeautifulSoup(page_article.text, "lxml")
    pdf_button = soup_article.find("a", class_="btn btn-sm float-left article-tool pdf d-flex align-items-center")
    pdf_url = pdf_button["href"] if pdf_button else None
    pdf_url = "https://dergipark.org.tr" + pdf_url if pdf_button else None
    
    article_volume_first = soup_article.find("div", class_ = "tab-pane active")
    article_volume = article_volume_first.find("span", class_ = "article-subtitle").text.split(",")[1].strip() if article_volume_first else None
    
    article_journal = soup_article.find("h1", {"id": "journal-title"}).text if soup_article.find("h1", {"id": "journal-title"}) else None
    return pdf_url, article_volume, article_journal

file_dir = "key_words.txt"  
words_list = key_word_list(file_dir)

for str_search in words_list:
    max_number = total_page_num(str_search)
    if max_number == 0:
        print("There is no such category in DergiPark")
        continue
    article_dict = {"Page_Number": [], "Searching": [],"Article_Name": [], "Article_Journal": [], "Article_Volume": [], "Article_PDF_URL": []}
    for page_num in range(1, max_number + 1):
        url = f'https://dergipark.org.tr/tr/search/{page_num}?q=%28title%3A+%22{str_search}%22+OR+journal%3A+%22{str_search}%22%29+AND+%28pubyear%3A+%28%3E%3D2008%29%29&section=articles'
        page = requests.get(url, timeout = 999)
        soup = BeautifulSoup(page.text, "lxml")
        print(f"{str_search} - {page} - {page_num}/{max_number}")
        # ---------- BOXES ---------- #
        boxes = soup.find_all("div", class_ = "card article-card dp-card-outline")
        
        for box in boxes:
            article_url, article_name = box_extract(box)
            # ---------- ARTICLE ---------- #
            pdf_url, article_volume, article_journal = article_extract(article_url)  
            
            article_dict["Page_Number"].append(page_num)
            article_dict["Searching"].append(str_search)
            article_dict["Article_Name"].append(article_name)
            article_dict["Article_Journal"].append(article_journal)
            article_dict["Article_Volume"].append(article_volume)
            article_dict["Article_PDF_URL"].append(pdf_url)
            print(article_name)
        time.sleep(1)
    
    os.makedirs("dataset_csv", exist_ok=True)
    os.makedirs(f"dataset_csv/{str_search}", exist_ok=True)  
    df = pd.DataFrame(article_dict) # Save All
    df.to_csv(f"dataset_csv/{str_search}/{str_search}_all.csv", index=False)