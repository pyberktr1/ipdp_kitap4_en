# this example shows the use of semaphores to limit 
# sharing of resources between processes

# multi process library
from multiprocessing import Process, Semaphore, Array, Event
# time performance
import time
# random number generator
import random
# thread library
from threading import Thread as thread

# cleaning process
def cleaner(no, name, laundry, dishes, wash, dwash):
    # start time
    start = time.perf_counter()
    wash_stop = 0 # stop time for laundry washing process
    dish_stop = 0 # stop time for dish washing process
    print(f"{name} tries...")
    
    # cont. till all laundry and dish washing jobs are ccomplete
    while (laundry[no] > 0) or (dishes[no] > 0):
        # laundry queue
        if laundry[no]>0:# if no laundry do not wait
            # wait for a free washing machine
            print(f"\033[91m{name} waits for a free washing machine...\033[00m")
            result = wash.acquire(block=True,timeout=1)
            if not result:# time out
                print(f"\033[94m{name}: timed out when waiting for a wash machine.\033[00m")
            else:
                try:
                    print(f"\033[96m{name} washes laundry. Empty washers: ",
                          f"{wash.get_value()}\033[00m")
                    # washing process delay
                    time.sleep(laundry[no])
                    laundry[no] = 0        
                finally:
                    # job done, free washing machine
                    wash_stop = time.perf_counter() - start - dish_stop
                    print(f"\033[92m{name} completed laundry job in ",
                          f"{wash_stop:1.3f} seconds\033[00m")
                    wash.release()
                    print(f"{name}::L{wash.get_value()}")
                    
        # dish washing queue
        if dishes[no]>0:# if no dish to wash, then no wait
            # no dish washer is free, wait
            print(f"\033[91m{name} waits for a free dish washer...\033[00m")
            result = dwash.acquire(block=True,timeout=1)
            if not result:# time out
                print(f"\033[94m{name}: timed out when waiting for a dish washer.\033[00m")
            else:
                try:
                    print(f"\033[96m{name} washes dishes. Empty dish washers: ",
                          f"{dwash.get_value()}\033[00m")
                    # washing process delay
                    time.sleep(dishes[no])
                    dishes[no] = 0        
                finally:
                    # job done, free dish washing machine
                    dish_stop = time.perf_counter() - start - wash_stop
                    print(f"\033[92m{name} completed dish washing job in ",
                          f"{dish_stop:1.3f} seconds\033[00m")
                    dwash.release()
                    print(f"{name}::D{dwash.get_value()}")
            
    print(f"{name} completed all jobs in {time.perf_counter() - start:1.3f} seconds.")

# timer counter                    
def timer(close):
    # timer counter
    i = 0
    while not close.is_set():
        print(f"\033[95mSeconds : {i}\033[00m")
        time.sleep(1)
        i+=1

# main program block
if __name__ == "__main__":

    # only 3 laundry washers
    wash = Semaphore(3)

    # only 2 dish washers
    dwash = Semaphore(2)

    # 10 person will share the wash machines
    names = ["Bill  ", "Sam  ", "Jack  ", "John ", "Harry ",
               "Tom   ", "Hans  ", "Victor", "Terry ", "Bob   "]
    
    # laundry and dish washer jobs are created
    # for each person
    laundry = Array('f', len(names))
    dishes  = Array('f', len(names))
    for i in range(len(names)):
        laundry[i] = 5#(random.uniform(2,5))
        dishes[i]  = 5#(random.uniform(2,5))

    # timer thread and stop event
    close = Event()
    z_thread  = thread(target=timer, args=(close,))
    z_thread.start()

    # we set a process for each person and start
    processes  = []
    for i in range(len(names)):
        p = Process(target=cleaner, args=(i, names[i], laundry, 
                     dishes, wash, dwash, ))
        processes.append(p)
        p.start()
    
    # wait for processes to be completed    
    for p in processes:
        p.join()
    
    # stop timer 
    close.set()
    z_thread.join()
        
    print("\nEmpty machines:",
          f"\nWasher:{wash.get_value()} :: D.washer:{dwash.get_value()}")
    print("Everybody finished work!")
    
