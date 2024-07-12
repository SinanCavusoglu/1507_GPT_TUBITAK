import time 

import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException

df_dict = {"YEAR": [], "NUMBER": [], "CILT": []}

download_dir = "C:\\Users\\siren\\Desktop\\WebScraping_DS\\Barolar Birliği\\Miscellaneous JRs\\Kararlar Dergisi\\PDFs"
chrome_options = webdriver.ChromeOptions()
prefs = {
"download.default_directory": download_dir,
"download.prompt_for_download": False,
"plugins.always_open_pdf_externally": True}
chrome_options.add_experimental_option("prefs", prefs)

cService = webdriver.ChromeService(executable_path='C:/Users/siren/Desktop/WebScraping_DS/chromedriver.exe')

for year in range(1990, 2023):
    print("YEAR:", year)
    url = "https://www.anayasa.gov.tr/tr/yayinlar/kararlar-dergisi/?yil=2022&searchTags="
    driver = webdriver.Chrome(service=cService, options=chrome_options)
    driver.get(url = url)
    driver.maximize_window()
    
    # ---------- Select Year ---------- #
    year_list = driver.find_element(by=By.XPATH, value='//*[@id="yil"]')
    select_year = Select(year_list)
    select_year.select_by_value(str(year))
    
    rows = driver.find_element(by=By.XPATH, value='//*[@id="dergitum"]').find_elements(by=By.TAG_NAME,value="tr")
    for row in rows:
        td = row.find_elements(by=By.TAG_NAME, value="td")
        df_dict["YEAR"].append(td[-1])
        df_dict["NUMBER"].append(td[-2])
        df_dict["CILT"].append(td[-3])
    
        url_pdf = td[1].find_element(by=By.TAG_NAME, value="a").get_attribute("href")
        print(url_pdf)
        driver.get(url=url_pdf)
        time.sleep(5)
        
        