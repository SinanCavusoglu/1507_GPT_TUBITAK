import os
import pandas as pd

import requests
from bs4 import BeautifulSoup

def key_word_list(file_dir):
    # Prepare the key-words list
    with open(file_dir, "r") as file:
        words_list = [word.strip("\n") for word in file.readlines()]
    return words_list 

def total_page_num(word):
    # Return max number of pages
    url = f"https://search.trdizin.gov.tr/en/publication/search?q=title%3A%28{search_str}%29+journalName%3A%28{search_str}%29&searchName=&order=year-DESC&facet-accessStatus=%5B*+TO+NOW%5D&facet-publicationLanguage=tur&page=1&limit=100"
    page = requests.get(url, timeout = 300)
    soup = BeautifulSoup(page.text, "lxml")
    page_slider = soup.find("input", {"onchange":"APP.submit(this,form);"})
    max_ = page_slider["max"] if page_slider else 0
    return int(max_)

def box_extract(box):
    # Extract Article Info
    article_name = box.find("div", class_ = "result-content").find("div", class_ = "result-title").find("a").text                      # Article Name
    
    art_or_pr = box.find("div", class_ = "result-journal")
    journal_name = art_or_pr.find("a").text if art_or_pr else "Proje"                                                                  # Journal Name
    
    result_info = box.find("div", class_ = "result-content").find("div", class_ = "result-info")                                       # PDF URL
    try:
        pdf_js = result_info.find_all("a", class_ = "me-4")[1] if result_info else None                     
    except IndexError:
        pdf_js = result_info.find_all("a", class_ = "me-4")[0] if result_info else None
    
    article_det = box.find("div", class_ = "result-title").find("a", class_ = "search-item")["href"]
    article_det = "https://search.trdizin.gov.tr/en"+article_det
    
    return article_name.strip(), journal_name.strip(), pdf_js, article_det

file_dir = "key_words.txt"  # List of searching key-words
words_list = key_word_list(file_dir)
search_str = "+OR+".join(words_list)

article_dict = {"Page_Number" : [],"Article_Name": [], "Article_Journal": [], "Article_PDF_URL": [], "Article_Detail": []}
max_number = total_page_num(search_str)
if max_number == 0:
    print("There is no such category in TRDizin")
elif max_number > 0:
    for page_num in range(1, max_number+1):
        url = f"https://search.trdizin.gov.tr/en/publication/search?q=abstract%3A%28{search_str}%29+title%3A%28{search_str}%29+journalName%3A%28{search_str}%29&searchName=&order=year-DESC&facet-accessStatus=%5B*+TO+NOW%5D&facet-publicationLanguage=tur&page={page_num}&limit=100"
        page = requests.get(url, timeout = 999)
        soup = BeautifulSoup(page.text, "lxml")
        print(max_number)
        print(f"{page} - {page_num}/{max_number}")
        # ---------- BOXES ---------- #
        boxes = soup.find_all("div", class_ = "result-item mb-4")
        
        for box in boxes:

            article_name, journal_name, pdf_js, article_det = box_extract(box)
            
            article_dict["Page_Number"].append(page_num) 
            article_dict["Article_Name"].append(article_name)
            article_dict["Article_Journal"].append(journal_name)
            article_dict["Article_PDF_URL"].append(str(pdf_js))
            article_dict["Article_Detail"].append(article_det)
            
            
    os.makedirs("dataset", exist_ok = True)
    df = pd.DataFrame(article_dict)
    df.to_csv("dataset/dataset_csv.csv", index=False)
