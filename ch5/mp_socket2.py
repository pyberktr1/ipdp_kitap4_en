# this example shows two way communication between processes
# using sockets

# multi process library
from multiprocessing import Process
# socket library
import socket
# time performance
from time import sleep

# server process (receive first, xmit last)
def server():
    # we set listen link
    s_input = socket.socket()
    # socket opened for listening  
    s_input.bind(("localhost", 12345))
    s_input.listen(1)
    # link and addresss for receiving accepted
    link, adr = s_input.accept()
    
    # we set a link for xmission
    s_output = socket.socket()
    # socket set for xmission
    s_output.connect(("localhost", 12346))

    # we draw a data packet from input socket
    print(link.recv(1024).decode())
    # we set a delay
    sleep(2)
    
    # we are sending a packet
    s_output.send(b"Hello from Server!")
    
    # all the links must be closed
    link.close()
    s_output.close()

# client process (xmit first, receive last)
def client():
    # wait for the server up
    sleep(2)
    # we set an output socket for xmission
    s_output = socket.socket()
    # socket linked for connection
    s_output.connect(("localhost", 12345))
    
    # we set an input socket for receiving
    s_input = socket.socket()
    # socket linked for listening
    s_input.bind(("localhost", 12346))
    s_input.listen(1)
    # link and address for connection accepted
    link, adr = s_input.accept()

    # we send a data packet
    s_output.send(b"client says hello!")
    
    # dump the received packet
    print(link.recv(1024).decode())

    # all the links must be closed
    link.close()
    s_output.close()

# main program block
if __name__ == "__main__":
    
    print("COMM STARTS")
    
    # processes created
    p1 = Process(target=server)
    p2 = Process(target=client)
    
    # processes started
    p1.start()
    p2.start()
    
    # processes waited  
    p1.join()
    p2.join()

    print("COMM STOPS")