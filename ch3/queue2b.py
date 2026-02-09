# in this example there are three threads: producer, interface and
# consumer. Two queues are used between threads for data sharing

# time performance
from time import sleep, perf_counter
# queue library
from queue import Queue, Full, Empty
# thread library
from threading import Thread, Event

# global data
sampling_period     = 0.1   # seconds
buf_time            = 1     # seconds
buf_size            = buf_time // sampling_period # sample
buf_half_size       = buf_time / 2 # second
data                = []

# producer thread
def producer(cancel:Event, queue1):
    sample = 1
    # cont. until cancel is active
    while not (cancel.is_set()):
        try:
            # sample added to queue
            queue1.put(sample, block = False)
        except Full: # wait till queue is empty
            sleep(buf_half_size)
            continue
        else: # success
            # next sample
            sample = sample + 1
    
    # producer is stopped

# interface thread
def interface(cancel:Event, queue1, queue2):
    # start routine
    while not queue1.full():
        sleep(sampling_period)
    
    # cont. till cancel is active
    while not (cancel.is_set()):
        # queue2 filling routine
        try:
            # a sample is being drawn from q1
            sample = queue1.get(block = False) 
        except Empty: # wait until q1 full
            sleep(sampling_period) 
            continue
        else: # success
            ok = False
            while not ok:
                # put drawn sample to q2
                try:
                    # put the sample to q2
                    queue2.put(sample, block = False)
                except Full:
                    # wait for q2 empty
                    sleep(buf_half_size)
                    continue
                else:# success
                    # interface process delay
                    sleep(sampling_period / 10)
                    ok = True

            # mark job as done
            queue1.task_done()
    
    # playing is stopped...
    
# consumer thread
def consumer(cancel, pause:Event, queue2):
    # dropped sample counter
    n = 0
    # paused flag
    paused   = False

    # start routine
    print("Playing is started...")
    while not queue2.full():
        sleep(sampling_period)

    # record start time
    data.append(perf_counter())

    # cont. till cancel is active
    while not (cancel.is_set()):
        # pause signal is active, wait...
        while pause.is_set():
            paused = True
            print("\rPlaying is paused...", end="")
            sleep(sampling_period)
            if cancel.is_set(): # cancel is active, stop
                # cancel pause
                break
        if paused:# pause is in progress
            paused = False
            print("\nPlaying is resumed...")
        
        # sampling starts
        try:
            # a sample is drawn from q2
            sample = queue2.get(block = False) 
        except Empty:
            # a sample is dropped
            print("queue Empty!")
            sample = 0
            n = n + 1
            sleep(sampling_period) 
            continue
        else:
            sleep(sampling_period) # sample time
            # mark job as done
            queue2.task_done()

    # record stop time
    data.append(perf_counter())
    data.append(sample)

    print(f"Playing is ended... Dropped sample count: {n} ")

# queue flush routine
def queue_flush(queue):
    while not queue.empty():
        queue.get(block=False)
        queue.task_done()
        
# main program bolumu
def main():
    # queues created
    queue1   = Queue(maxsize = buf_size)
    queue2   = Queue(maxsize = buf_size)
    
    # producer cancel event
    cancel = Event()

    # producer pause event
    pause = Event()

    # producer thread created
    producer_thread  = Thread(
              target = producer,
              args   = (cancel, queue1,)
    )

    # interface thread created
    interface_thread  = Thread(
               target = interface,
               args   = (cancel, queue1, queue2,)
    )

    # consumer thread created and started
    consumer_thread = Thread(
             target = consumer,
             args   = (cancel, pause, queue2,),
    )

    # threads started
    producer_thread.start()
    interface_thread.start()
    consumer_thread.start()
    
    # start playing
    sleep(10) # second
    
    # pause playing
    pause_time = 5
    pause.set()
    sleep(pause_time)# second
    
    # resume playing
    pause.clear()
    sleep(15)# second
    
    # cancel playing
    cancel.set()

    # wait for threads to complete
    producer_thread.join()
    interface_thread.join()
    consumer_thread.join()
    
    # flush all queues and wait for them
    queue_flush(queue1)
    queue_flush(queue2)
    
    queue1.join()
    queue2.join()
    
    print(f"Total execution time = {data[1] - data[0]:3.5f} "
          f"seconds and last sample : {data[2]}")
    print(f"Average sampling time = "
          f"{(data[1] - data[0] - pause_time) / data[2]:3.5f} seconds")

if __name__ == '__main__':
    main()
