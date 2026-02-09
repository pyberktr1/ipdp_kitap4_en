# This example shows the use of conditions to regulate sharing
# between processes

# multi process library
from multiprocessing import Process, Lock, Condition, Queue
# time library
import time
# random number library
import random
# th library
from threading import Thread as th

# producer process
# only one producer bakes breads
def producer(basket, bread_ok):
    # initial delay
    #time.sleep(2)
    for i in range(5):# initially 5 breads are baked
        # bake delay
        time.sleep(random.uniform(0.1, 0.5))
        # we acquire a lock to the bread_ok condition
        with bread_ok:
            # a bread is baked
            bread = f"bread#{i+1}"
            # put the bread in the basket
            basket.put(bread)
            print(f"Baker: {bread} baked!")
            # we notify consumers that a bread is available
            bread_ok.notify()  

    # last breads are baked
    for i in range(2):# last breads equal to the number of consumers
        # production delay
        time.sleep(random.uniform(0.1, 0.5))
        # we acquire a lock to the condition
        with bread_ok:
            # a bread is baked
            bread = f"last bread"
            # put the bread in the basket
            basket.put(bread)
            print(f"Baker: {bread} baked!")
            # we notify the consumers
            bread_ok.notify()  

# consumer process
def consumer(t_id, basket, bread_ok):
    while True:# cont. till all breads are consumed
        # we acquire a lock to the condition
        with bread_ok:
            while basket.empty():# if no bread wait...
                print(f"Client#{t_id} waits for a bread...")
                bread_ok.wait()  # wait for bread 
            
            # there is bread in the basket
            bread = basket.get()
            print(f"Client#{t_id}: took the {bread} ")
            # is this the last one?
            if "last bread" in bread:  
                break# no breads, finish process

# main program block
if __name__ == "__main__":

    # Global data
    # fresh baked bread basket queue
    basket        = Queue()
    # lock for safe sharing of basket queue
    basket_lock = Lock()
    # the condition that notifies consumers
    # that there is a bread in the basket
    bread_ok = Condition(basket_lock)
    
    print("OUR BAKERY IS OPEN!")

    # producer process 
    p1 = Process(target=producer, args=(basket, bread_ok, ))
    p1.start()

    # initial delay
    #time.sleep(1)
    
    # consumer processes
    p2 = Process(target=consumer, args=(1, basket, bread_ok, ))
    p2.start()

    p3 = Process(target=consumer, args=(2, basket, bread_ok, ))
    p3.start()

    # wait all the processes to complete
    p1.join()
    p2.join()
    p3.join()
    
    # close the queue
    basket.close()
    print("OUR BAKERY IS CLOSED!")
