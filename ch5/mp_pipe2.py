# this examples shows the two way use of pipes

# process library
import multiprocessing as mp
# time performance
import time

# xmitter process
def xmitter(pipe):
    # we use a with context to use the pipe
    with pipe as b:
        print("\nTransmitting...")
        time.sleep(5)
        # we send a message
        b.send("xmitter says Hello!")
        # we enter into listening mode
        # if there si no response the process will block
        msg = b.recv()
        print(f"\nxmitter receives: {msg}")

# receiver prosesi
def receiver(pipe):
    with pipe as b:
        print("\nReceiving...")
        # we made intentional delay here
        #time.sleep(7)
        msg = b.recv()
        print(f"\nreceiver receives: {msg}")
        time.sleep(1)
        # only one of the below messages will be received
        b.send("receiver says hello")
        b.send("receiver says hello again")

# main program block
if __name__ == '__main__':
    # we create a full-dublex pipe
    r_pipe, x_pipe = mp.Pipe()
    
    # processes created
    p1 = mp.Process(target=xmitter, args=(x_pipe,))
    p2 = mp.Process(target=receiver,args=(r_pipe,))

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
