import time 

import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
download = True

df_dict = {"Thesis_No":[], "Thesis_Name":[], "Year":[], "URL_PDF":[]}

download_dir = "C:\\Users\\siren\\Desktop\\WebScraping_DS\\YÖK\\YOK_download_pdf"
chrome_options = webdriver.ChromeOptions()
prefs = {
"download.default_directory": download_dir,
"download.prompt_for_download": False,
"plugins.always_open_pdf_externally": True}
chrome_options.add_experimental_option("prefs", prefs)

cService = webdriver.ChromeService(executable_path='C:/Users/siren/Desktop/WebScraping_DS/chromedriver.exe')

for year in range(2006,2025): # Start 2006 
    print("YEAR:", year)
    url = "https://tez.yok.gov.tr/UlusalTezMerkezi/tarama.jsp#tabs-2"
    driver = webdriver.Chrome(service = cService, options=chrome_options)
    driver.get(url = url)
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)
    
    time.sleep(0.7)
    #---------- Detailed Search ----------#
    searching_word = driver.find_element(by=By.XPATH, value='//*[@id="tabs-2"]/form/table/tbody/tr/td/table/tbody/tr[3]/td[1]/input')
    searching_word.send_keys("Hukuk")
        
    searching_medium = driver.find_element(by=By.XPATH, value='//*[@id="tabs-2"]/form/table/tbody/tr/td/table/tbody/tr[3]/td[2]/select')
    select_medium = Select(searching_medium)
    select_medium.select_by_value('4')
        
    lang = driver.find_element(by=By.XPATH, value='//*[@id="tabs-2"]/form/table/tbody/tr/td/table/tbody/tr[3]/td[7]/select')
    select_lang = Select(lang)
    select_lang.select_by_value("1")
        
    year_list = driver.find_element(by=By.XPATH, value='//*[@id="tabs-2"]/form/table/tbody/tr/td/table/tbody/tr[2]/td[5]/select[1]')
    select_year = Select(year_list)
    select_year.select_by_value(str(year))
        
    perm = driver.find_element(by = By.XPATH, value='//*[@id="tabs-2"]/form/table/tbody/tr/td/table/tbody/tr[4]/td[5]/select')
    select_perm = Select(perm)
    select_perm.select_by_value("1")
    
    find = driver.find_element(by=By.XPATH, value='//*[@id="tabs-2"]/form/table/tbody/tr/td/table/tbody/tr[7]/td/input[2]')
    find.click()
    time.sleep(0.2) 

    while True:
    
        list_thesis = driver.find_elements(by=By.XPATH,value='//*[@id="div1"]/table/tbody/tr')
        
        for num,thesis in enumerate(list_thesis, start = 1): 
            #---------- Get Info ----------#
            row = thesis.find_elements(By.TAG_NAME, "td")
            thesis_no = row[1].text
            # ---------- Open PDF pop-up ---------- #
            pdf_value = thesis.get_attribute("span")
            try:
                click_detail_pdf = driver.find_element(by=By.XPATH, value=f'//*[@id="div1"]/table/tbody/tr[{num}]/td[2]/span') 
                driver.execute_script("arguments[0].click();", click_detail_pdf)
                time.sleep(0.5)
            except NoSuchElementException:
                print("All Theses are Finished")
                break
            except StaleElementReferenceException:
                click_detail_pdf = driver.find_element(by=By.XPATH, value=f'//*[@id="div1"]/table/tbody/tr[{num}]/td[2]/span') 
                driver.execute_script("arguments[0].click();", click_detail_pdf)
    
            
            pdf_url_btn = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="dialog-modal"]/p/table/tbody/tr[2]/td[2]/a'))) 
            try:
                pdf_url = "https://tez.yok.gov.tr/UlusalTezMerkezi/" + pdf_url_btn.get_attribute("href")
            except StaleElementReferenceException:
                pdf_url_btn = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="dialog-modal"]/p/table/tbody/tr[2]/td[2]/a')))
                pdf_url = "https://tez.yok.gov.tr/UlusalTezMerkezi/" + pdf_url_btn.get_attribute("href")
            
            if download == True:
               driver.execute_script("arguments[0].click();", pdf_url_btn)
            
            close_btn = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[1]/a'))) 
            close_btn.click()
            
            thesis_year = row[3]
            thesis_name = row[4].text.split("\n")[0]
    
            df_dict["Thesis_No"].append(thesis_no)
            df_dict["Thesis_Name"].append(thesis_name)
            df_dict["Year"].append(thesis_year)
            df_dict["URL_PDF"].append(pdf_url)
            
        next_page = driver.find_element(by=By.XPATH, value='//*[@id="div1"]/table/tfoot/tr/td/div/div[1]/div/ul/li[7]')
    
        if next_page.get_attribute("class") == "disabled":
            driver.close()
            break
        else:
            next_page_btn = next_page.find_element(By.TAG_NAME, "a")
            next_page_btn.click()
    
    
df = pd.DataFrame(df_dict)
df.to_csv("YOK_Article_CSV.csv", index = False)

