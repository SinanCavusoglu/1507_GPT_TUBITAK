import time 

import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

df_dict = {"JR_Name":[], "JR_URL":[]}

download_dir = "C:\\Users\\siren\\Desktop\\WebScraping_DS\\Barolar Birliği\\istanbul_barosu\\istanbul_barosu_dergisi\\istanbul_baro_pdf"
chrome_options = webdriver.ChromeOptions()
prefs = {
"download.default_directory": download_dir,
"download.prompt_for_download": False,
"plugins.always_open_pdf_externally": True}
chrome_options.add_experimental_option("prefs", prefs)

cService = webdriver.ChromeService(executable_path='C:/Users/siren/Desktop/WebScraping_DS/chromedriver.exe')

url = "https://www.istanbulbarosu.org.tr/Yayinlar.aspx"
driver = webdriver.Chrome(service = cService, options=chrome_options)

driver.get(url=url)
driver.maximize_window()

baro_jr_btn = driver.find_element(by=By.XPATH, value='//*[@id="baroDergileri"]/a')
baro_jr_btn.click()
time.sleep(3)
boxes_main =  driver.find_element(by=By.XPATH, value='//*[@id="dvTest"]/ul')
boxes = boxes_main.find_elements(by=By.TAG_NAME, value='li')

for box in boxes:
    box_main = box.find_element(by=By.TAG_NAME, value='a')
    jr_url = box_main.get_attribute("href")
    jr_name = box_main.find_element(by=By.TAG_NAME, value='div').text
    df_dict["JR_Name"].append(jr_name)
    df_dict["JR_URL"].append(jr_url)
    if jr_name == "Özel Sayı 1:Ceza":
        break
    
df = pd.DataFrame(df_dict)
df.to_csv("istanbulBaroDergi.csv", index=False)

jr_list = df.JR_URL.to_list()
for jr in jr_list:
    driver.get(jr)
    time.sleep(0.8)