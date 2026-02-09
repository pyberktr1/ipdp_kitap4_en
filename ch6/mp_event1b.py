# this example shows the use of queues for concurrent processing
# of parts in the production line

# multi process library
from multiprocessing import Process, Event, Queue
# this signals are defined only in queue library
from queue import Empty, Full

# time performance
from time import sleep
# thread library
from threading import Thread as th

# production line process
def machine(name, in_q, out_q):
    # parts counter
    i = 0
    print(f"{name} waits...")
    # cont. till system shutdown
    stop = False
    while not stop:
        # get a paert from queue
        try:
            i = in_q.get(timeout=5)
            print(f"{name} processes part#{i}!")
            # we set a fault here
            #if name=="Press" and i==3:
            #    stop = True
            #    continue
            # normal process delay
            sleep(1)
            print(f"{name} finished processing part#{i}!")
        except Empty as error: # queue timed out
            stop = True
            continue
        
        # we put the processed part to the output queue
        try:
            out_q.put(i, timeout=5)
        except Full as error: # output queue timed out
            stop = True
    
    # finalize the process    
    print(f"{name} timed out in part#{i}",
           ". \n All systems will be de-activated...")
    
# zaman sayaci                    
def clock(clock_stop):
    i = 0 # seconds counter
    # count seconds in a loop
    while not clock_stop.is_set():
        print(f"\033[95mSaniye : {i}\033[00m")
        sleep(1)
        i+=1
                     
# main program block
if __name__ == "__main__":
    
    # number of parts to be processed
    part_count = 10

    # mechanical systems created
    mech_sys  = ["Feeder", "Press", "Paint", "Oven"]
    
    # queues created
    queues    = [Queue(maxsize=part_count) for _ in range(len(mech_sys)+1)]
    
    # a process for each system is created
    processes = []
    for i in range(len(mech_sys)):
        processes.append(Process(target=machine, args=(mech_sys[i], queues[i], 
                            queues[i+1],)))

    # timer thread
    clock_stop = Event()
    clock_th   = th(target=clock, args=(clock_stop, ))
    clock_th.start()

    # processes started
    for p in processes:
        p.start()
    
    # initial delay
    sleep(1)
    # all parts goes to feeder
    for i in range(part_count):
        sleep(0.5)
        queues[0].put(i+1)
        print(f"part#{i} sent for processing...")
    
    # processes waited
    for p in processes:
        p.join()
    
    # stop timer
    clock_stop.set()
    clock_th.join()

    # all queues are closed
    for i in range(len(mech_sys)+1):
        queues[i].close()
    
    print("ALL SYSTEMS ARE CLOSED!")