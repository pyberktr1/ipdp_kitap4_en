# this example uses non-blocking semaphores to share resources
# between processes

# multi process library
from multiprocessing import Process, Semaphore, Array, Event
# time library
import time
# random number library
import random
# thread library
from threading import Thread as thread

# cleaning process with non-blocking semaphores
def cleaner(no, name, laundry, dishes, wash, dwash):
    # startlangic anini kaydet
    start = time.perf_counter()
    wash_stop = 0
    dish_stop = 0
    print(f"{name} tries...")
    
    # cont. till all jobs done
    while True:
        # laundry queue
        if laundry[no]>0:# no laundry no wait
            if wash.acquire(block=False):
                print(f"\033[96m{name} washes laundry. Empty washers: ",
                      f"{wash.get_value()}\033[00m")
                # washing process delay
                time.sleep(laundry[no])
                laundry[no] = 0
                # job done, free washer
                wash_stop = time.perf_counter() - start - dish_stop
                print(f"\033[92m{name} completed laundry job in ",
                      f"{wash_stop:1.3f} seconds\033[00m")
                wash.release()
                
        # dishes queue
        if dishes[no]>0:# no dish no wait
            if dwash.acquire(block=False):
                print(f"\033[96m{name} washes dishes. Empty dish washers: ",
                      f"{dwash.get_value()}\033[00m")
                # washing process delay
                time.sleep(dishes[no])
                dishes[no] = 0
                # job done, free washer
                dish_stop = time.perf_counter() - start - wash_stop
                print(f"\033[92m{name} completed dish job in ",
                      f"{dish_stop:1.3f} seconds\033[00m")
                dwash.release()
                
        # retry delay, applied if a job is left
        if (laundry[no] > 0) or (dishes[no] > 0):
            time.sleep(0.1)
        else:
            print(f"{name} completed all the jobs in {time.perf_counter() - start:1.3f}",
                    " seconds.")
            break

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
    