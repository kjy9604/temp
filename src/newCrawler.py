from abc import ABCMeta, abstractmethod
import random
import subprocess
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
from bs4 import BeautifulSoup as bs

def connection(): 

    # IP Change
    subprocess.Popen(['systemctl', 'reload']+['tor']).wait()
    print('tor reload')
    time.sleep(2)

    temp = True
    num = 0 # 커넥션 시도 회수
    while temp and num < 90:
        try:
            num += 1
            print(num)
            # selenium option
            PROXY="localhost:9050"
            opts = Options()
            user_agent = 'Mozilla/5.0 CK={} (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'

            webdriver.DesiredCapabilities.CHROME['proxy'] = {
                "httpProxy": PROXY,
                "ftpProxy": PROXY,
                "sslProxy": PROXY,
                "proxyType": "MANUAL"
            }

            # soup option
            proxies = {
                'http': 'socks5://127.0.0.1:9050',
                'https': 'socks5://127.0.0.1:9050'
            }
            webdriver.DesiredCapabilities.CHROME['acceptSslCerts']=True

            opts.add_argument("user-agent="+user_agent)
            # 추가옵션 - 임시로 주석
            opts.add_argument('--headless')
            opts.add_argument('--no-sandbox')
            opts.add_argument('--proxy-server='"socks5://"+PROXY)
            opts.binary_location = '/usr/bin/google-chrome'

            url = "http://wtfismyip.com/text"
            driver =webdriver.Chrome(executable_path="../chromedriver",options=opts)
            driver.create_options()
            driver.get(url)
            temp = False
        except Exception as e:
            print(e)
            driver.quit()
    return driver

def closeAllChrome(driver):
	driver.delete_all_cookies()
	driver.close()
	driver.quit()
	print(driver.session_id)
	time.sleep(120)
	return None

# Product
class Crawler(metaclass=ABCMeta):
    @abstractmethod
    def crawl(self):
        pass

# concreteProduct
class SearchRank(Crawler):
    def crawl(query, word):
        url = f"https://search.naver.com/search.naver?display=15&f=&filetype=0&page=2&query={query}&research_url=&sm=tab_pge&start=1&where=web"
        proxies = {
            'http': 'socks5://127.0.0.1:9050',
            'https': 'socks5://127.0.0.1:9050'
        }
        page = requests.get(url, proxies=proxies)
        soup = bs(page.text, "html.parser")
        flag = False
        rank = "X"

        print(query)
        print(word)


        elements = soup.select('li.bx div > div.total_tit_group')

        for index, element in enumerate(elements, 1):
            print("{} 번째 게시글의 제목: {}".format(index, element.text))
            if (word in element.text) :
                print("True!!")
                flag = True
                rank = index
                return str(rank)

        if (flag == True) :
            return str(rank)
        else :
            url2 = f"https://search.naver.com/search.naver?display=15&f=&filetype=0&page=3&query={query}&research_url=&sm=tab_pge&start=16&where=web"
            page2 = requests.get(url2, proxies=proxies)
            soup2 = bs(page2.text, "html.parser")
            elements2 = soup2.select('li.bx div > div.total_tit_group')
            for index, element in enumerate(elements2, 16):
                print("{} 번째 게시글의 제목: {}".format(index, element.text))
                if (word in element.text) :
                    print("True!!")
                    flag = True
                    rank = index
                    return str(rank)
                
            return str(rank)

class ShopRank(Crawler):
    def crawl(self, query, word, mid):
        url = f"https://search.shopping.naver.com/search/all?query={query}&frm=NVSHATC&prevQuery={word}"
        # url = f"https://search.shopping.naver.com/search/all?frm=NVSHATC&origQuery={query}&pagingIndex=1&pagingSize=40&productSet=total&query={query}&sort=rel&timestamp=&viewType=list"

        flag = False
        rank = "X"
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument("--single-process")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--proxy-server=socks5://127.0.0.1:9150")
        path='../chromedriver'
        browser = webdriver.Chrome(path, chrome_options=chrome_options)
        browser.maximize_window()

        # 페이지 이동
        # url = "https://play.google.com/store/movies/top"
        browser.get(url)


        # 지정한 위치로 스크롤 내리기
        # 1080 해상도인 경우, 1080 위치로 한페이지를 스크롤한다
        browser.execute_script("window.scrollTo(0,1080)")

        # 화면 가장 하단으로 스크롤 내리기
        browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")


        interval = 1  # 1초에 한 번씩 스크롤 내림

        # 현재 문서 높이를 가져와서 저장
        prev_height = browser.execute_script("return document.body.scrollHeight")


        while True:
            # 가장 아래로 스크롤 이동
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")

            # 페이지 로딩 대기
            time.sleep(interval)

            # 현재 문서 높이를 가져와서 저장
            curr_height = browser.execute_script("return document.body.scrollHeight")
            if prev_height == curr_height:
                break

            prev_height = curr_height

        print("스크롤 완료")

        # ----------------------------------------------------------------
        soup = bs(browser.page_source, "html.parser")
        elements = soup.select('ul.list_basis > div > div > li > div > div.basicList_info_area__17Xyo > div.basicList_title__3P9Q7 > a')
        # elements = soup.select('ul.list_basis')
        print(len(elements))

        for index, element in enumerate(elements, 1):
            print("{} 번째 게시글의 제목: {}".format(index, element.text))
            if (str(mid) in str(element)) :
                print("True!!")
                flag = True
                rank = index
                # return 하면 될듯?
                return str(rank)

        if (flag == True) :
            return str(rank)
        else :
            # url2 = f"https://search.naver.com/search.naver?display=15&f=&filetype=0&page=3&query={query}&research_url=&sm=tab_pge&start=16&where=web"
            # page2 = requests.get(url2)
            # soup2 = bs(page2.text, "html.parser")
            # elements2 = soup2.select('li.bx div > div.total_tit_group')
            # for index, element in enumerate(elements2, 16):
            # 	print("{} 번째 게시글의 제목: {}".format(index, element.text))
                # if (word in element.text) :
                # 	print("True!!")
                # 	flag = True
                # 	rank = index
                # 	# return 하면 될듯?
                # 	return str(rank)
                
            return str(rank)


class Type1(Crawler):
    def crawl(self, query, word, mid):
        print('Type1')
        # 체류시간
        randTime = random.randrange(60, 91)
        print(f"{randTime}초 체류 예정")

        # query 받은걸 배열로 변환 후 random으로 하나 찝어냄
        arr = query.split(',')
        arrLen = len(arr)
        randNum = random.randrange(0, arrLen)
        randQuery = arr[randNum]

        driver = connection()
        if (driver is None):
            return "Connection Error"

        ip = driver.find_element_by_tag_name('pre').text

        print(f'현재 IP  ::::  {ip}')

        url = f"https://search.naver.com/search.naver?display=15&f=&filetype=0&page=2&query={randQuery}&research_url=&sm=tab_pge&start=1&where=web"
        # page = requests.get(url, proxies=proxies)
        # soup = bs(page.text, "html.parser")
        flag = False
        rank = "X"
        click = False
        href = ""

        driver.get(url)

        # 지정한 위치로 스크롤 내리기
        # 1080 해상도인 경우, 1080 위치로 한페이지를 스크롤한다
        driver.execute_script("window.scrollTo(0,1080)")

        # 화면 가장 하단으로 스크롤 내리기
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

        # soup = bs(driver.page_source, "html.parser")

        # elements = soup.select('li.bx')
        elements = driver.find_elements_by_partial_link_text(word)

        for index, element in enumerate(elements, 1):
            print("{} 번째 게시글의 제목: {}".format(index, element.text))
            if (word in element.text) :
                print("True!!")
                print(element.text)
                print(element.get_attribute('href'))
                href = element.get_attribute('href')
                flag = True
                break

        if (flag != True) :
            url2 = f"https://search.naver.com/search.naver?display=15&f=&filetype=0&page=3&query={randQuery}&research_url=&sm=tab_pge&start=16&where=web"
            driver.get(url2)
            driver.execute_script("window.scrollTo(0,1080)")
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            elements2 = driver.find_elements_by_partial_link_text(word)
            for index, element in enumerate(elements2, 16):
                print("{} 번째 게시글의 제목: {}".format(index, element.text))
                if (word in element.text) :
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
            closeAllChrome(driver)
            print(driver)
            print(driver.session_id)
            return "done"
        else :
            closeAllChrome(driver)
            return str(rank)

class Type2(Crawler):
    def crawl(self, query, word, mid):
        print('Type2')
        # 체류시간
        randTime = random.randrange(60, 91)
        print(f"{randTime}초 체류 예정")

        # query 받은걸 배열로 변환 후 random으로 두개 찝어냄
        arr = query.split(',')
        arrLen = len(arr)
        randNum = random.randrange(0, arrLen)
        randQuery1 = arr[randNum]
        randQuery2 = ''
        if (arrLen == 1) :
            randQuery2 = randQuery1
        else :
            arr.pop(randNum)
            randNum = random.randrange(0, arrLen - 1)
            randQuery2 = arr[randNum]

        driver = connection()
        if (driver is None):
            return "Connection Error"

        ip = driver.find_element_by_tag_name('pre').text

        print(f'현재 IP  ::::  {ip}')

        # 먼저 쿼리1 검색
        url = f"https://search.naver.com/search.naver?display=15&f=&filetype=0&page=2&query={randQuery1}&research_url=&sm=tab_pge&start=1&where=web"

        flag = False
        rank = "X"
        click = False
        href = ""

        driver.get(url)
        driver.execute_script("window.scrollTo(0,1080)")

        # 화면 가장 하단으로 스크롤 내리기
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

        # 쿼리2 검색처리
        url = f"https://search.naver.com/search.naver?display=15&f=&filetype=0&page=2&query={randQuery1}+{randQuery2}&research_url=&sm=tab_pge&start=1&where=web"
        driver.get(url)
        driver.execute_script("window.scrollTo(0,1080)")

        # 화면 가장 하단으로 스크롤 내리기
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

        # soup = bs(driver.page_source, "html.parser")

        # elements = soup.select('li.bx')
        elements = driver.find_elements_by_partial_link_text(word)

        for index, element in enumerate(elements, 1):
            print("{} 번째 게시글의 제목: {}".format(index, element.text))
            if (word in element.text) :
                print("True!!")
                print(element.text)
                print(element.get_attribute('href'))
                href = element.get_attribute('href')
                flag = True
                break

        if (flag != True) :
            url2 = f"https://search.naver.com/search.naver?display=15&f=&filetype=0&page=3&query={randQuery1}+{randQuery2}&research_url=&sm=tab_pge&start=16&where=web"
            driver.get(url2)
            driver.execute_script("window.scrollTo(0,1080)")
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            elements2 = driver.find_elements_by_partial_link_text(word)
            for index, element in enumerate(elements2, 16):
                print("{} 번째 게시글의 제목: {}".format(index, element.text))
                if (word in element.text) :
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
            closeAllChrome(driver)
            print(driver)
            print(driver.session_id)
            return "done"
        else :
            closeAllChrome(driver)
            return str(rank)

class Type3(Crawler):
    def crawl(self, query, word, mid):
        print('Type3')
        # 체류시간
        randTime = random.randrange(60, 91)
        print(f"{randTime}초 체류 예정")

        # query 받은걸 배열로 변환 후 random으로 두개 찝어냄
        arr = query.split(',')
        arrLen = len(arr)
        randNum = random.randrange(0, arrLen)
        randQuery1 = arr[randNum]
        randQuery2 = ''
        if (arrLen == 1) :
            randQuery2 = randQuery1
        else :
            arr.pop(randNum)
            randNum = random.randrange(0, arrLen - 1)
            randQuery2 = arr[randNum]

        driver = connection()
        if (driver is None):
            return "Connection Error"

        ip = driver.find_element_by_tag_name('pre').text

        print(f'현재 IP  ::::  {ip}')

        # 먼저 쿼리1+쿼리2 검색
        url = f"https://search.naver.com/search.naver?display=15&f=&filetype=0&page=2&query={randQuery1}+{randQuery2}&research_url=&sm=tab_pge&start=1&where=web"

        flag = False
        rank = "X"
        click = False
        href = ""

        driver.get(url)
        driver.execute_script("window.scrollTo(0,1080)")

        # 화면 가장 하단으로 스크롤 내리기
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

        # 쿼리1 검색처리
        url = f"https://search.naver.com/search.naver?display=15&f=&filetype=0&page=2&query={randQuery1}&research_url=&sm=tab_pge&start=1&where=web"
        driver.get(url)
        driver.execute_script("window.scrollTo(0,1080)")

        # 화면 가장 하단으로 스크롤 내리기
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

        # 쿼리2 검색처리
        url = f"https://search.naver.com/search.naver?display=15&f=&filetype=0&page=2&query={randQuery2}&research_url=&sm=tab_pge&start=1&where=web"
        driver.get(url)
        driver.execute_script("window.scrollTo(0,1080)")

        # 화면 가장 하단으로 스크롤 내리기
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

        # soup = bs(driver.page_source, "html.parser")

        # 뒤로가기 처리
        driver.back()
        driver.execute_script("window.scrollTo(0,1080)")

        # 화면 가장 하단으로 스크롤 내리기
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

        # elements = soup.select('li.bx')
        elements = driver.find_elements_by_partial_link_text(word)

        for index, element in enumerate(elements, 1):
            print("{} 번째 게시글의 제목: {}".format(index, element.text))
            if (word in element.text) :
                print("True!!")
                print(element.text)
                print(element.get_attribute('href'))
                href = element.get_attribute('href')
                flag = True
                break

        if (flag != True) :
            url2 = f"https://search.naver.com/search.naver?display=15&f=&filetype=0&page=3&query={randQuery1}&research_url=&sm=tab_pge&start=16&where=web"
            driver.get(url2)
            driver.execute_script("window.scrollTo(0,1080)")
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            elements2 = driver.find_elements_by_partial_link_text(word)
            for index, element in enumerate(elements2, 16):
                print("{} 번째 게시글의 제목: {}".format(index, element.text))
                if (word in element.text) :
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
            closeAllChrome(driver)
            print(driver)
            print(driver.session_id)
            return "done"
        else :
            closeAllChrome(driver)
            return str(rank)

class Type4(Crawler):
    def crawl(self, query, word, mid):
        print('Type4')
        # 체류시간
        randTime = random.randrange(60, 91)
        print(f"{randTime}초 체류 예정")

        # query 받은걸 배열로 변환 후 random으로 두개 찝어냄
        arr = query.split(',')
        arrLen = len(arr)
        randNum = random.randrange(0, arrLen)
        randQuery1 = arr[randNum]
        randQuery2 = ''
        if (arrLen == 1) :
            randQuery2 = randQuery1
        else :
            arr.pop(randNum)
            randNum = random.randrange(0, arrLen - 1)
            randQuery2 = arr[randNum]

        driver = connection()
        if (driver is None):
            return "Connection Error"

        ip = driver.find_element_by_tag_name('pre').text

        print(f'현재 IP  ::::  {ip}')

        # 먼저 쿼리1+쿼리2 검색
        url = f"https://search.naver.com/search.naver?display=15&f=&filetype=0&page=2&query={randQuery1}+{randQuery2}&research_url=&sm=tab_pge&start=1&where=web"

        flag = False
        rank = "X"
        click = False
        href = ""

        driver.get(url)
        driver.execute_script("window.scrollTo(0,1080)")

        # 화면 가장 하단으로 스크롤 내리기
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

        # 쿼리1 검색처리
        url = f"https://search.naver.com/search.naver?display=15&f=&filetype=0&page=2&query={randQuery1}&research_url=&sm=tab_pge&start=1&where=web"
        driver.get(url)
        driver.execute_script("window.scrollTo(0,1080)")

        # 화면 가장 하단으로 스크롤 내리기
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

        # 쿼리2 검색처리
        url = f"https://search.naver.com/search.naver?display=15&f=&filetype=0&page=2&query={randQuery2}&research_url=&sm=tab_pge&start=1&where=web"
        driver.get(url)
        driver.execute_script("window.scrollTo(0,1080)")

        # 화면 가장 하단으로 스크롤 내리기
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

        # elements = soup.select('li.bx')
        elements = driver.find_elements_by_partial_link_text(word)

        for index, element in enumerate(elements, 1):
            print("{} 번째 게시글의 제목: {}".format(index, element.text))
            if (word in element.text) :
                print("True!!")
                print(element.text)
                print(element.get_attribute('href'))
                href = element.get_attribute('href')
                flag = True
                break

        if (flag != True) :
            url2 = f"https://search.naver.com/search.naver?display=15&f=&filetype=0&page=3&query={randQuery2}&research_url=&sm=tab_pge&start=16&where=web"
            driver.get(url2)
            driver.execute_script("window.scrollTo(0,1080)")
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            elements2 = driver.find_elements_by_partial_link_text(word)
            for index, element in enumerate(elements2, 16):
                print("{} 번째 게시글의 제목: {}".format(index, element.text))
                if (word in element.text) :
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
            closeAllChrome(driver)
            print(driver)
            print(driver.session_id)
            return "done"
        else :
            closeAllChrome(driver)
            return str(rank)

class Type5(Crawler):
    def crawl(self, query, word, mid):
        print('Type5')
        # 체류시간
        randTime = random.randrange(60, 91)
        print(f"{randTime}초 체류 예정")

        # query 받은걸 배열로 변환 후 random으로 하나 찝어냄
        arr = query.split(',')
        arrLen = len(arr)
        randNum = random.randrange(0, arrLen)
        randQuery = arr[randNum]

        driver = connection()
        if (driver is None):
            return "Connection Error"

        ip = driver.find_element_by_tag_name('pre').text

        print(f'현재 IP  ::::  {ip}')

        url = f"https://search.naver.com/search.naver?display=15&f=&filetype=0&page=2&query={randQuery}&research_url=&sm=tab_pge&start=1&where=web"
        # page = requests.get(url, proxies=proxies)
        # soup = bs(page.text, "html.parser")
        flag = False
        rank = "X"
        click = False
        href = ""

        driver.get(url)

        # 지정한 위치로 스크롤 내리기
        # 1080 해상도인 경우, 1080 위치로 한페이지를 스크롤한다
        driver.execute_script("window.scrollTo(0,1080)")

        # 화면 가장 하단으로 스크롤 내리기
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

        # soup = bs(driver.page_source, "html.parser")

        # elements = soup.select('li.bx')
        elements = driver.find_elements_by_partial_link_text(word)

        for index, element in enumerate(elements, 1):
            print("{} 번째 게시글의 제목: {}".format(index, element.text))
            if (word in element.text) :
                print("True!!")
                print(element.text)
                print(element.get_attribute('href'))
                href = element.get_attribute('href')
                flag = True
                break

        if (flag != True) :
            url2 = f"https://search.naver.com/search.naver?display=15&f=&filetype=0&page=3&query={randQuery}&research_url=&sm=tab_pge&start=16&where=web"
            driver.get(url2)
            driver.execute_script("window.scrollTo(0,1080)")
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            elements2 = driver.find_elements_by_partial_link_text(word)
            for index, element in enumerate(elements2, 16):
                print("{} 번째 게시글의 제목: {}".format(index, element.text))
                if (word in element.text) :
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
            closeAllChrome(driver)
            print(driver)
            print(driver.session_id)
            return "done"
        else :
            closeAllChrome(driver)
            return str(rank)

class Type6(Crawler):
    def crawl(self, query, word, mid):
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

        driver = connection()
        if (driver is None):
            return "Connection Error"

        ip = driver.find_element_by_tag_name('pre').text

        print(f'현재 IP  ::::  {ip}')

        url = f"https://search.naver.com/search.naver?display=15&f=&filetype=0&page=2&query={replaceQuery}&oquery={randQuery}&research_url=&sm=tab_pge&start=1&where=web"
        # page = requests.get(url, proxies=proxies)
        # soup = bs(page.text, "html.parser")
        flag = False
        rank = "X"
        click = False
        href = ""

        driver.get(url)

        # 지정한 위치로 스크롤 내리기
        # 1080 해상도인 경우, 1080 위치로 한페이지를 스크롤한다
        driver.execute_script("window.scrollTo(0,1080)")

        # 화면 가장 하단으로 스크롤 내리기
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

        # soup = bs(driver.page_source, "html.parser")

        # elements = soup.select('li.bx')
        elements = driver.find_elements_by_partial_link_text(word)

        for index, element in enumerate(elements, 1):
            print("{} 번째 게시글의 제목: {}".format(index, element.text))
            if (word in element.text) :
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
                if (word in element.text) :
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
            closeAllChrome(driver)
            print(driver)
            print(driver.session_id)
            return "done"
        else :
            closeAllChrome(driver)
            return str(rank)


# Factory
class CrawlFactory(metaclass=ABCMeta):
    @abstractmethod
    def createCrawler(self):
        ''' factory method '''
        pass

# concreteFactory
class SiteFactory(CrawlFactory):
    def createCrawler(self):
        num = random.randrange(1, 7)
        if num == 1:
            return Type1()
        elif num == 2:
            return Type2()
        elif num == 3:
            return Type3()
        elif num == 4:
            return Type4()
        elif num == 5:
            return Type5()
        else:
            return Type6()

class SearchFactory(CrawlFactory):
    def createCrawler(self):
        return SearchRank()


# client
class Client():
    
    def __init__(self):
        self.query = ""
        self.word = ""
        self.loop = ""
        self.crawler = ""
        self.mid = ""

    def create(self, param, query, word, loop):
        """param은 사용자 요구에 따라 변경"""

        # 사용자 요구에 따라, product를 생산할 factory 생성
        if param == 'site':
            factory = SiteFactory()
        elif param == 'search':
            factory = SearchRank()
        else:
            return

        # product 생산 (객체 생성)
        self.crawler = factory.createCrawler()
        self.query = query
        self.word = word
        self.loop = loop
        # # 생산된 product를 사용
        # self.crawler.crawl(query, word)

##        # product 생산, 실행, 반환하는 templete_method 호출
##        mymouse = factory.useMouse()

    def crawl(self):
        if self.crawler == "" or self.word == "" or self.query == "" or self.loop == "":
            print("객체 생성이 되지 않았습니다")
            return
        else:
            num = 1
            while(self.loop > num):
                self.crawler.crawl(self.query, self.word)

    def setLoop(self, loop):
        self.loop = loop


if __name__ == '__main__':
    client = Client()
    client.create('site', '하이데브', 'highdev.modoo.at', 2)