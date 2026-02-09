# using map() method for serial utilization of pool threads
# pool library
from concurrent.futures import ThreadPoolExecutor as thpx

# time performance
from time import perf_counter, sleep

def task(param):
    print(f"task#{param[0]} starts...")
    # task is handled here
    for _ in range(10):
        # I/O delay simulation
        sleep(0.1)
        # execution time calculated
        t = perf_counter()
        print(f"task#{param[0]} : time : {t - param[1]: 2.5f} ")
    return f" task#{param[0]} completed..."

# start time
start = perf_counter()

# two tasks are thrown to the pool
with thpx() as executor:
    results = executor.map(task, [[1, perf_counter()], [2, perf_counter()]])
    for result in results:
        print(result)

# stop time
stop = perf_counter()
print(f"Total execution time: {stop - start: 2.5f} seconds")
