
### 프로젝트 기본 정보
chrome + selenium + tor를 이용한 마케팅 봇

### 실행 전 필요한 파일
**** Linux 기준으로 작업했기 때문에 로컬에서 동작하지 않을 수 있습니다 ****

Google Chrome을 기반으로 크롤링 작업을 하기 때문에, 컴퓨터의 Google Chrome과 같은 버전의 chromedriver가 필요합니다.

- 버전 확인

  chrome://version/ URL로 이동

- chromedriver 다운로드

  [다운로드 페이지 이동](https://sites.google.com/a/chromium.org/chromedriver/downloads)

- chromedriver 파일 위치

  /usr/local/bin

- Message: unknown error: no chrome binary at /usr/bin/google-chrome 에러

  해당 경로에 google-chrome 파일이 없을 경우 발생

  홈브루를 사용하여 크롬 설치를 하거나, src/util/DriverUtil.py:54 라인을 주석하면 됩니다

  단, 이 경우 chromedriver의 버전 확인이 필요합니다.

  [링크](https://jessymin.github.io/web-scraping/2019/10/01/selenium-chrome-binary-error-solution.html)

- 개발자를 확인할 수 없기 때문에 ‘chromedriver’을(를) 열 수 없습니다.

  [링크](https://somjang.tistory.com/entry/MAC-OSX-%EA%B0%9C%EB%B0%9C%EC%9E%90%EB%A5%BC-%ED%99%95%EC%9D%B8%ED%95%A0-%EC%88%98-%EC%97%86%EA%B8%B0-%EB%95%8C%EB%AC%B8%EC%97%90-chromedriver%EC%9D%84%EB%A5%BC-%EC%97%B4-%EC%88%98-%EC%97%86%EC%8A%B5%EB%8B%88%EB%8B%A4-%ED%95%B4%EA%B2%B0-%EB%B0%A9%EB%B2%95)


Tor 설치(필수) [링크](https://m.blog.naver.com/ateon1/221329883861)

### 라이브러리 설치
```bash
$ python3 -m venv venv

$ . venv/bin/activate

$ pip3 install -r requirements.txt

# 실행
$ python3 ./app.py
```

### 각 클래스 설명
- app.py
  - connect()

    데이터베이스 연결

  - close(driver, cursor)

    pymysql 드라이버 종료

  - crawling()

    app.py 구동 시 호출되는 크롤링 함수, 데이터베이스와 통신 후 조회된 로우들 기준으로 크롤링을 반복 수행함

  - Crawl()

    Flask API 통신 클래스

- src/crawlClient
  
    app.py 에서 create()로 각 크롤링 객체를 생성함

- src/creator/
  - CrawlFactory

    Creator 인터페이스

  - SiteFactor

    CrawlFactory를 상속받음, 임의의 숫자(1~6)을 만들어내어서 각 타입의 순위조작(Type1 ~ Type6) 클래스 리턴

  - SearchFactor

    CrawlFactory를 상속받음, SearchRank 클래스 리턴

  - ShopFactor

    CrawlFactory를 상속받음, ShopRank 클래스 리턴

- src/product/Crawler

  기능구현 객체 인터페이스

- src/util/DriverUtil

  셀레니움 연결과 IP변경, 크롬의 탭 종료 및 닫기 기능
### 기능 설명
- src/product/SearchRank

  네이버 검색 후 30위까지에서 입력된 값의 순위 반환

- src/product/ShopRank

  네이버 쇼핑에서 검색어와 연관검색어 조작

- src/product/Type1

  검색어 입력 -> 사이트 클릭 -> 체류시간 (60 ~ 90초 사이) -> 쿠키 삭제 및 브라우저 초기화

- src/product/Type2

  검색어 입력 -> 검색어 및 사이트명 입력 (Ex 하이데브 검색 후 하이데브 개발사) -> 사이트 클릭 -> 체류시간 (60 ~ 90초 사이) -> 쿠키 삭제 및 브라우저 초기화

- src/product/Type3

  자동완성어 입력 -> 사이트명 입력 -> 검색어 입력 / 역순으로 검색이 중요 -> 백스페이스 -> 사이트 클릭 -> 체류시간
  
  (EX 하이데브 개발사 검색 -> 하이데브 -> 개발사 -> 백스페이스)

- src/product/Type4

  자동완성어 입력 -> 사이트명 입력 -> 검색어 입력 / 역순으로 검색이 중요 -> 사이트 클릭  -> 체류시간

- src/product/Type5

  쿼리값 입력 -> 사이트 클릭 -> 체류시간

  "https://search.naver.com/search.naver?display=15&f=&filetype=0&page=2&query=하이데브&research_url=&sm=tab_pge&start=1&where=web"

- src/product/Type6

  타입5에서 +값을 붙이고 사이트 클릭

  "https://search.naver.com/search.naver?display=15&f=&filetype=0&page=2&query=하이데브&oquery=개발사&research_url=&sm=tab_pge&start=1&where=web"

### API 통신
- https://crawler.hidev.link/crawl
  - GET

    오늘 날짜 기준으로 크롤링 진행되는 목록 조회
  - POST

    크롤링 정보 INSERT
    - Parameter

      type : 'site' / 'shop' / 'search', 

      URL_MID : 'URL 혹은 네이버쇼핑 MID', 

      keyword : '담을 키워드', 

      searchWord : '연관검색어', 

      loop : '한번 크롤링 시 반복할 횟수', 

      startDate : '반복시작일', 

      endDate : '반복종료일'

      * Date는 YYYY-MM-DD 형식
  - DELETE

  크롤링 정보 DELETE
    - Parameter

      crawlIdx : 삭제할 crawl_idx
