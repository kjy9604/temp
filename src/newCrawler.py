from abc import ABCMeta, abstractmethod
import random
import subprocess
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup as bs

Driver = None # 공용 웹드라이버

# selenium과 tor 연결
def connection(): 

    global Driver

    changeIp()
    if (Driver is None):

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
                # proxies = {
                #     'http': 'socks5://127.0.0.1:9050',
                #     'https': 'socks5://127.0.0.1:9050'
                # }
                webdriver.DesiredCapabilities.CHROME['acceptSslCerts']=True

                opts.add_argument("user-agent="+user_agent)
                opts.add_argument('--headless')
                opts.add_argument('--no-sandbox')
                opts.add_argument('--proxy-server='"socks5://"+PROXY)
                opts.binary_location = '/usr/bin/google-chrome'

                url = "http://wtfismyip.com/text"
                Driver =webdriver.Chrome(executable_path="/home/ubuntu/chromedriver",options=opts)
                Driver.create_options()
                Driver.execute_script("window.open('');")
                Driver.switch_to.window(Driver.window_handles[-1])
                Driver.get(url)
                time.sleep(5)
                ip = Driver.find_element_by_tag_name('pre').text

                print(f'현재 IP  ::::  {ip}')
                temp = False
            except Exception as e:
                print(e)
                Driver.quit()
        return Driver
    else:
        url = "http://wtfismyip.com/text"
        Driver.get(url)
        time.sleep(5)
        ip = Driver.find_element_by_tag_name('pre').text

        print(f'현재 IP  ::::  {ip}')
        return Driver

def changeIp():
    global Driver
    if (Driver is None):
        return
    else :
        # IP Change
        subprocess.Popen(['systemctl', 'reload']+['tor']).wait()
        print('tor reload')
        time.sleep(2)
        Driver.execute_script("window.open('');")
        Driver.switch_to.window(Driver.window_handles[-1])
        return

# selenium 탭 종료 후 2분 슬립
def closeSelenium():
    global Driver
    if (Driver is None) :
        return None
    else :
        Driver.delete_all_cookies()
        # Driver.close()
        time.sleep(120)
        return None

# selenium 종료 후 2분 슬립
def quitSelenium():
    global Driver
    if (Driver is None) :
        return None
    else :
        Driver.delete_all_cookies()
        Driver.close()
        Driver.quit()
        print(Driver.session_id)
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
    def crawl(self, query, word):
        global Driver
        url = f"https://search.shopping.naver.com/search/all?query={query}&frm=NVSHATC&prevQuery={word}"

        flag = False
        rank = "X"
        if (Driver is None):
            connection()
        else:
            changeIp()
        Driver.maximize_window()

        # 페이지 이동
        # url = "https://play.google.com/store/movies/top"
        Driver.get(url)
        time.sleep(5)


        # 지정한 위치로 스크롤 내리기
        # 1080 해상도인 경우, 1080 위치로 한페이지를 스크롤한다
        Driver.execute_script("window.scrollTo(0,1080)")

        # 화면 가장 하단으로 스크롤 내리기
        Driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")


        interval = 1  # 1초에 한 번씩 스크롤 내림

        # 현재 문서 높이를 가져와서 저장
        prev_height = Driver.execute_script("return document.body.scrollHeight")


        while True:
            # 가장 아래로 스크롤 이동
            Driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

            # 페이지 로딩 대기
            time.sleep(interval)

            # 현재 문서 높이를 가져와서 저장
            curr_height = Driver.execute_script("return document.body.scrollHeight")
            if prev_height == curr_height:
                break

            prev_height = curr_height

        print("스크롤 완료")

        # ----------------------------------------------------------------
        soup = bs(Driver.page_source, "html.parser")
        elements = soup.select('ul.list_basis > div > div > li > div > div.basicList_info_area__17Xyo > div.basicList_title__3P9Q7 > a')
        # elements = soup.select('ul.list_basis')
        print(len(elements))

        for index, element in enumerate(elements, 1):
            print("{} 번째 게시글의 제목: {}".format(index, element.text))
            if (str(self.mid) in str(element)) :
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
    def crawl(self, query, word):
        global Driver 
        print('Type1')
        # 체류시간
        randTime = random.randrange(60, 91)
        print(f"{randTime}초 체류 예정")

        # query 받은걸 배열로 변환 후 random으로 하나 찝어냄
        arr = query.split(',')
        arrLen = len(arr)
        randNum = random.randrange(0, arrLen)
        randQuery = arr[randNum]

        
        if (Driver is None):
            connection()
        else:
            changeIp()

        url = f"https://search.naver.com/search.naver?display=15&f=&filetype=0&page=2&query={randQuery}&research_url=&sm=tab_pge&start=1&where=web"
        flag = False
        rank = "X"
        click = False
        href = ""

        Driver.get(url)
        time.sleep(5)

        # 지정한 위치로 스크롤 내리기
        # 1080 해상도인 경우, 1080 위치로 한페이지를 스크롤한다
        Driver.execute_script("window.scrollTo(0,1080)")

        # 화면 가장 하단으로 스크롤 내리기
        Driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

        elements = Driver.find_elements_by_partial_link_text(word)

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
            Driver.get(url2)
            Driver.execute_script("window.scrollTo(0,1080)")
            Driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            elements2 = Driver.find_elements_by_partial_link_text(word)
            for index, element in enumerate(elements2, 16):
                print("{} 번째 게시글의 제목: {}".format(index, element.text))
                if (word in element.text) :
                    print("True!!")
                    flag = True
                    href = element.get_attribute('href')
                    break
                
        if (flag == True) :
            link = Driver.find_element_by_xpath('//a[@href="'+href+'"]')
            link.click()
            time.sleep(5)
            max_time_end = time.time() + randTime
            while True :
                # 가장 아래로 스크롤 이동
                Driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

                # 페이지 로딩 대기
                time.sleep(2)

                # 현재 문서 높이를 가져와서 저장
                curr_height = Driver.execute_script("return document.body.scrollHeight")

                prev_height = curr_height
                Driver.execute_script("window.scrollTo(0, 0)")
                if time.time() > max_time_end :
                    break

            Driver.back()
            time.sleep(2)
            closeSelenium()
            return "done"
        else :
            closeSelenium()
            return str(rank)

class Type2(Crawler):
    def crawl(self, query, word):
        global Driver 
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

        
        if (Driver is None):
            connection()
        else:
            changeIp()

        # 먼저 쿼리1 검색
        url = f"https://search.naver.com/search.naver?display=15&f=&filetype=0&page=2&query={randQuery1}&research_url=&sm=tab_pge&start=1&where=web"

        flag = False
        rank = "X"
        click = False
        href = ""

        Driver.get(url)
        time.sleep(5)
        Driver.execute_script("window.scrollTo(0,1080)")

        # 화면 가장 하단으로 스크롤 내리기
        Driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

        # 쿼리2 검색처리
        url = f"https://search.naver.com/search.naver?display=15&f=&filetype=0&page=2&query={randQuery1}+{randQuery2}&research_url=&sm=tab_pge&start=1&where=web"
        Driver.get(url)
        time.sleep(5)
        Driver.execute_script("window.scrollTo(0,1080)")

        # 화면 가장 하단으로 스크롤 내리기
        Driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

        elements = Driver.find_elements_by_partial_link_text(word)

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
            Driver.get(url2)
            Driver.execute_script("window.scrollTo(0,1080)")
            Driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            elements2 = Driver.find_elements_by_partial_link_text(word)
            for index, element in enumerate(elements2, 16):
                print("{} 번째 게시글의 제목: {}".format(index, element.text))
                if (word in element.text) :
                    print("True!!")
                    flag = True
                    href = element.get_attribute('href')
                    break
                
        if (flag == True) :
            link = Driver.find_element_by_xpath('//a[@href="'+href+'"]')
            link.click()
            time.sleep(5)
            max_time_end = time.time() + randTime
            while True :
                # 가장 아래로 스크롤 이동
                Driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

                # 페이지 로딩 대기
                time.sleep(2)

                # 현재 문서 높이를 가져와서 저장
                curr_height = Driver.execute_script("return document.body.scrollHeight")

                prev_height = curr_height
                Driver.execute_script("window.scrollTo(0, 0)")
                if time.time() > max_time_end :
                    break

            Driver.back()
            time.sleep(2)
            closeSelenium()
            return "done"
        else :
            closeSelenium()
            return str(rank)

class Type3(Crawler):
    def crawl(self, query, word):
        global Driver 
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

        
        if (Driver is None):
            connection()
        else:
            changeIp()

        # 먼저 쿼리1+쿼리2 검색
        url = f"https://search.naver.com/search.naver?display=15&f=&filetype=0&page=2&query={randQuery1}+{randQuery2}&research_url=&sm=tab_pge&start=1&where=web"

        flag = False
        rank = "X"
        click = False
        href = ""

        Driver.get(url)
        time.sleep(5)
        Driver.execute_script("window.scrollTo(0,1080)")

        # 화면 가장 하단으로 스크롤 내리기
        Driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

        # 쿼리1 검색처리
        url = f"https://search.naver.com/search.naver?display=15&f=&filetype=0&page=2&query={randQuery1}&research_url=&sm=tab_pge&start=1&where=web"
        Driver.get(url)
        time.sleep(5)
        Driver.execute_script("window.scrollTo(0,1080)")

        # 화면 가장 하단으로 스크롤 내리기
        Driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

        # 쿼리2 검색처리
        url = f"https://search.naver.com/search.naver?display=15&f=&filetype=0&page=2&query={randQuery2}&research_url=&sm=tab_pge&start=1&where=web"
        Driver.get(url)
        time.sleep(5)
        Driver.execute_script("window.scrollTo(0,1080)")

        # 화면 가장 하단으로 스크롤 내리기
        Driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

        # 뒤로가기 처리
        Driver.back()
        Driver.execute_script("window.scrollTo(0,1080)")

        # 화면 가장 하단으로 스크롤 내리기
        Driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

        elements = Driver.find_elements_by_partial_link_text(word)

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
            Driver.get(url2)
            Driver.execute_script("window.scrollTo(0,1080)")
            Driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            elements2 = Driver.find_elements_by_partial_link_text(word)
            for index, element in enumerate(elements2, 16):
                print("{} 번째 게시글의 제목: {}".format(index, element.text))
                if (word in element.text) :
                    print("True!!")
                    flag = True
                    href = element.get_attribute('href')
                    break
                
        if (flag == True) :
            link = Driver.find_element_by_xpath('//a[@href="'+href+'"]')
            link.click()
            time.sleep(5)
            max_time_end = time.time() + randTime
            while True :
                # 가장 아래로 스크롤 이동
                Driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

                # 페이지 로딩 대기
                time.sleep(2)

                # 현재 문서 높이를 가져와서 저장
                curr_height = Driver.execute_script("return document.body.scrollHeight")

                prev_height = curr_height
                Driver.execute_script("window.scrollTo(0, 0)")
                if time.time() > max_time_end :
                    break

            Driver.back()
            time.sleep(2)
            closeSelenium()
            return "done"
        else :
            closeSelenium()
            return str(rank)

class Type4(Crawler):
    def crawl(self, query, word):
        global Driver 
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

        
        if (Driver is None):
            connection()
        else:
            changeIp()

        # 먼저 쿼리1+쿼리2 검색
        url = f"https://search.naver.com/search.naver?display=15&f=&filetype=0&page=2&query={randQuery1}+{randQuery2}&research_url=&sm=tab_pge&start=1&where=web"

        flag = False
        rank = "X"
        click = False
        href = ""

        Driver.get(url)
        time.sleep(5)
        Driver.execute_script("window.scrollTo(0,1080)")

        # 화면 가장 하단으로 스크롤 내리기
        Driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

        # 쿼리1 검색처리
        url = f"https://search.naver.com/search.naver?display=15&f=&filetype=0&page=2&query={randQuery1}&research_url=&sm=tab_pge&start=1&where=web"
        Driver.get(url)
        time.sleep(5)
        Driver.execute_script("window.scrollTo(0,1080)")

        # 화면 가장 하단으로 스크롤 내리기
        Driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

        # 쿼리2 검색처리
        url = f"https://search.naver.com/search.naver?display=15&f=&filetype=0&page=2&query={randQuery2}&research_url=&sm=tab_pge&start=1&where=web"
        Driver.get(url)
        time.sleep(5)
        Driver.execute_script("window.scrollTo(0,1080)")

        # 화면 가장 하단으로 스크롤 내리기
        Driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

        elements = Driver.find_elements_by_partial_link_text(word)

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
            Driver.get(url2)
            Driver.execute_script("window.scrollTo(0,1080)")
            Driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            elements2 = Driver.find_elements_by_partial_link_text(word)
            for index, element in enumerate(elements2, 16):
                print("{} 번째 게시글의 제목: {}".format(index, element.text))
                if (word in element.text) :
                    print("True!!")
                    flag = True
                    href = element.get_attribute('href')
                    break
                
        if (flag == True) :
            link = Driver.find_element_by_xpath('//a[@href="'+href+'"]')
            link.click()
            time.sleep(5)
            max_time_end = time.time() + randTime
            while True :
                # 가장 아래로 스크롤 이동
                Driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

                # 페이지 로딩 대기
                time.sleep(2)

                # 현재 문서 높이를 가져와서 저장
                curr_height = Driver.execute_script("return document.body.scrollHeight")

                prev_height = curr_height
                Driver.execute_script("window.scrollTo(0, 0)")
                if time.time() > max_time_end :
                    break

            Driver.back()
            time.sleep(2)
            closeSelenium()
            return "done"
        else :
            closeSelenium()
            return str(rank)

class Type5(Crawler):
    def crawl(self, query, word):
        global Driver 
        print('Type5')
        # 체류시간
        randTime = random.randrange(60, 91)
        print(f"{randTime}초 체류 예정")

        # query 받은걸 배열로 변환 후 random으로 하나 찝어냄
        arr = query.split(',')
        arrLen = len(arr)
        randNum = random.randrange(0, arrLen)
        randQuery = arr[randNum]

        
        if (Driver is None):
            connection()
        else:
            changeIp()

        url = f"https://search.naver.com/search.naver?display=15&f=&filetype=0&page=2&query={randQuery}&research_url=&sm=tab_pge&start=1&where=web"
        flag = False
        rank = "X"
        click = False
        href = ""

        Driver.get(url)
        time.sleep(5)

        # 지정한 위치로 스크롤 내리기
        # 1080 해상도인 경우, 1080 위치로 한페이지를 스크롤한다
        Driver.execute_script("window.scrollTo(0,1080)")

        # 화면 가장 하단으로 스크롤 내리기
        Driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

        elements = Driver.find_elements_by_partial_link_text(word)

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
            Driver.get(url2)
            Driver.execute_script("window.scrollTo(0,1080)")
            Driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            elements2 = Driver.find_elements_by_partial_link_text(word)
            for index, element in enumerate(elements2, 16):
                print("{} 번째 게시글의 제목: {}".format(index, element.text))
                if (word in element.text) :
                    print("True!!")
                    flag = True
                    href = element.get_attribute('href')
                    break
                
        if (flag == True) :
            link = Driver.find_element_by_xpath('//a[@href="'+href+'"]')
            link.click()
            time.sleep(5)
            max_time_end = time.time() + randTime
            while True :
                # 가장 아래로 스크롤 이동
                Driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

                # 페이지 로딩 대기
                time.sleep(2)

                # 현재 문서 높이를 가져와서 저장
                curr_height = Driver.execute_script("return document.body.scrollHeight")

                prev_height = curr_height
                Driver.execute_script("window.scrollTo(0, 0)")
                if time.time() > max_time_end :
                    break

            Driver.back()
            time.sleep(2)
            closeSelenium()
            return "done"
        else :
            closeSelenium()
            return str(rank)

class Type6(Crawler):
    def crawl(self, query, word):
        global Driver 
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

        
        if (Driver is None):
            connection()
        else:
            changeIp()

        url = f"https://search.naver.com/search.naver?display=15&f=&filetype=0&page=2&query={replaceQuery}&oquery={randQuery}&research_url=&sm=tab_pge&start=1&where=web"
        flag = False
        rank = "X"
        click = False
        href = ""

        Driver.get(url)
        time.sleep(5)

        # 지정한 위치로 스크롤 내리기
        # 1080 해상도인 경우, 1080 위치로 한페이지를 스크롤한다
        Driver.execute_script("window.scrollTo(0,1080)")

        # 화면 가장 하단으로 스크롤 내리기
        Driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

        elements = Driver.find_elements_by_partial_link_text(word)

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
            Driver.get(url2)
            Driver.execute_script("window.scrollTo(0,1080)")
            Driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            elements2 = Driver.find_elements_by_partial_link_text(word)
            for index, element in enumerate(elements2, 16):
                print("{} 번째 게시글의 제목: {}".format(index, element.text))
                if (word in element.text) :
                    print("True!!")
                    flag = True
                    href = element.get_attribute('href')
                    break
                
        if (flag == True) :
            link = Driver.find_element_by_xpath('//a[@href="'+href+'"]')
            link.click()
            time.sleep(5)
            max_time_end = time.time() + randTime
            while True :
                # 가장 아래로 스크롤 이동
                Driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

                # 페이지 로딩 대기
                time.sleep(2)

                # 현재 문서 높이를 가져와서 저장
                curr_height = Driver.execute_script("return document.body.scrollHeight")

                prev_height = curr_height
                Driver.execute_script("window.scrollTo(0, 0)")
                if time.time() > max_time_end :
                    break

            Driver.back()
            time.sleep(2)
            closeSelenium()
            return "done"
        else :
            closeSelenium()
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

class ShopFactory(CrawlFactory):
    def createCrawler(self):
        return ShopRank()


# client
class Client():
    
    def __init__(self):
        self._query = ""
        self._word = ""
        self._loop = ""
        self._crawler = ""
        self._mid = ""

    def create(self, param, query, word, loop):
        """param은 사용자 요구에 따라 변경"""

        # 사용자 요구에 따라, product를 생산할 factory 생성
        if param == 'site': # 검색어 순위 조작용, Type 1 ~ 6까지 랜덤, 현재 진행중임
            factory = SiteFactory()
        elif param == 'search': # 검색어 순위 도출용, 검색하여 30위까지 도출함
            factory = SearchFactory()
        elif param == 'shop': # 네이버쇼핑 검색어, 연관검색어, 제품ID로 연관검색어 조작 + 순위조작
            factory = ShopFactory()
        else:
            return

        # product 생산 (객체 생성)
        self._crawler = factory.createCrawler()
        self._query = query
        self._word = word
        self._loop = loop

    def crawl(self):
        if self._crawler == "" or self._word == "" or self._query == "" or self._loop == "":
            print("객체 생성이 되지 않았습니다")
            return
        else:
            num = 1
            while(self._loop >= num):
                self._crawler.crawl(self._query, self._word)
                num += 1

    def loop(self):
        return self._loop

    def loop(self, loop):
        self._loop = loop

    def mid(self):
        return self._mid

    def mid(self, mid):
        self._mid = mid


if __name__ == '__main__':
    # client = Client()
    # client.create('site', '하이데브', 'highdev.modoo.at', 2)
    # try:
    #     client.crawl()
    # except Exception as e:
    #     print(e)
    print("newCrawler")
