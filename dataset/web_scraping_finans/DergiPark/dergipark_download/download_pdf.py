import time 

import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import InvalidArgumentException

def download_pdf_DP(csv):
    download_dir = "C:\\Users\\siren\\Desktop\\1507\\dataset\\web_scraping_finans\\DergiPark\\dergipark_download\\DergiPark_PDF"
    chrome_options = webdriver.ChromeOptions()
    prefs = {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "plugins.always_open_pdf_externally": True}
    chrome_options.add_experimental_option("prefs", prefs)
    
    cService = webdriver.ChromeService(executable_path='C:/Users/siren/Desktop/1507/dataset/chromedriver.exe')
   

    url_list = csv.Article_PDF_URL.to_list()
    for url in url_list:
        driver = webdriver.Chrome(service = cService, options=chrome_options)
        try:
            driver.get(url)
        except InvalidArgumentException:
            continue
        driver.maximize_window()
        print(url)
        try:
          
            download_button = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="download"]'))
            )
            download_button.click()
            time.sleep(0.7)
        except Exception as e:
            print(f"Failed to download {url}: {e}")
        finally:
            driver.quit()
"""
def download_pdf_TRDizin(csv):
    download_dir = "C:\\Users\\siren\\Desktop\\WebScraping_DS\\DP-TRDizin\\PDF-s\\TRDizin_PDF"
    chrome_options = webdriver.ChromeOptions()
    prefs = {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "plugins.always_open_pdf_externally": True}
    chrome_options.add_experimental_option("prefs", prefs)
    
    cService = webdriver.ChromeService(executable_path='C:/Users/siren/Desktop/WebScraping_DS/chromedriver.exe')

    trdizin_url_list = csv.Article_Detail.to_list()
    for url in trdizin_url_list:
        driver = webdriver.Chrome(service = cService, options=chrome_options)
        driver.get(url)
        driver.maximize_window()
        time.sleep(0.8)
        
        #try:
          
        get_href = WebDriverWait(driver, 200).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/div[2]/div/div/div/div/div[1]/div[2]/a[2]')) 
        )
        download_button = get_href.get_attribute("href")
        driver.execute_script(download_button)

        driver.switch_to.window(driver.window_handles[1])
        
        download_button = WebDriverWait(driver, 200).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="download"]'))
        )
        download_button.click()
        time.sleep(3.5)
    #except Exception as e:
        #print(f"Failed to click and download {url}: {e}")
    #finally:
        driver.quit()
"""


pdf_df = pd.read_csv(r"C:\Users\siren\Desktop\1507\dataset\web_scraping_finans\DergiPark\dergipark_download\noDupDergipark.csv")

pdf_df_index = pdf_df[pdf_df["Article_PDF_URL"] == "https://dergipark.org.tr/tr/download/article-file/873410"].index[0].tolist()
pdf_df = pdf_df.iloc[pdf_df_index:]
#dergipark_pdf_csv = pdf_df[pdf_df.Source == "DergiPark"]
#trdizin_pdf_csv = pdf_df[pdf_df.Source == "TRDizin"]
#trdizin_pdf_csv = trdizin_pdf_csv[1335:]

download_pdf_DP(csv=pdf_df)
#download_pdf_TRDizin()

