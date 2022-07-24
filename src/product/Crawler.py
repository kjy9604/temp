from abc import ABCMeta, abstractmethod

# Product
class Crawler(metaclass=ABCMeta):
    @abstractmethod
    def crawl(self):
        pass
