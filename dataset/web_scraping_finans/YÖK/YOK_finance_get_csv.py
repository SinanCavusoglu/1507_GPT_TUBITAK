import os
import time 

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
# Ekonomi = Economics", "Maliye = Finance"
subject_list = ["Ev Ekonomisi = Home Economics", "Uluslararası Ticaret = International Trade"]
                
for subject in subject_list:
    download = True
    dir_name = subject.split("=")[0].strip()
    os.makedirs(f"C:/Users/siren/Desktop/1507/dataset/web_scraping_finans/YÖK/YÖK_pdf/{dir_name}", exist_ok=True)
    download_dir = f"C:/Users/siren/Desktop/1507/dataset/web_scraping_finans/YÖK/YÖK_pdf/{dir_name}"
    download_dir = download_dir.replace("/", "\\")
    chrome_options = webdriver.ChromeOptions()
    prefs = {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "plugins.always_open_pdf_externally": True}
    chrome_options.add_experimental_option("prefs", prefs)

    cService = webdriver.ChromeService(executable_path=r'C:\Users\siren\Desktop\1507\dataset\chromedriver.exe')


    for year in range(2006,2025): # Start 2006 
        
        print("SUBJECT:", subject)
        print("YEAR:", year)
        url = "https://tez.yok.gov.tr/UlusalTezMerkezi/tarama.jsp"
        driver = webdriver.Chrome(service = cService, options=chrome_options)
        driver.get(url = url)
        driver.maximize_window()
        wait = WebDriverWait(driver, 10)
    
        #---------- Detailed Search ----------#
        
        searching_word = driver.find_element(by=By.XPATH, value='//*[@id="konu"]')
        searching_word.send_keys(subject)
            
        lang = driver.find_element(by=By.XPATH, value='//*[@id="tabs-1"]/form/table/tbody/tr/td/table/tbody/tr[5]/td[4]/select')
        select_lang = Select(lang)
        select_lang.select_by_value("1")
            
        year_list = driver.find_element(by=By.XPATH, value='//*[@id="tabs-1"]/form/table/tbody/tr/td/table/tbody/tr[2]/td[6]/select[1]')
        select_year = Select(year_list)
        select_year.select_by_value(str(year)) 
        
        perm = driver.find_element(by = By.XPATH, value='//*[@id="tabs-1"]/form/table/tbody/tr/td/table/tbody/tr[3]/td[4]/select')
        select_perm = Select(perm)
        select_perm.select_by_value("1")
        
        find = driver.find_element(by=By.XPATH, value='//*[@id="tabs-1"]/form/table/tbody/tr/td/table/tbody/tr[8]/td/input[3]') 
        
        find.click()
        time.sleep(2)

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
                    time.sleep(2)
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
                time.sleep(2)
                close_btn.click()
                
            next_page = driver.find_element(by=By.XPATH, value='//*[@id="div1"]/table/tfoot/tr/td/div/div[1]/div/ul/li[7]')
        
            if next_page.get_attribute("class") == "disabled":
                
                time.sleep(10)
                driver.close()
                break
            else:
                next_page_btn = next_page.find_element(By.TAG_NAME, "a")
                next_page_btn.click()
        


