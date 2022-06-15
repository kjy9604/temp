import requests
from bs4 import BeautifulSoup as bs

flag = False # 2페이지에서 검색 결과가 없을 때 3페이지 전환용
rank = "X" # 기본값 X, 있을 시 몇번째에 있는지 반환
start = 1
pageNum = 2
word = "highdev.pro"
query = "하이데브"
url = f"https://search.naver.com/search.naver?display=15&f=&filetype=0&page={pageNum}&query={query}&research_url=&sm=tab_pge&start={start}&where=web"
def crawl(query, word, pageNum, start):

	page = requests.get(url)
	soup = bs(page.text, "html.parser")


	elements = soup.select('li.bx div > div.total_tit_group')

	for index, element in enumerate(elements, start):
		print("{} 번째 게시글의 제목: {}".format(index, element.text))
		if (word in element.text) :
			print("True!!")
			flag = True
			rank = index
			# return 하면 될듯?
			break

	if (flag == True) :
		return rank
	elif (flag == False and pageNum == 2) : 
		start = 16
		pageNum = 3
		return crawl(query, word, pageNum, start)
	else :
		return rank
	
	