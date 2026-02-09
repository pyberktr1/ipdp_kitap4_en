# Sample application that records web pages to disk
# web scraper module
from web import Web
# time performance
from time import perf_counter, sleep

# web addresses
site_names = [
                "http://www.sm0vpo.com/rx/tda7k-rx2.htm",
                "http://www.sm0vpo.com/rx/tba120-1.htm",
                "http://www.sm0vpo.com/rx/tda7000.htm",
                "http://www.sm0vpo.com/rx/quickrx.htm",
                "http://www.sm0vpo.com/rx/synth.htm",
                "http://www.elektormagazine.com/"
                ]

# web downloading starts
print(f"Downloading...")    
start = perf_counter()

# A thread is defined for each web page request task
threads = []
i = 0 # thread id counter
for name in site_names:
    i = i + 1
    thread = Web(name, i)
    threads.append(thread)    
    thread.start()

# threads are waited
total_thread_time = 0
for thread in threads:
    thread.join()
    print(thread)# result
    # total thread time that will be seen
    # when serial execution
    total_thread_time+=thread.ex_time
    
print(f"All tasks completed in {perf_counter()-start:2.5f} seconds.")
print(f"Total task time {total_thread_time: 2.5f} seconds.")