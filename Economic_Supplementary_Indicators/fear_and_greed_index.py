import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

# WebDriver 설정
options = Options()
options.add_argument("--headless")  # 옵션: 화면 없이 실행 (필요시)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# URL 접속
driver.get(url="https://edition.cnn.com/markets/fear-and-greed")

# 자바스크립트를 사용해 페이지 로딩 대기
#while driver.execute_script("return document.readyState") != "complete":
#    time.sleep(1)

# 요소 찾기
try:
    idx = driver.find_element(By.CLASS_NAME, value="market-fng-gauge__dial-number-value").text
    # 빈 문자열 확인
    if idx.strip() == '':
        print("값이 비어있습니다.")
    else:
        idx = int(idx)  # 정수로 변환
        print(idx)
finally:
    driver.quit()  # 브라우저 종료
