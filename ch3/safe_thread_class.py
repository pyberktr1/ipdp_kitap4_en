# this example shows the implementation of a 
# safe thread class that uses a lock

# thread library
from threading import Thread, Lock
# time performance
from time import perf_counter, sleep

# shared resources
message = []
count   = 0

# monitor thread refresh time (in seconds)
refresh_time = 1

# fiber class created
class fiber:
    # initialization body
    def __init__(self):
        # global variables
        self.message = []
        self.count   = 0
        self.lock    = Lock()
    
    # class task
    def task(self, id):
        # local status variable
        status = 0
    
        # task repeated 100 times
        for i in range(100):
            status = status + id
            sleep(0.1)
        
            # critical section        
            with self.lock:
                # message put to buffer
                self.message.append(f"task#{id} progress: "
                                  f"{status}")
    # monitor task
    def monitor(self, refresh_time):
        # monitor refresh counter
        refresh_counter = 0
        # message dump loop
        while True:
            # refresh delay
            sleep(refresh_time)
            refresh_counter+=1
            print(f"\nrefresh count: {refresh_counter}")
        
            # message buffer acquires lock
            with self.lock:
                # all messages in the buffer dumped
                for i in range(len(self.message)):
                    self.count = self.count + 1
                    print(self.message[i])
        
                # message buffer flushed
                self.message = []

# main program block
# a fiber is created from fiber class
f = fiber()

# start time
start = perf_counter()

# threads created and started
threads = []
for i in range(1,11):
    thread = Thread(target=f.task, args=(i,))
    thread.start()
    threads.append(thread)

# daemon thread monitor created and started
thread = Thread(target=f.monitor, args=(refresh_time,), daemon=True)
thread.start()

# threads waited
for thread in threads:
    thread.join()
    
# stop time
stop = perf_counter()

# waiting for buffer dump to complete
sleep(refresh_time*1.5)

# final results are reported
print()
print(f"All tasks are ended in {stop - start : 2.5f} seconds")
print(f"Totally {f.count} messages reported")
