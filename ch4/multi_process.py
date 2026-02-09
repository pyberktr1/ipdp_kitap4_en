# this example shows how using multi processes are used to 
# speed up a complex calculation

# time performance
import time
# multi_porcess library
import multiprocessing

# process task
def task(intervals, pid, q):
    # result
    result = []

    # a complex calculation task
    for i in range(intervals[0], intervals[1]):
        # a complex function
        p = ((((i+0.1)**2)/3.141)**2 + (i+1.2)*1.288**2)**0.5 - (25.5/(i-3.22))**1.148
        result.append(p)
    
    # result thrown to the queue
    q.put({pid : result})
    
if __name__ == '__main__':
    
    # start time
    start = time.perf_counter()
    
    # result
    result = []
    
    q = multiprocessing.Queue()

    # intervals calculated
    intervals = []
    interval_count = 10
    interval = 10**7//interval_count
    for i in range(0, interval_count):
        intervals.append([i*interval, (i+1)*interval])

    # processes
    processes = []
    
    # processes created
    for i in range(interval_count): # 10 intervals
        processes.append(multiprocessing.Process(target=task, 
                                            args=(intervals[i], i, q, )))

    # processes started
    for i in range(interval_count):
        processes[i].start()
    
    # results are drawn from queue
    d = {}
    for i in range(interval_count):
        d.update(q.get())
    
    # data in the dictionary is ordered into a list
    for i in range(interval_count):
        val = d.pop(i, None)
        if val == None:
            print("Data error! ", val)
        else:
            result = result + val
    
    stop = time.perf_counter()
   
    print(f"calculation took {stop - start : 3.5f} seconds")
    
    print(result[0])
