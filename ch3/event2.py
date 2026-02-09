# thread synchronization example using events

# thread library
from threading import Thread, Event
# time eprformance
from time import sleep, perf_counter

def task(play , trigger: Event, id: int) -> None:
    # wait for thread start
    play.wait()
    # thread operations
    print(f"thread {id} starts and waits...\n",end="")
    sleep(2)
    # we make an intentional delay here
    if id == 3:
        sleep(5)
    print(f"thread{id} completed.")
    # trigger next thread
    trigger.set()

# main program block
def main() -> None:
    
    # maximum thread number
    max_threads = 5
    
    # events and threads created
    events    = []
    threads   = []
    for i in range(max_threads):
        events.append(Event())
    
    for i in range(max_threads):
        # trigger events determined
        if i < (max_threads - 1):
            k = i + 1
        else:
            k = i
        threads.append(Thread(target=task, args=(events[i], events[k], i+1)))

    # threads started
    for thread in threads:
        thread.start()

    print("All tasks started...")
    print()
    
    start = perf_counter()
    
    # all tasks will be completed serially
    # lets trigger the first event
    # which will eventually trigger other
    # events
    events[0].set()
    
    # wait for all tasks to complete
    for thread in threads:
        thread.join()
    
    # stop time
    stop = perf_counter()
    
    print("All tasks are stopped...")
    print(f"All tasks took {stop - start : 2.5f} seconds")
    
# call to main()
if __name__ == "__main__":
    main()
