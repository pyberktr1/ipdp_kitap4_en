# this example shows data sharing between processes
# this is a more advanced example

# multi process library
from multiprocessing import Process, Value, Lock
# time performance
import time
# random number library
import random

# cabinet sharing process
def cabinet(name, empty_cabinet):
    # start time
    start = time.perf_counter()
    
    # try until a cabinet is empty
    while True:
        # we acquire a lock to the shared value
        with empty_cabinet.get_lock():
            # are there any empty cabinets?
            if empty_cabinet.value > 0:
                # yes
                empty_cabinet.value -= 1
                print(f"\033[96m{name} entered to a cabinet. empty cabinets: ",
                      f"{empty_cabinet.value}\033[00m")
                break
        
        # no empty cabinets, wait...
        print(f"\033[91m{name} waits...\033[00m")
        # try again some time later...
        time.sleep(1)
        print(f"\033[93m{name} retries...\033[00m")

    # dress in the cabinet
    time.sleep(2 + random.uniform(0,3))
    # job accomplished, free the cabinet for others to use
    with empty_cabinet.get_lock():
        empty_cabinet.value +=1
    print(f"\033[92m{name} dressed in ",
          f"{time.perf_counter() - start :1.3f} seconds.\033[00m")

# main program block
if __name__ == "__main__":

    # there are only 3 cabinets
    empty_cabinet = Value('i', 3)

    # there are 5 persons to use the cabinets
    names = ["Harry", "Bill", "Jack", "John", "Mike"]

    # we set a process for each person
    processes = []
    for name in names:
        p = Process(target=cabinet, args=(name, empty_cabinet, ))
        processes.append(p)
        p.start()
        
    # time counts
    for i in range(9):
        print(f"\033[95mSeconds : {i}\033[00m")
        time.sleep(1)
    
    # wait for the processes   
    for p in processes:
        p.join()
        
    print(f"\nFinal number of empty cabinets: {empty_cabinet.value}")
    print("Everybody completed his job!")
    
