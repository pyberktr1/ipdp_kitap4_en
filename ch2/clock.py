# non-threaded clock application
# CTRL+C to end the execution
# due to infinite loop

# zamanlayici kutuphanesi
import time

# clock function
def clock():
    sec = 0 # seconds counter
    # infinite counter
    while True:
        sec = sec + 1
        time.sleep(1)
        print(f"\r{sec} seconds elapsed...", end="")

# main block
clock()

# below code does not find execution chance
input("Press Enter to end...\n")
