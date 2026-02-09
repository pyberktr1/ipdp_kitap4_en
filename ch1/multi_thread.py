# multi thread sample application
# time performance library
from time import perf_counter, sleep
# thread library
from threading import Thread

def task(id, start):
    print(f"Task#{id} starts...\n", end="")
    # task is handled here
    for _ in range(10):
        # I/O delay simulation
        # There are empty wait states of the CPU
        # when waiting for I/O processes to complete
        # examples to I/O processes:
        # web queries, disk processes etc.
        sleep(0.1)
        # time interval of the query is calculated here
        interval = perf_counter()
        print(f"Task#{id} : interval : {interval - start: 2.3f} \n", end="")
    print(f" Task#{id} complete...\n", end="")

# start time is recorded
start = perf_counter()

# sperate threads for each task is initialized
ip1 = Thread(target = task, args = (1, perf_counter(),))
ip2 = Thread(target = task, args = (2, perf_counter(),))

# start the threads
ip1.start()
ip2.start()

# wait for completion of each task
ip1.join()
ip2.join()

# stop time is recorded
stop = perf_counter()
print(f"Total execution time: {stop - start: 2.3f} seconds\n", end="")
