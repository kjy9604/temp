from . import Crawler
from bs4 import BeautifulSoup as bs
import time
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from util import DriverUtil

class ShopRank(Crawler.Crawler):
    def crawl(self, query, word, url_mid):

        driver = DriverUtil.DriverUtil.getDriver()
        url = f"https://search.shopping.naver.com/search/all?query={query}&frm=NVSHATC&prevQuery={word}"

        flag = False
        rank = "X"
        if (driver is None):
            DriverUtil.DriverUtil.connection()
        else:
            DriverUtil.DriverUtil.changeIp()
        driver.maximize_window()

        # 페이지 이동
        # url = "https://play.google.com/store/movies/top"
        driver.get(url)
        time.sleep(5)


        # 지정한 위치로 스크롤 내리기
        # 1080 해상도인 경우, 1080 위치로 한페이지를 스크롤한다
        driver.execute_script("window.scrollTo(0,1080)")

        # 화면 가장 하단으로 스크롤 내리기
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")


        interval = 1  # 1초에 한 번씩 스크롤 내림

        # 현재 문서 높이를 가져와서 저장
        prev_height = driver.execute_script("return document.body.scrollHeight")


        while True:
            # 가장 아래로 스크롤 이동
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

            # 페이지 로딩 대기
            time.sleep(interval)

            # 현재 문서 높이를 가져와서 저장
            curr_height = driver.execute_script("return document.body.scrollHeight")
            if prev_height == curr_height:
                break

            prev_height = curr_height

        print("스크롤 완료")

        # ----------------------------------------------------------------
        soup = bs(driver.page_source, "html.parser")
        elements = soup.select('ul.list_basis > div > div > li > div > div.basicList_info_area__17Xyo > div.basicList_title__3P9Q7 > a')
        # elements = soup.select('ul.list_basis')
        print(len(elements))

        for index, element in enumerate(elements, 1):
            print("{} 번째 게시글의 제목: {}".format(index, element.text))
            if (str(url_mid) in str(element)) :
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
                # if (url_mid in element.text) :
                # 	print("True!!")
                # 	flag = True
                # 	rank = index
                # 	# return 하면 될듯?
                # 	return str(rank)
                
            return str(rank)