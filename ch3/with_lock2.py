# This example shows the use of lock for
# correct resource sharing between threads
# in this version of the example we redesigned
# the task function to exclude the process delay
# from the critical region. 
# this example shows the importance of keeping
# context of the critical section limited.

# thread library
from threading import Thread, Lock
# time performance
from time import perf_counter, sleep

# shared resource
count = 0

# task using a lock to share a resource 
def task(id):
    # count defined as global for sharing
    global count
    # task repeated 5 times
    for i in range(5):
        
        # task delay is taken outside of the
        # critical region, since it is not related 
        # to the actual resource sharing taking
        # place in the critical region.
        sleep(0.2)

        # we are entering ciritical section
        lock.acquire()
        
        # critical region starts here
        
        # count incremented
        temp = count
        temp = temp + 1
            
        # count updated
        count = temp
    
        # task reported
        print(f"task#{id} has count = {count}\n", end="")
        
        # we are leaving critical section
        lock.release()

# main program block
# lock created
lock = Lock()

# start time
start = perf_counter()

# threads created
th1 = Thread(target=task, args=(1,))
th2 = Thread(target=task, args=(2,))

# threads started
th1.start()
th2.start()

# threads waited
th1.join()
th2.join()

# stop time
stop = perf_counter()

# results reported
print(f"Final count = {count}")
print(f"All tasks took {stop - start : 2.5f} seconds")
