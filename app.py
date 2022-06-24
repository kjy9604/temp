import threading
from flask import Flask
from flask_api import status
from flask_restplus import Resource, Api
import requests
from bs4 import BeautifulSoup as bs
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import random
import time
from abc import ABCMeta, abstractmethod

# Flask Settings
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
api = Api(app, version='1.0', title='크롤러', description='크롤러 API')
ns = api.namespace('Crawler', description='Crawlers')
app.config.SWAGGER_UI_DOC_EXPANSION = 'full'


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


@ns.route('/siteRank/<string:keyword>/<string:url>/<int:loop>')
@ns.response(200, 'Found')
@ns.response(404, 'Not found')
@ns.response(500, 'Internal Error')
@ns.param('keyword', '검색어')
@ns.param('url', '검색어로 찾을 URL')
@ns.param('loop', '반복할 횟수')
class RequestCrawlingAPI(Resource):
	@ns.doc('get')
	def get(self):
		return

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)