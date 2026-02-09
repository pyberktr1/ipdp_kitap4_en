# this example shows the usage of process pools
# for limiting the resource utilization

# operating system library
import os

# time performance
import time
# multi process pool library
from concurrent.futures import ProcessPoolExecutor as p_executor

# process task
def task(intervals, pid):
    # result
    result = []

    # a complex calculation is made
    for i in range(intervals[0], intervals[1]):
        # a complex function
        p = ((((i+0.1)**2)/3.141)**2 + (i+1.2)*1.288**2)**0.5 - (25.5/(i-3.22))**1.148
        result.append(p)
    
    # result returned
    d = [pid, result]
    return d
    
if __name__ == '__main__':

    # cpu count is queried
    cpu_count = os.cpu_count()
    print("CPU count = ", cpu_count)

    # start time
    start = time.perf_counter()
    
    # result
    result = []
    
    # intervals calculated
    intervals = []
    pids      = []
    interval_count = 10
    interval = 10**7//interval_count
    for i in range(0, interval_count):
        intervals.append([i*interval, (i+1)*interval])
        pids.append(i)
    
    # process id list (ordered according to execution order)
    pid_list = [] 
    
    # process pool created and executed
    # we limit cpu utilization by setting the worker process
    # number below the cpu count. It is factorized by 20 here
    # lowering this factor increases the number of CPU cores
    # that are utilized in processes.
    with p_executor(max_workers=cpu_count//20) as executor:
        results = executor.map(task, intervals, pids)
        
        # results are automatically ordered by the executor
        for res in results:
            pid_list.append(res[0])
            result = result + res[1]

            
    stop = time.perf_counter()
   
    print(f"calculation took {stop - start : 3.5f} seconds")
    
    # results always come in order
    print(pid_list)
    
    print(result[0])
