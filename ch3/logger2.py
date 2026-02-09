# In this example an event is used to regulate
# the message dump refresh of the monitor task

# thread library
from threading import Thread, Lock, Event
# time performance
from time import perf_counter, sleep

# shared resources
message = []
count = 0

# task thread
def task(id):
    # message defined as global
    global message
    
    # local status variable
    satus = 0
    
    # task is repeated 100 times
    for i in range(100):
        # non-critical region
        satus = satus + id
        sleep(0.1)
        
        # critical region
        with lock:
            # satus message send to buffer
            message.append(f"task#{id} progress: {satus}")
  
            # we set a message full signal for refreshing
            buffer_full.set()
            
# monitor thread
def monitor():
    # message defined as global 
    global message
    # count defined as global
    global count
    
    # messages dumped to display
    while True:
        # a buffer full event is waited for refreshing
        buffer_full.wait()
        
        # message buffer acquires lock
        with lock:
            # messages are dumped
            for i in range(len(message)):
                count = count + 1
                print(message[i])
        
            # message buffer flushed
            print("*")
            message = []
            
            # buffer_full signal is reset since
            # message box is emptied
            buffer_full.clear()

# main program block
# a lock is created
lock = Lock()

# message buffer full event is created
buffer_full = Event()

# start time
start = perf_counter()

# threads created and started
threads = []
for i in range(1,11):
    thread = Thread(target=task, args=(i,))
    thread.start()
    threads.append(thread)

# monitor daemon is created and started
thread = Thread(target=monitor, daemon=True)
thread.start()

# threads waited
for thread in threads:
    thread.join()
    
# stop time
stop = perf_counter()

# delay for last messages to be dumped
buffer_full.set()
sleep(1)

# final results reported
print()
print(f"All tasks ended in {stop - start : 2.5f} seconds.")
print(f"Totally {count} messages reported.")
