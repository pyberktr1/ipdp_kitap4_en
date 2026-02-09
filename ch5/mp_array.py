# This example shows the safe sharing of arrays between processes

# nulti process library
from multiprocessing import Process, Array

# reservation process
def reserve(no, rooms):
    # we acquire a lock to the shared array
    with rooms.get_lock():
        rooms[no] = no + 1
        print(f"Firm{no}, reserved the room {rooms[no]}.")

# main program block
if __name__ == "__main__":
    # there are 7 firms to reserve 
    # 7 rooms from a hotel array structure
    rooms = Array('i', 7)
    # we set a process for each firm
    processes = []
    
    for i in range(7):
        p = Process(target=reserve, args=(i, rooms))
        processes.append(p)
        p.start()
    # wait for processes    
    for p in processes:
        p.join()
        
    print("\nreserve list:")
    print(list(rooms))
