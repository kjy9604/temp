import threading
from flask import Flask
import requests
from bs4 import BeautifulSoup as bs
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import random
from abc import ABCMeta, abstractmethod

# Flask Settings
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


q = queue.Queue()

class RequestHandling:
    def __init__(self):
        self.crawling_api = RequestCrawlingAPI()

    def async_requests(self):
        while True:
            if not q.empty() > 0:
              self.crawling_api.request_handling(q.get())

@app.before_first_request
def before_first_request():
    req = RequestHandling()
    threading.Thread(target=req.async_requests).start()


class RequestCrawlingAPI(Resource):
	def get(self):
		return
		

def closeAllChrome(driver):
	driver.delete_all_cookies()
	driver.close()
	driver.quit()
	print(driver.session_id)
	time.sleep(120)
	return None

# word = "highdev.pro"
# query = "하이데브"
@app.route('/searchRank/<query>/<word>')
def searchRank(query, word):

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
			# return 하면 될듯?
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
				# return 하면 될듯?
				return str(rank)
			
		return str(rank)
	
@app.route('/shopRank/<query>/<prevQuery>/<mid>')
def shopRank(query, prevQuery, mid):

	url = f"https://search.shopping.naver.com/search/all?query={query}&frm=NVSHATC&prevQuery={prevQuery}"
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

@app.route('/siteRank/<query>/<word>')
def siteRank(query, word):
	num = random.randrange(1, 7)
	print(f'랜덤번호 : {num}')
	result = ''
	if num == 1 :
		result = type1(query, word)
	elif num == 2 :
		result = type2(query, word)
	elif num == 3 :
		result = type3(query, word)
	elif num == 4 :
		result = type4(query, word)
	elif num == 5 :
		result = type5(query, word)
	else :
		result = type6(query, word)
	
	return result

def connection(): 
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

@app.route('/type1/<query>/<word>')
def type1(query, word):
	print("this is type1 !!!!")
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


@app.route('/type2/<query>/<word>')
def type2(query, word):
	print("this is type2 !!!!")
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


@app.route('/type3/<query>/<word>')
def type3(query, word):
	print("this is type3 !!!!")
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

@app.route('/type4/<query>/<word>')
def type4(query, word):
	print("this is type4 !!!!")
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

@app.route('/type5/<query>/<word>')
def type5(query, word):
	print("this is type5 !!!!")
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

@app.route('/type6/<query>/<word>')
def type6(query, word):
	print("this is type6 !!!!")
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


@app.route('/ipCheck')
def ipCheck():

	# chrome_options = webdriver.ChromeOptions()
	# chrome_options.add_argument('--headless')
	# chrome_options.add_argument('--no-sandbox')
	# chrome_options.add_argument("--single-process")
	# chrome_options.add_argument("--disable-dev-shm-usage")
	# chrome_options.add_argument("--proxy-server=socks5://127.0.0.1:9150")
	# path='../chromedriver'
	# browser = webdriver.Chrome(path, options=chrome_options)
	PROXY="localhost:9150"
	opts = Options()
	user_agent = 'Mozilla/5.0 CK={} (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'

	webdriver.DesiredCapabilities.CHROME['proxy'] = {
		"httpProxy": PROXY,
		"ftpProxy": PROXY,
		"sslProxy": PROXY,
		"proxyType": "MANUAL",
	}

	webdriver.DesiredCapabilities.CHROME['acceptSslCerts']=True


	opts.add_argument("user-agent="+user_agent)
	opts.add_argument('--headless')
	opts.add_argument('--no-sandbox')
	opts.add_argument('--proxy-server='"socks5://"+PROXY)

	print(webdriver.DesiredCapabilities.CHROME)

	driver =webdriver.Chrome(executable_path="../chromedriver",options=opts)


	# driver.get('https://www.expressvpn.com/what-is-my-ip')
	# user_agent_check = driver.execute_script("return navigator.userAgent;")
	# print(user_agent_check)
	# return user_agent_check

	driver.get('http://checkip.dyndns.org')
	time.sleep(5)
	soup = bs(driver.page_source, "html.parser")
	print(soup)
	element = soup.select_one('body').getText().split()
	print(element)
	driver.close()
	return element[3]

@app.route('/ipCheck2')
def ipCheck2():
	url = "http://icanhazip.com/"
	proxies = {
		'http': 'socks5://127.0.0.1:9050',
		'https': 'socks5://127.0.0.1:9050'
	}

	response = requests.get(url, proxies=proxies)
	print('tor ip: {}'.format(response.text.strip()))
	return 'asd'

@app.route('/test')
def testDef():
	str1 = "가나다라바"
	str2 = "abc,def,ghi"
	str1_to_arr = str1.split(',')
	str2_to_arr = str2.split(',')
	print(str1_to_arr) # ['가나다라바']
	print(str2_to_arr) # ['abc', 'def', 'ghi']
	print(len(str1_to_arr)) # 1
	print(len(str2_to_arr)) # 3
	return 'asdas'

if __name__ == '__main__':
    app.run(debug=True)