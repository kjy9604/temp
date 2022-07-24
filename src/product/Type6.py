from . import Crawler
from bs4 import BeautifulSoup as bs
import random
import time
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from util import DriverUtil

class Type6(Crawler.Crawler):
    def crawl(self, query, word, url_mid):
        driver = DriverUtil.DriverUtil.getDriver()
        print('Type6')
        # 체류시간
        randTime = random.randrange(60, 91)
        print(f"{randTime}초 체류 예정")

        # query로 받은 것중 하나를 검색어로 처리
        # 이후 query의 반점을 전부 + 처리해야함
        # query 받은걸 배열로 변환 후 random으로 하나 찝어냄
        arr = query.split(',')
        arrLen = len(arr)
        randNum = random.randrange(0, arrLen)
        randQuery = arr[randNum]

        replaceQuery = query.replace(',', '+')

        
        if (driver is None):
            DriverUtil.DriverUtil.connection()
        else:
            DriverUtil.DriverUtil.changeIp()

        url = f"https://search.naver.com/search.naver?display=15&f=&filetype=0&page=2&query={replaceQuery}&oquery={randQuery}&research_url=&sm=tab_pge&start=1&where=web"
        flag = False
        rank = "X"
        click = False
        href = ""

        driver.get(url)
        time.sleep(5)

        # 지정한 위치로 스크롤 내리기
        # 1080 해상도인 경우, 1080 위치로 한페이지를 스크롤한다
        driver.execute_script("window.scrollTo(0,1080)")

        # 화면 가장 하단으로 스크롤 내리기
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

        elements = driver.find_elements_by_partial_link_text(word)

        for index, element in enumerate(elements, 1):
            print("{} 번째 게시글의 제목: {}".format(index, element.text))
            if (url_mid in element.text) :
                print("True!!")
                print(element.text)
                print(element.get_attribute('href'))
                href = element.get_attribute('href')
                flag = True
                break

        if (flag != True) :
            url2 = f"https://search.naver.com/search.naver?display=15&f=&filetype=0&page=3&query={replaceQuery}&oquery={randQuery}&research_url=&sm=tab_pge&start=16&where=web"
            driver.get(url2)
            driver.execute_script("window.scrollTo(0,1080)")
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            elements2 = driver.find_elements_by_partial_link_text(word)
            for index, element in enumerate(elements2, 16):
                print("{} 번째 게시글의 제목: {}".format(index, element.text))
                if (url_mid in element.text) :
                    print("True!!")
                    flag = True
                    href = element.get_attribute('href')
                    break
                
        if (flag == True) :
            link = driver.find_element_by_xpath('//a[@href="'+href+'"]')
            link.click()
            time.sleep(5)
            max_time_end = time.time() + randTime
            while True :
                # 가장 아래로 스크롤 이동
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

                # 페이지 로딩 대기
                time.sleep(2)

                # 현재 문서 높이를 가져와서 저장
                curr_height = driver.execute_script("return document.body.scrollHeight")

                prev_height = curr_height
                driver.execute_script("window.scrollTo(0, 0)")
                if time.time() > max_time_end :
                    break

            driver.back()
            time.sleep(2)
            DriverUtil.DriverUtil.closeSelenium()
            return "done"
        else :
            DriverUtil.DriverUtil.closeSelenium()
            return str(rank)