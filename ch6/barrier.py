# this example shows the use of barriers 

# time library
import time
# random number library
import random
# th library
from threading import Thread as th
from threading import Barrier

# barrier thread
def barrier():
    # all threads are waited to reach the barrier
    b_id = b.wait()
    first = time.perf_counter()
    print(f"{b_id} thread passed the first barrier! T:{first:2.3f}")
    # random delay  
    time.sleep(random.uniform(1,3))
    # second barrier reach time
    catch = time.perf_counter()
    print(f"{b_id} reached the second barrier.",
          f"Time:{catch - first : 2.3f} sn.")
    # all threads are waited to reach the second barrier
    b.wait()
    # barrier time
    second = time.perf_counter()
    print(f"{b_id} thread passed the second barrier! T:{second:2.3f}")
    
# main program block
if __name__ == "__main__":
    
    # Global data
    # thread count
    thread_count = 3
    # barrier definition
    b = Barrier(thread_count)
    # thread definitions
    threads = []
    for i in range(thread_count):
        t = th(target=barrier)
        threads.append(t)

    print("START!")    
    # start time
    start = time.perf_counter()
    print(f"start time : {start : 2.3f}")
    
    # all threads started
    for i in range(thread_count):
        threads[i].start()
    
    # all threads waited
    for i in range(thread_count):
        threads[i].join()

    # stop time
    stop = time.perf_counter()
    print(f"stop time : {stop : 2.3f}")
    print("STOP!")
    
    