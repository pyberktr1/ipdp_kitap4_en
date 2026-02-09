# This module handles web requests using thread class
# threading library
from threading import Thread
# web requests library
import requests
# time performance
from time import perf_counter, sleep

# web scraper class
class Web(Thread):
    # initializer
    def __init__(self, name: str, id: None) -> None:
        super().__init__()
        self.name    = name            # site address
        self.st_time = perf_counter()  # start time
        self.id      = id              # id
        self.status  = None            # site status
        self.ex_time = None            # execution time
    
    # execution method
    def run(self):
        # for delay simulation add a # to the beginning of the line 
        """ 3 nolu ipi kasıtlı olarak bekletiyoruz
        if self.id == 3:
            sleep(3)
            #"""
        # header string for identification
        header = {
            "User-Agent":   "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "+
                            "AppleWebKit/537.36 (KHTML, like Gecko) "+
                            "Chrome/138.0.0.0 Safari/537.36 "
        }
        # web request is made here
        # result is recorded
        result = requests.get(self.name, headers = header)
        # request status is recorded
        self.status = result.status_code
        if  self.status == 200: # web page download successful
            # HTML data written to file
            with open(f".\\webs\\web_{self.id}.htm", 'wb') as f:
                f.write(result.text.encode("UTF-8"))
        # execution time
        self.ex_time = perf_counter() - self.st_time
        
    # the string data provided when a print() request is
    # made to the class 
    def __str__(self):
        msg = f"{self.id} :: Site : {self.name:50s} : "
        msg+= f"status : {self.status} :: Time : {self.ex_time: 2.5f} seconds"
        return msg
               
