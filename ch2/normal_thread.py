# non-daemon thread sample application
# since there is an infinite loop in the
# thread task, it is impossible to end
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
thread = Thread(target = clock)
thread.start()

# even main program is ended, the clock continues to
# count seconds due to unstopped thread
input("Press Enter to end...\n")
