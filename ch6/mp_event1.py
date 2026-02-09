# this example shows the use of events in multi processes

# multi process library
from multiprocessing import Process, Event
# time performance
from time import sleep
# thread library
from threading import Thread as th

# production machine process
# products are processed in a serial sequence
def machine(name, event, next_event, stop_event):
    i = 0 # element counter
    # cont. till stop signal is active
    while not stop_event.is_set():
        print(f"{name} waits...")
        # trigger event is waited
        # if it is delayed (timeout) then
        # system is automatically closed
        if (event.wait(timeout=5)):
            # trigger event is active
            i+=1 # increment counter
            print(f"{name} takes {i} part!")
            # we set a fault here
            #if name=="Press" and i==3:
            #    sleep(6)
            # normal process delay
            sleep(1)
            print(f"{name} finished {i} part!")
            next_event.set() # trigger next system
            event.clear() # activation event is reset
        else: # there is a timeout due to a fault in the system
            print(f"{name} timed out in {i} part.", 
                   "\nAll systems will be closed...")
            stop_event.set()# stop signal is active
    
    print(f"{name} closed!")

# time counter                    
def clock(clock_stop, stop_event):
    i = 0 # seconds counter
    # count seconds until close
    while not clock_stop.is_set():
        print(f"\033[95mSeconds : {i}\033[00m")
        sleep(1)
        i+=1
        # stop the system at 45th second
        if i == 45:
            stop_event.set()

# main program block
if __name__ == "__main__":

    # system stop event
    stop_event = Event()
    
    # mechanical systems are defined
    mech_sys   = ["feeder", "Press", "Paint", "oven"]
    # we set a trigger event for each system
    events     = [Event() for _ in range(len(mech_sys))]
    
    # we set a process for each system
    processes  = []
    for i in range(len(mech_sys)):
        processes.append(Process(target=machine, args=(mech_sys[i], events[i], 
                            events[(i+1)%len(mech_sys)], stop_event,)))

    # time counter thread and stop event
    clock_stop = Event()
    clock_th   = th(target=clock, args=(clock_stop, stop_event, ))
    clock_th.start()

    # processes started
    for p in processes:
        p.start()
    
    # initialization delay
    sleep(1)
    # first system is triggered
    events[0].set()
    
    # processes waited
    for p in processes:
        p.join()
    
    # stop the timer
    clock_stop.set()
    clock_th.join()

    print("ALL SYSTEMS INACTIVE!")