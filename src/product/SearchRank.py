from . import Crawler
import requests
from bs4 import BeautifulSoup as bs

class SearchRank(Crawler.Crawler):
    def crawl(self, query, word, url_mid):
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
            if (url_mid in element.text) :
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
                if (url_mid in element.text) :
                    print("True!!")
                    flag = True
                    rank = index
                    return str(rank)
                
            return str(rank)
