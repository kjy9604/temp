from abc import ABCMeta, abstractmethod

class Crawler(metaclass = ABCMeta):
	def __init__(self):
		self.word = ""
		self.url = ""
		self.loop = 0
		self.crawl()
	@abstractmethod
	def crawl(self):
		pass

	def getCrawler(self):
		return {"word": self.word, "url": self.url, "loop": self.loop}
	
	def setWord(self, word):
		self.word = word
	
	def setUrl(self, url):
		self.url = url
	
	def setLoop(self, loop):
		self.loop = loop

	def setCrawler(self, word, url, loop):
		self.word = word
		self.url = url
		self.loop = loop
