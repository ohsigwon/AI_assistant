from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

chromedriver_path = r'C:\Users\a0105\OneDrive\바탕 화면\파이썬 연습\p j c\chromedriver.exe'  # 또는 'C:\\Users\\a0105\\OneDrive\\바탕 화면\\파이썬 연습\\p j c\\chromedriver.exe'
service = Service(chromedriver_path)

driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get('https://gyeseong.riroschool.kr/user.php?action=signin')

try:
    driver.find_element(By.XPATH, '//*[@id="id"]').send_keys('22-10105')
    time.sleep(0.5)
    driver.find_element(By.XPATH, '//*[@id="pw"]').send_keys('kis60516!')
    time.sleep(0.5)

    login_button = driver.find_element(By.XPATH, '//*[@id="container"]/div/section/div[2]/div[2]/form/button')  # 로그인 버튼의 XPath 사용
    login_button.click()
    
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="container"]')))
except Exception as e:
    print(f"로그인 실패: {e}")
    driver.quit()
    exit()
    
    try:
        driver.find_element(By.XPATH, '//*[@id="container"]/div/ul[4]/li[1]/svg').click()  # 예: '//*[@id="menu"]/ul/li[1]/a'
        
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="container"]/div/div[2]/table/tbody/tr[2]/td[3]/a[2]')))  # 예: '//*[@id="container"]/div/div[2]/table/tbody/tr[3]/td[3]/a[2]'
        
        rows = driver.find_elements(By.XPATH, '//*[@id="container"]/div/div[2]/table/tbody/tr')
        
        print("수행평가 데이터:")
        for row in rows:
            try:
                title = row.find_element(By.XPATH, './td[3]/a[2]').text  # 제목의 XPath
                due_date = row.find_element(By.XPATH, './td[7]/strong').text  # 마감일의 XPath
                print(f"제목: {title}, 마감일: {due_date}")
            except Exception as e:
                print(f"수행평가 데이터 가져오기 실패: {e}")
    
    except Exception as e:
        print(f"수행평가 페이지로 이동 실패: {e}")
    
    driver.get('https://gyeseong.riroschool.kr/main_page_url')  # 실제 메인 페이지 URL로 교체
    
except Exception as e:
    print(f"오류 발생: {e}")

finally:
    driver.quit()
