
from interface.etl_interface import ETLInterface
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

class ShopeeETL(ETLInterface):
    def crawl(self):
        print("Crawl data")

    def transform(self):
        print("Transform data")

    def load(self):
        print("Load data")



