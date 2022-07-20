import threading
import time
from src import newCrawler
from flask import Flask, request
from flask_restx import Resource, Api
from abc import ABCMeta, abstractmethod
import queue
import pymysql
import datetime, json

# DB의 type
# shop : 네이버쇼핑
# search : 네이버 검색어순위 도출
# site : 실시간검색어 조작

###################################
### 이 호스트의 번호는 1번입니다 !!!!! ### # hostNum 수정할 라인
###################################

# Flask Settings
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
api = Api(app)

q = queue.Queue()

def connect():
	driver = pymysql.connect(
		user='crawl',
		passwd='crawl123$%^',
		host='crawler.cpaxhev3b6ts.ap-northeast-2.rds.amazonaws.com',
		database='crawl',
		charset='utf8'
	)
	return driver

# pymysql의 driver, cursor 닫기
def close(driver, cursor):
	driver.close()
	cursor.close()


def crawling():
	global q
	try:
		driver = connect()
		cursor = driver.cursor(pymysql.cursors.DictCursor)
		sql = f"""
					SELECT crawl_idx, crawl_type, keyword, search_word, url_mid, host_num, loop_count 
					FROM crawl.crawl 
					WHERE host_num = '1'
					AND loop_start_date <= now()
					AND loop_end_date >= now()
					ORDER BY crawl_idx DESC;""" # hostNum 수정할 라인
		
		cursor.execute(sql)
		result = cursor.fetchall()
		print('1')
		print(result)
		close(driver, cursor)
		if (len(result) == 0):
			print("크롤링 할 항목이 조회되지 않았습니다.")
			time.sleep(180)
			return crawling()
			
		for d in result:
			q.put(d)
		print('q size ::: ', q.qsize())
		for i in range(q.qsize()):
			inner = q.get() # DB row
			print(inner['crawl_type'])
			client = newCrawler.Client()
			client.create(inner['crawl_type'], inner['keyword'], inner['url_mid'], inner['loop_count'])
			if (inner['crawl_type'] == 'shop'):
				client.mid(inner['url_mid'])
			try:
				client.crawl()
			except Exception as e:
				print(e)
			time.sleep(180)
		return crawling()
	except Exception as e:
		print(e)
		return crawling()
	


@api.route('/crawl')
class Crawl(Resource):
	# 크롤링 할 리스트 가져옴
	def get(self):
		driver = connect()
		cursor = driver.cursor(pymysql.cursors.DictCursor)
		sql = f"""
					SELECT crawl_idx, crawl_type, keyword, search_word, url_mid, host_num, loop_count 
					FROM crawl.crawl 
					WHERE host_num = '1'
					AND loop_start_date <= now()
                    AND loop_end_date >= now()
					ORDER BY crawl_idx DESC;""" # hostNum 수정할 라인
		
		cursor.execute(sql)
		result = cursor.fetchall()
		result = json.dumps(result, ensure_ascii=False)
		# close(driver, cursor)
		return result

	def post(self):
		# 데이터 INSERT
		data = request.json
		if (data.get('type') is None or data.get('type') == '' or 
			data.get('URL_MID') is None or data.get('URL_MID') == '' or 
			data.get('keyword') is None or data.get('keyword') == '' or 
			data.get('searchWord') is None or data.get('searchWord') == '' or 
			data.get('loop') is None or data.get('loop') == '' or 
			data.get('startDate') is None or data.get('startDate') == '' or 
			data.get('endDate') is None or data.get('endDate') == ''):
			return 'Parameter is NULL'
		
		type = data.get('type')
		url_mid = data.get('URL_MID')
		keyword = data.get('keyword')
		searchWord = data.get('searchWord')
		loop = data.get('loop')
		startDate = data.get('startDate')
		endDate = data.get('endDate')

		driver = connect()
		cursor = driver.cursor(pymysql.cursors.DictCursor)
		sql = f"""INSERT INTO crawl.crawl(crawl_type, keyword, search_word, url_mid, host_num, loop_count, loop_start_date, loop_end_date) 
				VALUES('{type}', '{keyword}', '{searchWord}', '{url_mid}', '1', '{loop}', '{startDate}', '{endDate}');""" # hostNum 수정할 라인
		
		cursor.execute(sql)
		driver.commit()
		close(driver, cursor)

	def delete(self):
		# 데이터 DELETE
		data = request.json
		if (data.get('crawlIdx') is None or data.get('crawlIdx') == ''):
			return 'Parameter is NULL'
		
		crawlIdx = data.get('crawlIdx')

		driver = connect()
		cursor = driver.cursor(pymysql.cursors.DictCursor)
		sql = f"""DELETE FROM crawl.crawl WHERE crawl_idx = '{crawlIdx}' AND host_num = '1';""" # hostNum 수정할 라인
		
		cursor.execute(sql)
		driver.commit()
		close(driver, cursor)


if __name__ == '__main__':
	threading.Thread(target=lambda: app.run(host='127.0.0.1', port=5000, debug=False)).start()
	# crawling()
	threading.Thread(target=lambda: crawling()).start()
    # app.run(host='127.0.0.1', port=5000, debug=True)
	# print('main')
