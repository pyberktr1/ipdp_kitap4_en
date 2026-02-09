# daemon thread sample application
# despite there is an infinite loop in the
# thread task, it is now possible to end
# the task.

# threading library
from threading import Thread
# time performance
import time

# clock task
def clock():
    sec = 0
    # seconds counted in a infinite loop
    while True:
        sec = sec + 1
        time.sleep(1)
        print(f"\r{sec} seconds elapsed...", end="")

# main block
# thread is defined as a daemon thread
thread = Thread(target = clock, daemon = True)
thread.start()

# after main program is ended, the clock task 
# is also ended automatically.
input("\nPress Enter to end...\033[F")
