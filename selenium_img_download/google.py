from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import urllib.request



driver = webdriver.Chrome()
driver.get("https://www.google.co.kr/imghp?hl=ko&tab=ri&authuser=0&ogbl") #이미지 검색 url
elem = driver.find_element(By.NAME, "q")
elem.send_keys("조코딩")
elem.send_keys(Keys.RETURN)

# options = webdriver.ChromeOptions()
# options.add_experimental_option('excludeSwitches', ['enable-logging'])
# driver = webdriver.Chrome(executable_path='<path-to-chrome>', options=options)

SCROLL_PAUSE_TIME = 3

# Get scroll height
# 브라우저의 높이를 자바스크립트로 찾음(scrollHeight)
last_height = driver.execute_script("return document.body.scrollHeight")

while True: #
    # # 스크롤 내리면서 순서대로 저장할 때
    # images = driver.find_elements(By.CSS_SELECTOR,".rg_i.Q4LuWd")
    # count = 1
    # for image in images:
    #     try:
    #         image.click()
    #         time.sleep(3)
    #         imgUrl = driver.find_element(By.CSS_SELECTOR,".n3VNCb").get_attribute('src')
    #         # imgUrl = driver.find_element(By.XPATH,'''//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[3]/div/a/img''').get_attribute('src')
    #         urllib.request.urlretrieve(imgUrl, f'{str(count)}.jpg')
    #         count+=1
    #     except:
    #         pass
    # Scroll down to bottom
    # 브라우저 높이 끝까지 스크롤을 내리겠다
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME) # 0.5초 동안 페이지가 로딩 될 때가지 기다림

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height: # 이전 높이랑 같다면 더 이상 내릴 스크롤이 없는 것
        try:
            driver.find_elements(By.CSS_SELECTOR,".mye4qd").click()
        except:
            break
    last_height = new_height # if문이 안 걸리면 무한반복

# 작은 이미지
images = driver.find_elements(By.CSS_SELECTOR,".rg_i.Q4LuWd")
count = 1
for image in images:
    try:
        image.click()
        time.sleep()
        imgUrl = driver.find_element(By.CSS_SELECTOR,".n3VNCb").get_attribute('src')
        # imgUrl = driver.find_element(By.XPATH,'''//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[3]/div/a/img''').get_attribute('src')
        urllib.request.urlretrieve(imgUrl, f'{str(count)}.jpg')
        count+=1
    except:
        pass

driver.close()

