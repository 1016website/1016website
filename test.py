from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager # 매번 크롬드라이버를 깔아서 최신버전에 맞추는 번잡함을 방지하기 위해 크롬드라이버매니저를 설치
import time

# 옵션 생성
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
service = Service(ChromeDriverManager().install())
options.add_argument("headless")
driver = webdriver.Chrome(service=service, options=options)

url = "https://naver.com"
# 창 숨기는 옵션 추가

driver.get(url)




# driver.find_element(By.CLASS_NAME, "input_text").send_keys("블랙핑크")
# time.sleep(1)
#
# driver.find_element(By.ID, "query").send_keys("뉴진스")
# time.sleep(1)
#
# driver.find_element(By.NAME, "query").send_keys("트와이스")
# time.sleep(1)
#
# driver.find_element(By.CSS_SELECTOR, "#query").send_keys("에스파")
# time.sleep(1)
#
# driver.find_element(By.XPATH, '//*[@name="query"]').send_keys("에스파")
# time.sleep(1)

# driver.find_element(By.LINK_TEXT, "뉴스").click()
# 
# navs = driver.find_elements(By.CLASS_NAME, ".cjs_news_a")
#
#
# driver.find_element(By.CSS_SELECTOR, ".nav.shop").click()
#
# time.sleep(1)

navs = driver.find_elements(By.CSS_SELECTOR,".nav")
for nav in navs:
    print(nav.get_attribute("outerHTML"))
    print()