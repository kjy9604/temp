from . import CrawlFactory
import random
# from ..product import Type1, Type2, Type3, Type4, Type5, Type6
# from ..product.Type1 import Type1
# from ..product.Type2 import Type2
# from ..product.Type3 import Type3
# from ..product.Type4 import Type4
# from ..product.Type5 import Type5
# from ..product.Type6 import Type6

import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from product import Type1, Type2, Type3, Type4, Type5, Type6

class SiteFactory(CrawlFactory.CrawlFactory):
    def createCrawler(self):
        num = random.randrange(1, 7)
        if num == 1:
            return Type1.Type1()
        elif num == 2:
            return Type2.Type2()
        elif num == 3:
            return Type3.Type3()
        elif num == 4:
            return Type4.Type4()
        elif num == 5:
            return Type5.Type5()
        else:
            return Type6.Type6()