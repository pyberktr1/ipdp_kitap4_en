# this example shows how wait for events in processes

# process library
from multiprocessing import Process, Event
# time performance
from time import sleep
# thread library
from threading import Thread

# record player process
def player(play, stop):
    # cont. until stop is active
    while not stop.is_set():
        # we have a pause
        # a pause longer than 5s
        # will cancel the playing
        # in the channel automatically
        if (play.wait(timeout=5)):
            sleep(0.1)# play
        else:
            stop.set() # stop

# timer process
def timer(second, close):
    # delay for given seconds
    for i in range(round(second*10)):
        # if close signal is active
        # stop timer function
        if close.is_set():
            return
        # 0.1 second delay
        sleep(0.1)  

# commander process that send timed commands
# to each channel      
def commander(ch_count, plays, stops, close):
    # cont. till shutdown
    while not close.is_set():
        # pause all channels with 2 seconds interval
        for i in range(ch_count):
            # wait before command
            timer(2, close)
            # pause the corresponding channel
            plays[i].clear()
            
        # wait before another command sequence
        timer(2, close)
        
        # set all the channels to play status 
        for i in range(ch_count):
            # is a shutdown signal active?
            if close.is_set():
                break
            plays[i].set() 
            
    # set all the channles to play state before
    # shutdown. Otherwise we need to wait for
    # paused channels to be automatically
    # cancelled up to 5 seconds
    for i in range(ch_count):
        plays[i].set()
        stops[i].set()

# monitor process    
def monitor(ch_count, plays, stops):
    # wait for all processes to start
    sleep(0.5)
    sn=0.0 # seconds counter
    # count in infinite loop
    while True:
        # message buffer, set to time code first
        msg = f"timer:{sn:3.2f} sec. "
        
        # add all channel states to the message buffer
        for i in range(ch_count):
            if stops[i].is_set():
                status = "stopped"
            elif plays[i].is_set():
                status = "plays"
            else:
                status = "paused"
            # add all data to buffer   
            msg = msg + f"ch{i}.{status:10s}::"
        
        print("\r" + msg, end="")
        sleep(0.1) # refresh time
        sn+=0.1    # increment seconds counter
    
# main program block   
if __name__ == "__main__":
    
    # close signal
    close = Event()
    
    # channel count
    ch_count = 4
    
    # create a process, stop and play/pause event
    # for each cahnnel
    processes = []
    plays     = []
    stops     = []
    for i in range(ch_count):
        play = Event()
        stop = Event()
        play.set() # set to play state
        plays.append(play)
        stops.append(stop)
        processes.append(Process(target=player, args=(play, stop, )))
    
    # daemon type commander and monitor threads
    thread1 = Thread(target=commander, args=(ch_count, 
            plays, stops, close, ), daemon=True)
    thread2 = Thread(target=monitor, args=(ch_count, 
            plays, stops,), daemon=True)
    # thread s started
    thread1.start()
    thread2.start()
    
    # processes started
    for p in processes:
        p.start()
    
    print("PRESS ENTER TO END PLAYING...")
    input() 
    close.set() # SHUTDOWN IN PROGRESS
    
    # wait for all processes to stop
    for p in processes:
        p.join()