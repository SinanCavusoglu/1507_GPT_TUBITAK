import time 

import pandas as pd

import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

download_dir = "C:\\Users\\siren\\Desktop\\WebScraping_DS\\Diğer Kaynaklar\\Danıştay Dergisi\\PDFs"
chrome_options = webdriver.ChromeOptions()
prefs = {"download.default_directory": download_dir,
         "download.prompt_for_download": False,
         "plugins.always_open_pdf_externally": True}

chrome_options.add_experimental_option("prefs", prefs)
cService = webdriver.ChromeService(executable_path='C:/Users/siren/Desktop/WebScraping_DS/chromedriver.exe')

valid_numbers = list(range(109, 154))
url = 'https://www.danistay.gov.tr/danistay-dergiler'
driver = webdriver.Chrome(service = cService, options=chrome_options)
wait = WebDriverWait(driver, 20)

df_dict = {"JR_NO":[]}

driver.get(url)
driver.maximize_window()

boxes = driver.find_elements(by=By.XPATH, value='//*[@id="root"]/div/div[3]/div/div/div/div/div[2]/div')

for box in boxes:
    box_number = box.find_element(by=By.TAG_NAME, value='div').find_element(by=By.TAG_NAME, value='p').text
    if int(box_number) in valid_numbers:
        pdf_url = box.find_element(by=By.TAG_NAME, value='div').find_element(by=By.TAG_NAME, value='a')
        pdf_url.click()
        df_dict["JR_NO"].append(box_number)
        time.sleep(1.1)
        