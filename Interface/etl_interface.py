from abc import ABC, abstractmethod

class ETLInterface:
    @abstractmethod
    def run_crawl(self):
       pass

    @abstractmethod
    def run_transform(self):
        pass 
    
    @abstractmethod
    def run_load(self):
        pass

    @abstractmethod
    def run_all(self):
        pass