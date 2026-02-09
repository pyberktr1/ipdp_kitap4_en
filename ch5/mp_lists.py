# this example shows list sharing using managers

# multi process library
from multiprocessing import Process, Manager
# random number generator
import random
# time performance
import time

# message box process
def message(user, msg_box, lock):
    # message box process simulation delay
    time.sleep(5*random.random())# 0-5 seconds random delay
    msg = f"{user:7s}: {time.strftime('%H:%M:%S')} sent a message"

    # only one user can enter this section
    with lock:
        msg_box.append(msg)
        print(f"user {user :7s}: sent a message!")

# main program block
if __name__ == "__main__":
    # manager created
    with Manager() as mn:
        # message box created as a shared list
        msg_box   = mn.list()
        # manager used to define a global lock
        lock      = mn.Lock()
        # users
        users     = ["Harry", "Bill", "Mike", "Sammy"]
        # processes created
        processes = []
        for user in users:
            p = Process(target=message, args=(user, msg_box, lock,))
            processes.append(p)
            p.start()

        # wait processes
        for p in processes:
            p.join()

        # we will dump all the messages in the message box
        print("\nmessage box:")
        print("----------------------------------------------------")
        print()

        for line in msg_box:
            print(" :::", line)
        
        # alternative list method
        print("----------------------------------------------------")
        print()
        #print(list(msg_box))
    # it is impossible to reach data in the list after manager is
    # closed. So below code line is invalid.
    #print(list(msg_box))   