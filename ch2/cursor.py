# animated cursor application with daemon thread

# thread library
from threading import Thread
# t,me performance
import time

# animated cursor task
def cursor():
    symbol = ["|","/","-","\\"]
    # infinite loop
    while True:
        for s in symbol:
            time.sleep(0.1)
            print(f"{s}\b", end="", flush=True)
        
# main block
thread = Thread(target = cursor, daemon = True)
thread.start()

# when pressed to Enter, all tasks are ended
input("Press Enter to end...")
