# this example shows the use of timers 
# timers operates over threads

# time library
import time
# thread library
from threading import Thread as thread
from threading import Timer, Event

# timer function
def timer_f():
    # if close signal is active then shutdown
    if not close.is_set():
        sec[0] = sec[0] + incr
        Timer(incr, timer_f).start()
    else:
        print("timer closed!")
        
# monitor daemon thread
def monitor():
    while not close.is_set():
        print(f"\rclock(timer):{sec[0]: 2.3f} clock(main):{sec[1]: 2.3f}",
                end="")
        # refresh rate is maximum when no delay, 
        # in this case CPU gets busy excessively
        # refresh intervals longer than 0.05 sec is suitable
        #time.sleep(0.1)# refresh delay

# main program block
if __name__ == "__main__":
    
    # Global data
    # seconds counter for two clocks
    sec = [0.0]*2
    # display resolution
    incr  = 0.01# sec
    # stop time
    stop_time  = 5.0# sec
    # close event
    close = Event()

    print("CLOCK STARTED!")

    # monitor DAEMON thread
    thread(target=monitor, daemon=True).start()
    
    # start time
    start = time.perf_counter()
    
    # timer started
    timer_f()
    
    # main timer function
    while round(sec[1], 5)<stop_time:
        time.sleep(incr)
        sec[1] = sec[1] + incr
    
    # timer stop_time recorded
    s0 = sec[0]
    
    # stop_time recorded
    stop = time.perf_counter() - start

    # all system closes, 
    time.sleep(0.1)# delay necessary to see the actual clock
    close.set()

    print("\nfrom start to stop_time :",
        f"{stop: 2.3f} sec")
    print(f"difference between timer and main clock :",
        f"{s0 - sec[1]: 2.3f} sec")
    print(f"difference between real time and main clock :",
        f"{stop - sec[1]: 2.3f} sec")
    
