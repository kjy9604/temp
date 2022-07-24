from . import CrawlFactory
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from product import SearchRank

class SearchFactory(CrawlFactory.CrawlFactory):
    def createCrawler(self):
        return SearchRank.SearchRank()