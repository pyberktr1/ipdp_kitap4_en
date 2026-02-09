# This example shows the use of pipes in
# inter-process communication

# process library
import multiprocessing as mp
# time performance
import time

# xmitter process
def xmitter(pipe):
    print("\nTransmitting...")
    time.sleep(5)
    # we send a message through pipe
    pipe.send("xmitter says Hello!")
    # we need to close the pipe after use
    pipe.close()

# receiver process
def receiver(pipe):
    print("\nReceiving...")
    time.sleep(6)
    # we get a message from pipe
    msg = pipe.recv()
    print(f"\nReceived: {msg}")

# main program block
if __name__ == '__main__':
    # receiver receives from r_pipe side
    # and xmitter transmits from x_pipe side
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
