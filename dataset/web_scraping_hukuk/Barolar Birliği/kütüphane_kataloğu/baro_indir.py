import time 

import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


download_dir = "C:\\Users\\siren\\Desktop\\WebScraping_DS\\Barolar Birliği\\kütüphane_kataloğu\\kütüphane_pdf"
chrome_options = webdriver.ChromeOptions()
prefs = {
"download.default_directory": download_dir,
"download.prompt_for_download": False,
"plugins.always_open_pdf_externally": True}
chrome_options.add_experimental_option("prefs", prefs)

cService = webdriver.ChromeService(executable_path='C:/Users/siren/Desktop/WebScraping_DS/chromedriver.exe')
driver = webdriver.Chrome(service=cService, options=chrome_options)

df = pd.read_csv("barolarbirligi.csv")
url_list = df.BOOK_URL.to_list()

for url in url_list:
    driver.get(url=url)
    

