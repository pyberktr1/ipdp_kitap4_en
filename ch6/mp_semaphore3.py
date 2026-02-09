# this example shows fair printer sharing between processes
# using semaphores.

# multi process library
from multiprocessing import Process, Semaphore, Array, Event
# time library
from time import sleep
# thread library
from threading import Thread

# printer process
def printer(user, pages, printers, print_sem):
    # page limit per round
    max_page = 2
    # cont. till max_page limit exceeds    
    while pages[user]>0:
        # printer queue
        with print_sem:# wait if no free printer
            # attach printer to the user
            with printers.get_lock():
                if 1 not in printers:   # is printer#1 free?
                    printers[user]=1
                elif 2 not in printers: # is printer#2 free?
                    printers[user]=2
                elif 3 not in printers: # is printer#3 free?
                    printers[user]=3
                    
            # print till max_page limit
            for i in range(max_page):
                # printing time per page
                sleep(1.5)
                # decrement page counter
                pages[user]-=1
                if pages[user]==0:
                    # no pages to print
                    break# stop task
            
            # free printer in use
            with printers.get_lock():
                printers[user]=0
                
# printing status monitor        
def monitor(n_user, pages, printers):
    sec = 0.0 # seconds counter
    # cont. till program close
    while True:
        # prepare status message
        # show seconds
        msg = f"Time:{sec:3.2f} sec. "
        
        # add all user status to the message
        for i in range(n_user):
            # active users will have red colour
            if printers[i]>0:
                color = 91
            else:
                color = 0
            msg = msg + f"\033[{color}m{printers[i]}/{i}/{pages[i]}\033[00m::"
            
        # display the message
        print("\r" + msg + "          ", end="")
        # refresh delay
        sleep(0.1)
        # increment seconds counter
        sec+=0.1
    
# main program block   
if __name__ == "__main__":

    print("PRINTER STATUS...")
    print("printer/user/pages left")
    
    # printer count
    n_print_sem = 3
    # user count
    n_user      = 5  
    # number of pages that will printed by each user
    pages       = Array("i", [5, 7, 8, 9, 3])
    # printers status of each user recorded to this array
    # if a user's cell is filled with a zero value this
    # shows that user has no printer in use
    printers    = Array("i", n_user)
    
    # only 3 printers
    print_sem = Semaphore(n_print_sem)
    
    # we set a process for each user
    processes = []
    for i in range(n_user):
        processes.append(Process(target=printer, args=(i, 
                     pages, printers, print_sem,)))
    
    # monitor thread
    thread1 = Thread(target=monitor, args=(n_user, 
                    pages, printers,), daemon=True)
    
    # monitor thread started
    thread1.start()
    
    # processes started
    for p in processes:
        p.start()

    # processes waited
    for p in processes:
        p.join()
    
    # monitor thread shutdown delay
    sleep(1)