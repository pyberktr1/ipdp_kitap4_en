# Another example for multi-threaded task operation
# using for loops to create and start threads
# time performance
from time import perf_counter, sleep
# threading library
from threading import Thread

def task(id, start):
    print(f"task#{id} starts...\n", end="")
    # task handled here
    for _ in range(2):
        # I/O delay
        sleep(0.1)
        # time interval
        t = perf_counter()
        print(f"task#{id} took: {t - start: 2.3f} seconds\n", end="")
    # task#3 is blocked here intentionally
    # busy waits are not wanted in threads
    # since they steal CPU time
    # if waits are mandotory then use sleep() method instead
    while (id == 3):
        pass
        
    print(f" task#{id} completed...\n", end="")

# start time
start = perf_counter()

# 5 threads are initialized here
threads = []
for i in range(1,6):
    threads.append(Thread(target = task, args = (i, perf_counter(),)))
    threads[i-1].start()

# wait for tasks to complete
for thread in threads:
    thread.join()

# stop time
stop = perf_counter()
print(f"Total execution time: {stop - start: 2.3f} seconds\n", end="")
