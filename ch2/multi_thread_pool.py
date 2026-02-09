# sample application with thread pools
# thread pool library
from concurrent.futures import ThreadPoolExecutor as thpx

# time performtce
from time import perf_counter, sleep

def task(id, start):
    print(f"task#{id} starts...")
    # task handled here
    for _ in range(10):
        # I/O delay simulation
        sleep(0.1)
        # execution time calculated
        t = perf_counter()
        print(f"task#{id} : time : {t - start: 2.5f} ")
    return f" task#{id} completed..."

# start time
start = perf_counter()

# two tasks are thrown to the pool
with thpx() as executor:
    th1 = executor.submit(task, 1, perf_counter())
    th2 = executor.submit(task, 2, perf_counter())
    # results from the pool is reported
    print(th1.result())
    print(th2.result())    

# stop time
stop = perf_counter()
print(f"Total execution time: {stop - start: 2.5f} seconds")
