# this example shows the use of sockets in 
# inter-process communication

# multi process library
from multiprocessing import Process
# socket library
import socket

# server process (receiving side)
def server():
    # we define a socket
    s = socket.socket()
    # localhost:127.0.0.1 address, 12345 port
    # opened for listening
    s.bind(("localhost", 12345))
    print("listening socket: ",s.getsockname())
    s.listen(1)
    # link and addresss obtained for comm.
    link, adr = s.accept()
    print("receive socket: ",link)
    print("receive address: ",adr)
    # the received packet is dumped
    print(link.recv(1024).decode())
    # we always close the opened link
    link.close()

# client proses (xmitting side)
def client():
    # we define a socket for xmit
    s = socket.socket()
    # localhost, 12345 port set for xmit
    # this is the opposite side listen link address
    s.connect(("localhost", 12345))
    print("xmit socket  : ",s.getsockname())
    # a data packet (least than 1024 bytes) is sent
    s.send(b"client says hello!")
    # we need to close the link
    s.close()
    
# mian program block
if __name__ == "__main__":

    print("XMIT STARTS!")    
    
    # processes created
    p1 = Process(target=server)
    p2 = Process(target=client)
    
    # processes started
    p1.start()
    p2.start()
    
    # processes waited  
    p1.join()
    p2.join()

    # xmit complete 
    print("END OF XMISSION!")