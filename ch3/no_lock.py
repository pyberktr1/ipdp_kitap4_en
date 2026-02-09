# This example shows what happens when two threads 
# shares a resource without using a lock.

# thread library
from threading import Thread
# time eprformance
from time import perf_counter, sleep

# shared resource
count = 0

# a counter task
def task(id):
    # count declared as global for sharing
    global count
    # task repeats 5 times
    for i in range(5):
        # count incremented
        temp = count
        temp = temp + 1
    
        # task delay
        sleep(0.2)
        
        # count updated
        count = temp
    
        # task result
        print(f"task#{id} has count = {count}\n", end="")

# start time
start = perf_counter()

# threads created
th1 = Thread(target=task, args=(1,))
th2 = Thread(target=task, args=(2,))

# threads started
th1.start()
th2.start()

# threads are waited
th1.join()
th2.join()

# stop time 
stop = perf_counter()

# results reported
print(f"Final count = {count}")
print(f"All tasks took {stop - start : 2.5f} seconds")
