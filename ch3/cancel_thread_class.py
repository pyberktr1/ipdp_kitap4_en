# This example shows how a thread class can be 
# cancelled using an event

# thread library
from threading import Thread, Event
# time performance
from time import sleep

# the thread class that can be cancelled
class th_class(Thread):
    def __init__(self, cancel, result, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cancel = cancel # cancel signal
        self.result = result # result variable

    def run(self):
        cursor = ("|","/","-","\\") # cursor symbols
        for i in range(10):
            sleep(1)
            print(f"\r thread execution time: {i+1} second  {cursor[i%4]}", end="")
            if self.cancel.is_set(): # is cancel active?
                print("\nthread is cancelled")
                # abnormal cancel status 
                # is returned
                self.result[0] = -1
                return
    
        # thread finalized normally
        print("\nthread is stopped normally")
        self.result[0] = 0
        return

# main program block
def main() -> None:
    
    # cancel signal created
    cancel = Event()
    result = [None]
    
    # thread created from th_class
    thread = th_class(cancel, result)
    
    # thread started
    thread.start()

    # thread is waited here
    # for normal thread cancellation
    # add an extra delay here
    sleep(3)
    #sleep(8)

    # we set cancel signal here
    if thread.is_alive(): # is thread still alive?
        print("\nthread will be cancelled..")
        cancel.set()
    else:
        print("thread is not alive. thread cancellation is cancelled...")
    
    # we are waiting here to get the result from thread    
    while thread.is_alive():
        pass
        
    print(f"result: {result[0]}")
   
if __name__ == '__main__':
    main()
    
