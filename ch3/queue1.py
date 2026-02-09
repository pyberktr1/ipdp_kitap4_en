# this example show how two threads can share
# data using a queue

# time performance
from time import sleep, perf_counter
# queue library
from queue import Queue, Full, Empty
# thread library
from threading import Thread, Event

# producer thread
def producer(producer_cancel:Event, queue):
    n = 0 # dropped sample counter
    # 100 samples will be produced.
    for i in range(1, 101):
        # sampling start time
        start = perf_counter()
        try:
            sleep(0.5) # sample time
            # a sample put to queue
            queue.put(i, block = False)
        except Full:
            print("\033[91mQueue Full!\033[0m")
            n = n + 1
            continue
        else:
            stop = perf_counter()
            print(f"\033[91msample {i} is added: time = ",
                  f"{stop - start : 2.5f} queue : {queue.qsize()}\033[0m")
    print(f"\033[91mproduction is stopped... Dropped sample count: {n} \033[0m")
    producer_cancel.set()

# consumer thread
def consumer(producer_cancel:Event, queue):
    # sample counter
    n = 0
    # all samples will be drawn from the queue
    while not (queue.empty() and producer_cancel.is_set()):
        # sampling starts
        start = perf_counter()
        try:
            # draw a sample from queue
            sample = queue.get(block = False) 
        except Empty:
            print("queue is empty!")
            sleep(0.125) # dummy sample delay
            continue
        else:
            n = n + 1
            sleep(0.25)     # sample time
            # sleep(0.5)    # extra sample time
            stop = perf_counter()
            print(f"{sample} is drawn from queue: time = ",
                  f"{stop - start : 2.5f} queue : {queue.qsize()}")
            # mark job as done in queue
            queue.task_done()
    print(f"consumer is stopped... sample count: {n} ")

# main program block
def main():
    # queue created with max size 10
    queue   = Queue(maxsize = 10)
    # producer cancel  event
    producer_cancel = Event()

    # producer thread created and started
    producer_thread  = Thread(
        target = producer,
        args   = (producer_cancel, queue,)
    )
    producer_thread.start()

    # consumer thread created and started
    consumer_thread = Thread(
        target = consumer,
        args   = (producer_cancel, queue,),
    )
    consumer_thread.start()

    # wait for threads to complete
    producer_thread.join()
    consumer_thread.join()

    # wait for the queue to complete
    queue.join()

if __name__ == '__main__':
    main()
