# this example shows the handling of event loop manually

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
    
# main program block
if __name__ == "__main__":
    
    # evloop query, for normal operation
    # deactivate following two lines
    #evloop = asyncio.get_event_loop()
    #print(f"Evloop status before opening: \n{evloop}")
    
    # open a new evloop
    evloop = asyncio.new_event_loop()
    # set it as default
    asyncio.set_event_loop(evloop)
    
    # evloop query
    evloop = asyncio.get_event_loop()
    print(f"Evloop status after opening: \n{evloop}")
    
    # execute a coro by throwing it to evloop
    # evloop stays active till coro ends
    # then it is also stopped but not closed
    evloop.run_until_complete(main())

    # evloop query
    evloop = asyncio.get_event_loop()
    print(f"Evloop status after main coro: \n{evloop}")
    