import time 

import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

# Hukuk, Adalet, Yargı, Dava, Kanun, Yasa
df_dict = {"BOOK_NAME":[], "BOOK_URL":[]}

download_dir = "C:\\Users\\siren\\Desktop\\WebScraping_DS\\Barolar Birliği\\kütüphane_kataloğu\\kütüphane_pdf"
chrome_options = webdriver.ChromeOptions()
prefs = {
"download.default_directory": download_dir,
"download.prompt_for_download": False,
"plugins.always_open_pdf_externally": True}
chrome_options.add_experimental_option("prefs", prefs)

cService = webdriver.ChromeService(executable_path='C:/Users/siren/Desktop/WebScraping_DS/chromedriver.exe')

url= "https://koha.barobirlik.org.tr:8080/cgi-bin/koha/opac-search.pl?advsearch=1&idx=kw&q=Yarg%C4%B1%C3%A7&op=or&idx=kw&q=%C4%B0htar&op=or&idx=kw&q=Adalet&op=or&idx=kw&q=Anayasa&op=or&idx=kw&q=Avukat&op=or&idx=kw&q=Dan%C4%B1%C5%9Ftay&op=or&idx=kw&q=Dava&op=or&idx=kw&q=Hakim&op=or&idx=kw&q=Hukuk&op=or&idx=kw&q=Kadastro&op=or&idx=kw&q=Kanun&op=or&idx=kw&q=Mahkeme&op=or&idx=kw&q=Tazminat&op=or&idx=kw&q=Savc%C4%B1&op=or&idx=kw&q=Yarg%C4%B1tay&op=or&idx=kw&q=Temyiz&limit=mc-itype%2Cphr%3AEBK&sort_by=relevance&limit-yr=2006-&limit=ln%2Crtrn%3Atur&do=Ara"

# I set the search parameter manually

driver = webdriver.Chrome(service=cService, options=chrome_options)
driver.get(url=url)
page_num = 0
while True:
    page_num += 1
    print("page num:", page_num)
    # Box Name
    boxes = driver.find_element(by=By.XPATH, value='//*[@id="bookbag_form"]/table/tbody').find_elements(by=By.TAG_NAME, value='tr')
    for box in boxes:
        box = box.find_element(by=By.CLASS_NAME, value='title_summary')
        book_name = box.find_element(by=By.TAG_NAME, value="a").text
        book_url_main = box.find_element(By.CLASS_NAME, "results_summary.online_resources")
        
        book_url = book_url_main.find_element(by=By.TAG_NAME, value="a").get_attribute("href")
        book_url_available = book_url_main.find_element(by=By.TAG_NAME, value="a").text
        
        if book_url_available == "Kitabın elektronik haline erişmek için tıklayınız.":
            df_dict["BOOK_NAME"].append(book_name)
            df_dict["BOOK_URL"].append(book_url)

    # Change Page
    page_slider = driver.find_element(by=By.XPATH, value='//*[@id="bottom-pages"]/nav/ul')
    next_btn = page_slider.find_elements(by=By.TAG_NAME, value="li")[-2]
    if next_btn.find_element(by=By.TAG_NAME, value="a").get_attribute("aria-label") == "Sonraki sayfaya git":
        next_btn.click()
    else:
        print("Last_Page")
        break

df = pd.DataFrame(df_dict)
df.to_csv("barolarbirligi.csv", index = False)