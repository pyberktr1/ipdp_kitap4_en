# this example shows the use of callback functions
# with event loops. Timer function in this example 
# is implemented as a callback function instead a coro
# definition. The program is ended after 10 seconds by the
# main coro.

# async io library
import asyncio
# time library
import time

# callback timer function
def timer(i, evloop):
    # is cancel signal active
    if cancel.is_set():
        return# end the callback
    # timer loop
    print(f"\rSeconds:{i}", end="")
    # increment seconds counter
    i+=1
    # make a callback to itself which will be active
    # after a 1 second delay. A non-blocking timing
    # is executed by the evloop. however the actual duration
    # of the delay is not guaranteed. It is at least 1 seconds,
    # but may be more according to the load of the evloop.
    evloop.call_later(1, timer, i, evloop)
    # Any blocking operation is not allowed beyond this point.
    # otherwise timer function does not operate normally.
    # the below blocking sleep() command is given intentionally
    # to show its consequences.
    #time.sleep(2)
      
# main coro
async def main():
    
    # Query actual evloop that is running
    evloop = asyncio.get_running_loop()
    print(f"main coro running evloop: \n{evloop}")
    
    # start time
    start = time.perf_counter()
    
    # evloop time is displayed
    print(f"Evloop time:{evloop.time():.0f}")
    # we make a direct call to timer() callback function
    # it is handled immediately in the evloop without a delay
    evloop.call_soon(timer, 0, evloop)
    # 10 seconds delay
    await asyncio.sleep(10)
    # cancel the timer() callback
    print(f"\ntimer will be cancelled! "
          f"\nEvloop time:{evloop.time():.0f}")
    cancel.set()
    # additional 3 seconds delay
    await asyncio.sleep(3)
    
    # stop time
    stop = time.perf_counter()
    print(f"\nexecution time:{stop-start:2.3f} seconds")
    # stop the evloop
    evloop.stop()
    
# main program block
if __name__ == "__main__":
    
    # we set a cancel event
    cancel = asyncio.Event()
      
    # open a new evloop
    evloop = asyncio.new_event_loop()
        
    # throw the main coro to the evloop as a task
    evloop.create_task(main())
    
    # run the evloop
    try:
        evloop.run_forever()# runs forever until a stop signal is received
    finally:# execution cont. from here after stopping
        # we need to stop the evloop before closing
        if evloop.is_running():# is evloop running?
            # stop running evloop
            evloop.stop()
        print("EVLOOP closes...")
        # we need to shutdown async generators first
        evloop.run_until_complete(evloop.shutdown_asyncgens())
        evloop.close() # stopped evloop is closed  
        