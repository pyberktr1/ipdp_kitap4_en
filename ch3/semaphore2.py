# sample application for web image download using thread pool
# this version of image download example uses two semaphores to
# limit the resource usages: one for web operations and the other
# for limiting the file operations

# thread pool library
from concurrent.futures import ThreadPoolExecutor as thpx
# web requests library
import requests
# used for converting image names in a proper format
import urllib.parse
# thread library
import threading

# download limit parameters
max_down_limit = 3
# semaphore created
semaphore_web = threading.Semaphore(max_down_limit)

# file limit parameters
max_file_limit = 2
# semaphore created
semaphore_file = threading.Semaphore(max_file_limit)

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

    # semaphore is used to limit download rate
    with semaphore_web:
        # file name rearranged
        f_name = urllib.parse.unquote(os.path.basename(url).replace("File:",""))
        print(f"\033[91m{f_name} is being downloaded...\033[0m")        
        # web resource is opened for download
        # result is recorded
        result = requests.get(url, headers = header)
        # request result is recorded
        status = result.status_code
        if status == 200: # success
            # request data is recorded here
            data = result.content
            print(f"{f_name} is downloaded...")
            print(f"\033[92m{f_name} is being opened..\033[0m")
            # image data is recorded to disk
            with open(f"./images/{f_name}", 'wb') as im_f:
                im_f.write(data)
                print(f'{f_name} is recorded...')
        else:
            print(f"\033[91mError!: {url} :: code={status} \033[0m")

    # file operations take place here   
    if status == 200: # success
        # second semaphore limits the file use
        with semaphore_file:
            print(f"\033[92m{f_name} is being opened..\033[0m")
            # we are giving an intentional delay to make a
            # bottleneck for file operations
            time.sleep(3)
            # image data is recorded to disk
            with open(f"./images/{f_name}", 'wb') as im_f:
                im_f.write(data)
                print(f'{f_name} is recorded...')
        
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
