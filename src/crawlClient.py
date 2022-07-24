# from creator import SiteFactory, SearchFactory, ShopFactory
from .creator import SiteFactory
from .creator import SearchFactory
from .creator import ShopFactory

# client
class Client():
    
    def __init__(self):
        self._query = ""
        self._word = ""
        self._loop = ""
        self._crawler = ""
        self._url_mid = ""

    def create(self, param, query, word, url_mid, loop):
        """param은 사용자 요구에 따라 변경"""

        # 사용자 요구에 따라, product를 생산할 factory 생성
        if param == 'site': # 검색어 순위 조작용, Type 1 ~ 6까지 랜덤, 현재 진행중임
            factory = SiteFactory.SiteFactory()
        elif param == 'search': # 검색어 순위 도출용, 검색하여 30위까지 도출함
            factory = SearchFactory.SearchFactory()
        elif param == 'shop': # 네이버쇼핑 검색어, 연관검색어, 제품ID로 연관검색어 조작 + 순위조작
            factory = ShopFactory.ShopFactory()
        else:
            return

        # product 생산 (객체 생성)
        self._crawler = factory.createCrawler()
        self._query = query
        self._word = word
        self._loop = loop
        self._url_mid = url_mid

    def crawl(self):
        if self._crawler == "" or self._word == "" or self._query == "" or self._loop == "":
            print("객체 생성이 되지 않았습니다")
            return
        else:
            num = 1
            while(self._loop >= num):
                self._crawler.crawl(self._query, self._word, self._url_mid)
                num += 1

    def loop(self):
        return self._loop

    def loop(self, loop):
        self._loop = loop

    def mid(self):
        return self._mid

    def mid(self, mid):
        self._mid = mid