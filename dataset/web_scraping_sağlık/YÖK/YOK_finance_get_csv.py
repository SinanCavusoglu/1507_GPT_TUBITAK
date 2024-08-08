
import os
import time 

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
# "Acil Tıp = Emergency Medicine", "Adli Tıp = Forensic Medicine", "Aile Hekimliği = Family Medicine", !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!BİTTİ
# "Allerji ve İmmünoloji = Allergy and Immunology", !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!BİTTİ
# "Anatomi = Anatomy",!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!BİTTİ
# "Anestezi ve Reanimasyon = Anesthesiology and Reanimation", !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!BİTTİ
# "Askeri Sağlık Hizmetleri = Military Health Services", !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!BİTTİ
# "Besin Hijyeni ve Teknolojisi = Food Hygiene and Technology", !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!BİTTİ
# "Beslenme ve Diyetetik = Nutrition and Dietetics", !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!BİTTİ
# "Biyofizik = Biophysics", !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!BİTTİ
# "Biyoistatistik = Biostatistics", !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!BİTTİ
# "Biyokimya = Biochemistry", !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!BİTTİ
# "Biyoloji = Biology", !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!BİTTİ
# "Çocuk Cerrahisi = Pediatric Surgery", !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!BİTTİ
# "Çocuk Sağlığı ve Hastalıkları = Child Health and Diseases"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!BİTTİ
# "Deontoloji ve Tıp Tarihi = Medical History and Ethics", !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!BİTTİ
# "Dermatoloji = Dermatology", !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!BİTTİ
# "Diş Hekimliği = Dentistry", !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!BİTTİ
# "Ebelik = Midwifery", !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!BİTTİ
# "Eczacılık ve Farmakoloji = Pharmacy and Pharmacology", !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!BİTTİ
# "Endokrinoloji ve Metabolizma Hastalıkları = Endocrinology and Metabolic Diseases",!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!BİTTİ
# "Enfeksiyon Hastalıkları ve Klinik Mikrobiyoloji = Infectious Diseases and Clinical Microbiology",!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!BİTTİ
# "Ergoterapi = Occupational Therapy", !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!BİTTİ
# "Farmasötik Toksikoloji = Pharmaceutical Toxicology",!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!BİTTİ
# "Fiziksel Tıp ve Rehabilitasyon = Physical Medicine and Rehabilitation", !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!BİTTİ
# "Fizyoloji = Physiology",!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!BİTTİ
# "Fizyopatoloji = Physiopathology", !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!BİTTİ
# "Fizyoterapi ve Rehabilitasyon = Physiotherapy and Rehabilitation",!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!BİTTİ
# "Gastroenteroloji = Gastroenterology", !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!BİTTİ
# "Genel Cerrahi = General Surgery",!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!BİTTİ
# "Geriatri = Geriatrics", !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!BİTTİ
# "Göğüs Cerrahisi = Thoracic Surgery",!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!BİTTİ
# "Göğüs Hastalıkları = Chest Diseases", !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!BİTTİ
# "Göğüs Kalp ve Damar Cerrahisi = Thoracic and Cardiovascular Surgery",!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!BİTTİ
# "Göz Hastalıkları = Eye Diseases", !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!BİTTİ
# "Halk Sağlığı = Public Health", !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!BİTTİ
# "Hastaneler = Hospitals",!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!BİTTİ
# "Hematoloji = Hematology", !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!BİTTİ
# "Hemşirelik = Nursing", !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!BİTTİ

# "Histoloji ve Embriyoloji = Histology and Embryology",

# "İç Hastalıkları = Internal diseases", !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!BİTTİ
# "İlk ve Acil Yardım = Emergency and First Aid",!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!BİTTİ
# "Kadın Hastalıkları ve Doğum = Obstetrics and Gynecology", !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!BİTTİ
# "Kardiyoloji = Cardiology", !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!BİTTİ
# "Kulak Burun ve Boğaz = Otorhinolaryngology (Ear-Nose-Throat)",!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!BİTTİ

# "Mikrobiyoloji = Microbiology", 
# "Moleküler Tıp = Molecular Medicine",
# "Morfoloji = Morphology", 
# "Nefroloji = Nephrology", 
# "Nöroloji = Neurology", 
# "Nöroşirürji = Neurosurgery", 
# "Onkoloji = Oncology", 
# "Ortopedi ve Travmatoloji = Orthopedics and Traumatology", 
# "Parazitoloji = Parasitology", 
# "Patoloji = Pathology", 
# "Plastik ve Rekonstrüktif Cerrahi = Plastic and Reconstructive Surgery",

# "Psikiyatri = Psychiatry", !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!BİTTİ
# "Psikoloji = Psychology", !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!BİTTİ
# "Radyasyon Onkolojisi = Radiation Oncology", !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!BİTTİ
# "Radyoloji ve Nükleer Tıp = Radiology and Nuclear Medicine", !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!BİTTİ
# "Romatoloji = Rheumatology", !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!BİTTİ
# "Sağlık Eğitimi = Health Education", !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!BİTTİ
# "Sağlık Kurumları Yönetimi = Health Care Management",!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!BİTTİ
# "Sağlık Yönetimi = Healthcare Management", 
# "Tıbbi Biyoloji = Medical Biology", 
# "Üroloji = Urology"

subject_list = ["Göz Hastalıkları = Eye Diseases", 
                "Halk Sağlığı = Public Health", 
                "Hastaneler = Hospitals",
                "Hematoloji = Hematology", 
                "Hemşirelik = Nursing", 
                "Histoloji ve Embriyoloji = Histology and Embryology"]
  
for subject in subject_list:
    download = True
    dir_name = subject.split("=")[0].strip()
    os.makedirs(f"C:/tubitak_1507/1507_GPT_TUBITAK/dataset/web_scraping_sağlık/YÖK/YÖK_pdf/{dir_name}", exist_ok=True)
    download_dir = f"C:/tubitak_1507/1507_GPT_TUBITAK/dataset/web_scraping_sağlık/YÖK/YÖK_pdf/{dir_name}"
    download_dir = download_dir.replace("/", "\\")
    chrome_options = webdriver.ChromeOptions()
    prefs = {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "plugins.always_open_pdf_externally": True}
    chrome_options.add_experimental_option("prefs", prefs)
    
    cService = webdriver.ChromeService(executable_path=r'C:\tubitak_1507\1507_GPT_TUBITAK\dataset\chromedriver.exe')


    for year in range(2007,2025): # Start 2007 
        
        print("SUBJECT:", subject)
        print("YEAR:", year)
        url = "https://tez.yok.gov.tr/UlusalTezMerkezi/tarama.jsp"
        driver = webdriver.Chrome(service = cService, options=chrome_options)
        driver.get(url = url)
        driver.maximize_window()
        wait = WebDriverWait(driver, 5)
    
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
        time.sleep(1)
        no_elm = 0
        while True:
        
            
            list_thesis = driver.find_elements(by=By.XPATH,value='//*[@id="div1"]/table/tbody/tr')
            
            for num,thesis in enumerate(list_thesis, start = 1): 
                #---------- Get Info ----------#
                row = thesis.find_elements(By.TAG_NAME, "td")
                #thesis_no = row[1].text
                #if int(thesis_no) == 733263:
                #    continue
                # ---------- Open PDF pop-up ---------- #
                pdf_value = thesis.get_attribute("span")
                try:
                    click_detail_pdf = wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@id="div1"]/table/tbody/tr[{num}]/td[2]/span')))
                    time.sleep(1.3)
                    driver.execute_script("arguments[0].click();", click_detail_pdf)
                except NoSuchElementException:
                    print("All Theses are Finished")
                    break
                
                except TimeoutException:
                    no_elm += 1
                    if no_elm == 5:
                        break
                    print("No such elements")
                    continue
                    
                try:
                    pdf_url_btn = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="dialog-modal"]/p/table/tbody/tr[2]/td[2]/a')))
                except TimeoutException:
                    print("No pdf button")
                    continue
                if download == True:
                    try:
                        driver.execute_script("arguments[0].click();", pdf_url_btn)
                    except StaleElementReferenceException:
                        print("Stale Element Problem")
                        continue
                close_btn = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[1]/a'))) 
                time.sleep(1.3)
                close_btn.click()
            try:
                next_page = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="div1"]/table/tfoot/tr/td/div/div[1]/div/ul/li[7]')))
            except Exception as e:
                print(f"Error: {e}")
                break
            if next_page.get_attribute("class") == "disabled":
                
                time.sleep(1.5)
                driver.close()
                break
            else:
                next_page_btn = next_page.find_element(By.TAG_NAME, "a")
                next_page_btn.click()
        


