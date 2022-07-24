from abc import ABCMeta, abstractmethod

class CrawlFactory(metaclass=ABCMeta):
    @abstractmethod
    def createCrawler(self):
        ''' factory method '''
        pass
