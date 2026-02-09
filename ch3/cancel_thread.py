# This example shows how a thread task can be cancelled
# using an event

# thread library
from threading import Thread, Event
# time performance
from time import sleep

# thread task that will be cancelled
def task(cancel: Event, result):
    cursor = ("|","/","-","\\")
    for i in range(10):
        sleep(1)
        print(f"\r thread execution time: {i+1} second  {cursor[i%4]}", end="")
        if cancel.is_set(): # is cancel signal active?
            print("\nthread is cancelled...")
            # anormal cancel status
            # is returned
            result[0] = -1
            return
    
    # thread cancellation is normal 
    print("\nthread completed its normal execution")
    result[0] = 0
    return

def main() -> None:
    
    # cancel signal created
    cancel = Event()
    result = [None]
    # thread created
    thread = Thread(target=task, args=(cancel, result,))
    
    # thread started
    thread.start()

    # thread is waited here.
    # for abnormal thread cancellation we
    # define a shorter delay than 10 seconds.
    sleep(3)
    #sleep(8)# activate for normal cancellation

    # we set a signal for thread cancellation
    if thread.is_alive(): # is thread alive?
        print("\nthread cancel in progress...")
        cancel.set()
    else:
        print("thread is not alive. So thread cancellation is cancelled...")
        
    # we wait for thread finalization for obtaining the result 
    # try to see the result when this part is inactivated.
    while thread.is_alive():
        pass

    print(f"Result: {result[0]}")

   
if __name__ == '__main__':
    main()
    
