# single threaded (serial) task operation sample
# time performance
from time import perf_counter, sleep

def task(id, start):
    print(f"task#{id} starts...")
    # task handled here
    for _ in range(10):
        # I/O delay simulation
        # There are empty wait states of the CPU
        # when waiting for I/O processes to complete
        # examples to I/O processes:
        # web queries, disk processes etc.
        sleep(0.1)#seconds
        # task completion time
        t = perf_counter()
        print(f"task#{id} : time interval : {t - start: 2.3f} ")
    print(f" task#{id} complete...")

# start time
start = perf_counter()

# two tasks are called in serial sequence
task(1, perf_counter())
task(2, perf_counter())

# stop time
stop = perf_counter()
print(f"Total execution time: {stop - start: 2.3f} seconds")
