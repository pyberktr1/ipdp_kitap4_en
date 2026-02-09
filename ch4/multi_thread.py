# this example shows that it is not possible to speed up
# calculations by multi-threading.

# time performance
import time
# thread library
import threading
# queue library
import queue

# thread task
def task(intervals, id, q):
    # result
    result = []

    # a complex calculation task
    for i in range(intervals[0], intervals[1]):
        # a complex function
        p = ((((i+0.1)**2)/3.141)**2 + (i+1.2)*1.288**2)**0.5 - (25.5/(i-3.22))**1.148
        result.append(p)
    
    # result put to a queue
    q.put({id : result})
    
if __name__ == '__main__':

    # start time
    start = time.perf_counter()
    
    # results
    result = []
    
    q = queue.Queue()

    # intervals calculated
    intervals = []
    interval_count = 10
    interval = 10**7//interval_count
    for i in range(0, interval_count):
        intervals.append([i*interval, (i+1)*interval])

    # threads
    threads = []
    
    # threads created
    for i in range(interval_count): # 10 interval/thread
        threads.append(threading.Thread(target=task, args=(intervals[i], i, q, )))

    # threads started
    for i in range(interval_count):
        threads[i].start()
    
    # results drawn from threads
    d = {}
    for i in range(interval_count):
        d.update(q.get())
    
    # dictionary data is ordered in a list
    for i in range(interval_count):
        val = d.pop(i, None)
        if val == None:
            print("Data error! ", val)
        else:
            result = result + val
    
    stop = time.perf_counter()
   
    print(f"calculation took {stop - start : 3.5f} seconds")
    
    print(result[0])
