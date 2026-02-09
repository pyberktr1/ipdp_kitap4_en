# this example use of value objects for safe sharing of data
# between processes. Pears and Bears process

# multi-process library
from multiprocessing import Process, Value, Lock
# time library
import time

# pear sharing between bears
def pear(name, pears):
    # we acquire a lock for pear sharing
    with pears.get_lock():
        # are there any pears to share?
        if pears.value > 0:
            # yes
            pears.value -= 1 # eat that pear, bear!
            print(f"Bear {name} eat a pear. remained pear: {pears.value}")
        else:
            # no. pity you bear!
            print(f"Pity! Bear {name} has no pear to eat.")

# ana program bolumu
if __name__ == "__main__":
    # we have only three pears to share
    pears = Value('i', 3)
    # we have 4 bears for sharing pears
    bears = ["Grease", "Brown", "Black", "Zippy"]
    
    # we set a process for each of the bears
    for name in bears:
        Process(target=pear, args=(name, pears)).start()