# this example shows how a message buffer can be
# shared between threads to pass messages safely
# using a lock

# thread library
from threading import Thread, Lock
# time performance
from time import perf_counter, sleep

# shared resources
buffer = [] # monitor task buffer
count = 0   # message counter

# monitor thread refresh time (in seconds)
refresh_time = 1

# task thread
def task(id):
    # buffer declared as global
    global buffer
    
    # local state variable
    state = 0
    
    # task repeated 100 times
    for i in range(100):
        # non-critical code section
        state = state + id
        sleep(0.1)
        
        # critical region with a context for
        # automatic release of the lock
        with lock:
            # critical code region
        
            # state is reported to the buffer
            buffer.append(f"task#{id} progress: {state}")
  
            # leaving critical region
            # we do not need a release() call since
            # we used a with context

# monitor thread for reporting messages
def monitor(refresh_time):
    # buffer declared as global for sharing
    global buffer
    # count declared as global 
    global count
    
    # buffer is dumped to display in an infinite loop
    while True:
        # refresh delay
        sleep(refresh_time)
        
        # a lock is acquired for buffer
        with lock:
            # all the messages dumped to the display
            for i in range(len(buffer)):
                count = count + 1
                print(buffer[i])
        
            # buffer flushed for reuse
            buffer = []
        
# main program block
# a lock created
lock = Lock()

# start time
start = perf_counter()

# threads created and started
threads = []
for i in range(1,11):
    thread = Thread(target=task, args=(i,))
    thread.start()
    threads.append(thread)

# monitor thread created and started
# it will be a daemon thread for
# automatic shutdown.
thread = Thread(target=monitor, args=(refresh_time,), daemon=True)
thread.start()

# threads waited
# we do not wait for monitor thread
for thread in threads:
    thread.join()
    
# stop time
stop = perf_counter()

# we need to wait for monitor task to complete full
# message dump
sleep(refresh_time*1.5)

# Final results are reported
print()
print(f"All tasks ended in {stop - start : 2.5f} seconds")
print(f"Totally {count} messages reported")
