# inter-thread communication example based on events

# thread library
from threading import Thread, Event
# time performance
from time import sleep

def task(event: Event, id: int) -> None:
    print(f"thread{id} started and waits...\n",end="")
    event.wait()
    print(f"thread{id} completed.")

# main program block
def main() -> None:
    # an event is created
    event = Event()
    
    # threads defined
    thread1 = Thread(target=task, args=(event,1))
    thread2 = Thread(target=task, args=(event,2))

    # threads started
    thread1.start()
    thread2.start()

    print("All tasks started...")
    # delay for all tasks to complete
    sleep(3) 
    # all the tasks are being finalized
    print("All tasks will be closed...")
    event.set()
    
# call to main()
if __name__ == "__main__":
    main()
