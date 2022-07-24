from . import CrawlFactory
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from product import ShopRank

class ShopFactory(CrawlFactory.CrawlFactory):
    def createCrawler(self):
        return ShopRank.ShopRank()