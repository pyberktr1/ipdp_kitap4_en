# this example shows the use of locks in multi processes

# multi process library
from multiprocessing import Process, Lock
# time performance
import time

# this process task defines a drill sharing between 
# multiple techs
def drill(tech, lock):
    
    print(f"{tech} request the drill")

    # only one tech is allowed to enter this section
    with lock: # we use a with context for automatic close
        print(f"{tech} drilling...")
        time.sleep(2)  # simulate process delay
        print(f"{tech} completed drill job.")

# ana program bolumu
if __name__ == "__main__":

    # we use a lock to safely share the use of drill
    lock = Lock()
    # technicians
    techs = ["Bill", "Harry", "Nigel"]

    # we define a process for each technician
    for tech in techs:
        Process(target=drill, args=(tech, lock,)).start()