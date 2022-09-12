from errno import ESTALE
from operator import index
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import csv
import os
from selenium.webdriver.common.keys import Keys
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning) # concat 쓰라는 경고 무시

'''
텔레그램 알림
'''

import telegram

chat_token = "5613827266:AAEyJ5wM9opn2tEHJvbtwqfPROTysgOnzAg"

bot = telegram.Bot(token = chat_token)

chat_id = 1666417159


try:
  URL = 'http://www.kyobobook.co.kr/bestSellerNew/bestseller.laf?mallGb=KOR&linkClass=c&range=1&kind=2&orderClick=DAd' 
  
  options = webdriver.ChromeOptions()
  options.add_experimental_option("excludeSwitches", ["enable-logging"])
  driver = webdriver.Chrome(options=options)

  # driver = webdriver.Chrome('/Users/boyeonjang/git/kyobobook-review/chromedriver')
  # driver = webdriver.Chrome('C:/Users/eunho/Workspace/kyobobook-review/chromedriver.exe')
  driver.get(url=URL)


  # df 선언
  df = pd.DataFrame(columns=['part','title','date','rating','text'])

  part_xpath = driver.find_element(By.XPATH, '''//*[@id="main_contents"]/div[3]/h4''')
  part = part_xpath.text
  partName = part.split()[0]
  print('part: ', partName)

  for book in range(1, 21): # top 20
    sleep(1)
    driver.find_element(By.XPATH, f'''//*[@id="main_contents"]/ul/li[{book}]/div[2]/div[2]/a''').send_keys(Keys.ENTER) # 책 제목 클릭
    sleep(1.5)
    title_xpath = driver.find_element(By.XPATH, '''//*[@id="container"]/div[2]/form/div[1]/h1/strong''') # 책 제목
    title = title_xpath.text

    try:
      driver.find_element(By.XPATH, '''//*[@id="event_info"]/li[3]/a''').send_keys(Keys.ENTER) # 리뷰 클릭
      # sleep(3)
      # driver.find_element(By.XPATH, '''//*[@id="detailFixedTab"]/div/div[1]/ul/li[3]/a''').send_keys(Keys.ENTER)
    except:
      driver.find_element(By.XPATH, '''//*[@id="book_info"]/li[2]/a''').send_keys(Keys.ENTER) # 리뷰 클릭
    sleep(3)

    # 페이지가 다음으로 넘어가면
    for n in range(1, 62): # 60페이지까지만 수집
      print(">>n: ",n)
      if n == 61:
          break
      try:
        sleep(1)
        for idx in range(1, 6): # 리뷰 5개씩
          rating_xpath = driver.find_element(By.XPATH, f'''//*[@id="box_detail_review"]/ul/li[{idx}]/div[1]/dl/dd[3]/span''') # 별점
          text_xpath = driver.find_element(By.XPATH, f'''//*[@id="box_detail_review"]/ul/li[{idx}]/div[1]/dl/dd[5]/div''') # 리뷰 글
          date_xpath = driver.find_element(By.XPATH, f'''//*[@id="box_detail_review"]/ul/li[{idx}]/div[1]/dl/dd[1]''') # 날짜
          
          rating = rating_xpath.text
          text = text_xpath.text
          date = date_xpath.text
          print('title: ', title)
          print('date: ', date)
          print('rating: ', rating)
          print('text: ', text)
          sleep(1)
          df = df.append({'part':partName, 'title':title, 'date':date, 'rating':rating, 'text':text},ignore_index=True)
          #df = df.append(more) => df = pd.concat([df, more]) #concat으로 바꿀 때 참고

          sleep(1)

        page_bar = driver.find_elements(By.CSS_SELECTOR,'#box_detail_review > div.list_paging.align_center > div >*')
        pn = len(page_bar)

        # if n != 0 :
        print(f'============= {n+1} 페이지의 리뷰 5개 =============')
        page_bar[pn-2].send_keys(Keys.ENTER)
        
      except:
        print('============= 다음 페이지가 없습니다 =============')
        break
    
    driver.back()
    sleep(0.5)
    driver.back()
    sleep(0.5)

  df.to_csv(f"./{partName}_top20_ok.csv", encoding='utf-8-sig')

  # done_book = df['title'].unique()

  # end_text = '코드 종료\n'+ done_book 
  end_text = '코드 종료\n'
  bot.sendMessage(chat_id=chat_id, text=end_text)
except Exception as e:
  print("!!!---예외가 발생했습니다.--- : ", e, '-----!!!!')
  df.to_csv(f"./{partName}_top{n}_no.csv", encoding='cp949')
  bot.sendMessage(chat_id=chat_id, text='예외발생')