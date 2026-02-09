# sample application for web image download using thread pool
# thread pool library
from concurrent.futures import ThreadPoolExecutor as thpx
# web requests library
import requests
# used for converting image names in a proper format
import urllib.parse

# time performance
import time
# operating system utility library
import os

# image download task
def down_image(url):
    # header string used for browser identification
    # proper identification is necessary for a
    # healthy download operation
    header = {
            "User-Agent":   "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "+
                            "AppleWebKit/537.36 (KHTML, like Gecko) "+
                            "Chrome/138.0.0.0 Safari/537.36 "
        }
    # binary image data
    data = None
    # web request is made here
    # result is recorded
    result = requests.get(url, headers = header)
    # request status recorded
    status = result.status_code
    if status == 200: # success
        # data is recorded to content property of result
        data = result.content
        # file name is arranged
        f_name = urllib.parse.unquote(os.path.basename(url).replace("File:",""))
        # image data is recorded to the file
        with open(f"./images/{f_name}", 'wb') as im_f:
            im_f.write(data)
            print(f'{f_name} recorded...')
    else:
        print(f"\033[91mError!: {url} :: code={status} \033[0m")
        # end of task
        return # nothing returned as result
        
# main program block
start = time.perf_counter()

urls = [

    "http://www.sm0vpo.com/rx/tda7k-rx2_01cct.gif",
    "http://www.sm0vpo.com/rx/tda7k-rx2e.jpg",
    "http://www.sm0vpo.com/rx/tda7k",#wrong address!
    "http://www.sm0vpo.com/rx/tda7k-rx2b.jpg",
    "http://www.sm0vpo.com/rx/tda7k-rx2a.jpg",
    "http://www.sm0vpo.com/rx/tda7k-rx2f.jpg",
    "http://www.sm0vpo.com/rx/tda7k-rx2c.jpg",
    "http://www.sm0vpo.com/rx/tda7k-rx2d.jpg"

]
# threads are withdrawn from the pool 
with thpx() as executor:
      executor.map(down_image, urls)

stop = time.perf_counter()    

print(f"All image download operations took {stop - start : 2.5f} seconds")
