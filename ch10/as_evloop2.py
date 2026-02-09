# this example shows manul event loop use 
# An evloop is opened first, than main coro is thrown to it
# The vloop is started to run forever.
# the main coro starts a task which stops the evloop after
# 10 seconds. After stopping the evloop is closed.

# async io library
import asyncio
# time library
import time

# an asynchronous coro
async def timer():
    # timer loop lasts 10 seconds
    for i in range(10):# 10 seconds
        print(f"\rSeconds::{i}", end="")
        await asyncio.sleep(1)
    # stop the running evloop
    # by deactiving below line we give the closing
    # control to the main coro.
    # it is not a good practice to to stop or
    # close a running evloop without completing all
    # the tasks.
    #asyncio.get_running_loop().stop()
    
# main coro
async def main():
    
    # Query actual evloop that is running
    evloop = asyncio.get_running_loop()
    print(f"main coro running evloop: \n{evloop}")
    
    # start time
    start = time.perf_counter()
    # start tasks
    await asyncio.create_task(timer())
    # stop time 
    stop = time.perf_counter()
    print(f"\nexecution time:{stop-start:2.3f} seconds")
    # stop running evloop
    evloop.stop()
    
# main program block
if __name__ == "__main__":
      
    # open a new evloop
    evloop = asyncio.new_event_loop()
    # set it as default
    asyncio.set_event_loop(evloop)
    
    # throw a coro as a task to the evloop
    # actual execution is realized when the
    # evloop is set to run mode.
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
        
    # evloop query
    evloop = asyncio.get_event_loop()
    print(f"Evloop status after closing: \n{evloop}")
    