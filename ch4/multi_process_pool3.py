# This example divides the workload using "chunksize" parameter of
# the process pool used. 

# time performance
import time
# process pool library
from concurrent.futures import ProcessPoolExecutor as p_executor

# proses taski
def task(i):

    # a complex function
    p = ((((i+0.1)**2)/3.141)**2 + (i+1.2)*1.288**2)**0.5 - (25.5/(i-3.22))**1.148
    
    # result returned
    return p
    
if __name__ == '__main__':
    
    # start time
    start = time.perf_counter()
    
    # result
    result = []
    
    # interval calculations
    interval = 10**7
    interval_count = 10
    chunks = interval//interval_count
    
    # process pool created and executed
    with p_executor() as executor:
        for res in executor.map(task, range(interval), chunksize=chunks):
            result.append(res)
                  
    stop = time.perf_counter()
   
    print(f"calculations took {stop - start : 3.5f} seconds")
      
    print(result[0])
