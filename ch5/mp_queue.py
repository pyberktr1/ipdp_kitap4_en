# this example show the use of queues in data sharing
# between processes

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

# reader prosesi
def reader(queue):
    print("\nReading...")
    # we get a message from queue
    msg = queue.get()
    print(f"\nReceived: {msg}")

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