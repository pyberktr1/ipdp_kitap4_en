# this example shows the use of queues in data sharing
# between processes. Since queues are one way, there will
# be problems if they are used in two way applications. 

# multi process library
import multiprocessing as mp
# time performance
import time

# printer process
def printer(queue):
    print("\nPrinting...")
    time.sleep(5)
    # we put a message to the queue
    queue.put("printer says Hello!")
    # we read from queue
    msg = queue.get()
    print(f"\nPrinter receives: {msg}")

# reader prosesi
def reader(queue):
    print("\nReading...")
    # we delay reading intentionally
    #time.sleep(7)
    # we get a message from queue
    msg = queue.get()
    print(f"\nReceived: {msg}")
    time.sleep(1)
    # we will add two messages to the queue
    # but only one of them will be drawn
    queue.put("Reader says Hello")
    queue.put("Reader says Hello again")

# main program block
if __name__ == '__main__':
    # queue created
    queue = mp.Queue()

    # processes created
    p1 = mp.Process(target=printer,  args=(queue,))
    p2 = mp.Process(target=reader, args=(queue,))

    # processes started
    p1.start()
    p2.start()
    
    # time count
    for i in range(10):
        print(f"\rSeconds : {i}", end="")
        time.sleep(1)
    
    # processes waited
    p1.join()
    p2.join()
    
    # queues must be closed after use
    queue.close()